# Main Satellite Code that does 3 things: Gets IMU data, activates magnetorquer to prevent tumbling,
# and sends telemetry to dashboard/mission control

import bluetooth
import network
import time
import machine
import struct
import math
from umqtt.simple import MQTTClient

# ================= WIFI + MQTT =================
SSID = "YOUR_SSID"
PASSWORD = "YOUR_PASSWORD"
MQTT_BROKER = "YOUR_LAPTOP_LOCAL_IP"
MQTT_PORT = 1883
TOPIC = b"mars/telemetry"
CLIENT_ID = b"esp32c3_team18"

# These IDs must match with those of ground station
SERVICE_UUID = bluetooth.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
CHAR_UUID = bluetooth.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")

# ================= HARDWARE =================
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
MPU_ADDR = 0x68
MPU_OK = False

# --- MAGNETORQUER SETUP (PINS 6 & 8) ---
# Set frequency to 1kHz for smooth 0.5A current control
coil_a = machine.PWM(machine.Pin(6), freq=1000, duty=1023)  # Default HIGH (OFF)
coil_b = machine.PWM(machine.Pin(8), freq=1000, duty=1023)  # Default HIGH (OFF)


def set_torquer(power):
    """
    Controls the H-bridge direction and strength.
    'power' ranges from -1023 (Full Reverse) to 1023 (Full Forward).
    """
    if abs(power) < 50:  # Deadzone to prevent micro-jitter
        coil_a.duty(1023)  # Both HIGH = Bridge OFF
        coil_b.duty(1023)
        return

    # Logic: One pin stays HIGH (P-MOS OFF), other pin pulses toward LOW (P-MOS pulsing ON)
    if power > 0:
        # Forward: Pin A pulses, Pin B stays OFF
        val = 1023 - int(power)
        coil_a.duty(val)
        coil_b.duty(1023)
    else:
        # Reverse: Pin B pulses, Pin A stays OFF
        val = 1023 - int(abs(power))
        coil_a.duty(1023)
        coil_b.duty(val)


# ================= MPU6050 =================
def init_mpu():
    global MPU_OK
    try:
        i2c.writeto_mem(MPU_ADDR, 0x6B, b"\x00")
        MPU_OK = True
        print("✅ MPU6050 ready")
    except:
        print("❌ MPU6050 not found")
        MPU_OK = False


def get_imu():
    if not MPU_OK:
        return 0.0, 0.0, 0.0
    try:
        data = i2c.readfrom_mem(MPU_ADDR, 0x3B, 6)
        ax, ay, az = struct.unpack(">hhh", data)
        # Calculate pitch/roll for detumbling logic of cubesat
        pitch = math.atan2(ay, math.sqrt(ax * ax + az * az)) * 57.3
        roll = math.atan2(-ax, az + 1) * 57.3
        return pitch, roll, 0.0
    except:
        return 0.0, 0.0, 0.0


# ================= BLE CLIENT =================
class SatelliteBLE:
    def __init__(self, ble, mqtt):
        self._ble = ble
        self.mqtt = mqtt
        self.conn = None
        self.start = None
        self.end = None
        self._ble.active(True)
        self._ble.irq(self.irq)
        self.remote_temp = 20.0
        self.remote_light = 500
        self.remote_vibe = 0
        self.remote_storm = False

    def scan(self):
        print("📡 BLE Scanning...")
        self._ble.gap_scan(0, 30000, 15000)

    def irq(self, event, data):
        if event == 5:  # SCAN_RESULT
            addr_type, addr, connectable, rssi, adv_data = data
            if rssi > -50:
                self._ble.gap_scan(None)
                self._ble.gap_connect(addr_type, addr, 20000)
        elif event == 7:  # CONNECT
            self.conn, addr_type, addr, *_ = data
            print("✅ BLE Link Physical established")
            time.sleep_ms(300)
            self._ble.gattc_discover_services(self.conn)
        elif event == 12:  # SERVICE_RESULT
            conn_handle, start, end, uuid = data
            if uuid == SERVICE_UUID:
                self.start, self.end = start, end
        elif event == 13:  # SERVICE_DONE
            if self.start:
                self._ble.gattc_discover_characteristics(
                    self.conn, self.start, self.end
                )
        elif event == 14:  # CHAR_RESULT
            conn_handle, def_handle, val_handle, props, uuid = data
            if uuid == CHAR_UUID:
                self._ble.gattc_write(conn_handle, val_handle + 1, b"\x01\x00", 1)
        elif event == 18:  # NOTIFY
            conn_handle, val_handle, data_bytes = data
            try:
                raw = data_bytes.decode().split(",")
                self.remote_temp = float(raw[0])
                self.remote_light = int(raw[1])
                self.remote_vibe = int(raw[2])
                self.remote_storm = int(raw[3]) == 1
            except:
                pass


# ================= NETWORK =================
def connect_wifi_mqtt():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.1)
    print("WiFi Connected")
    mqtt = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    mqtt.connect()
    print("MQTT Connected")
    return mqtt


# ================= MAIN =================
try:
    init_mpu()
    mqtt = connect_wifi_mqtt()
    ble_ctrl = bluetooth.BLE()
    sat = SatelliteBLE(ble_ctrl, mqtt)
    sat.scan()

    print("🚀 Magnetorquer Active on Pins 6 & 8")

    while True:
        # Get IMU data
        p, r, y = get_imu()

        # Simple active detumbling (Proportional Control)
        # Power is proportional to pitch angle
        torque_cmd = max(min(p * 12, 1023), -1023)
        set_torquer(torque_cmd)

        # Publish Telemetry
        msg = (
            '{"temp": %.1f, "light": %d, "vib": %d, "dust_storm": %s, '
            '"pitch": %.2f, "roll": %.2f, "yaw": %.2f, "torque": %d}'
            % (
                sat.remote_temp,
                sat.remote_light,
                sat.remote_vibe,
                "true" if sat.remote_storm else "false",
                p,
                r,
                y,
                torque_cmd,
            )
        )

        try:
            mqtt.publish(TOPIC, msg)
        except:
            print("MQTT Fail")

        time.sleep_ms(100)  # 10Hz control loop

except Exception as e:
    print("System error:", e)
    # SAFETY: Force Pins HIGH to turn H-Bridge OFF
    coil_a.duty(1023)
    coil_b.duty(1023)
    time.sleep(1)
    machine.reset()
