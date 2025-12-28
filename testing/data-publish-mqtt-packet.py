# Sample testing code for publishing data to MQTT over Wifi
# File also includes packeting function to make the sensor data into a packet that can be pushed

import network
import time
from umqtt.simple import MQTTClient
import machine

# ================= WiFi =================
SSID = "ADD_SSID_HERE"
PASSWORD = "ADD_PASSWORD_HERE"

# ================= MQTT =================
MQTT_BROKER = "ADD_YOUR_IP_HERE"
MQTT_PORT = 1883
TOPIC = b"mars/telemetry"  # Type in same topic you are retreiving data from
CLIENT_ID = b"esp32c3_team18"

# ================= LED (optional) =================
led = machine.Pin(8, machine.Pin.OUT)


# ================= WiFi Connect =================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")

    print("\nWiFi connected")
    print("IP:", wlan.ifconfig()[0])
    led.on()


# ================= MQTT Connect =================
def connect_mqtt():
    print("Connecting to MQTT...")
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=60)
    client.connect()
    print("MQTT connected")
    return client


# ================= Main =================
connect_wifi()
mqtt = connect_mqtt()

counter = 0


# Function to format sensor data into a packet
def format_sensor_data(temp, light, vibe, ir_storm, pitch, roll, yaw):
    data = (
        '{"temp": %.1f, "light": %d, "vibe": %d, '
        '"ir_storm": %s, "pitch": %.2f, "roll": %.2f, "yaw": %.2f}'
        % (
            temp / 10,
            light,
            vibe,
            "true" if ir_storm else "false",
            pitch / 100,
            roll / 100,
            yaw / 100,
        )
    )
    return data


while True:
    try:
        # Sample msg
        msg = str(format_sensor_data(counter, 100, 1, 1, 3, 1, 3))

        print("Publishing:", msg)
        mqtt.publish(TOPIC, msg)
        counter += 1
        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        led.off()
        time.sleep(3)
        machine.reset()
