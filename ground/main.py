# Main code file for ground station


import bluetooth
import time
import machine
import uasyncio as asyncio
import bluetooth
from ble_advertising import advertising_payload
from micropython import const

# --- SENSOR IMPORTS ---
from ldr import LDR
from vibration_sensor import DigitalInterruptWindow
from dhtasync import AsyncDHT22
from ir_digital import IRDigital

# --- SERVO CLASS ---


class AsyncServo:
    def __init__(self, pin, min_duty=40, max_duty=115, damping=0.15):
        self.pwm = machine.PWM(machine.Pin(pin), freq=50)
        self.min_duty, self.max_duty = 40, 115
        self.damping = damping
        self.current_angle = 90
        self.target_angle = 90

    def _apply(self, angle):
        duty = int(40 + (angle/180) * (115-40))
        self.pwm.duty(duty)

    def set_target(self, angle):
        self.target_angle = angle

    async def run(self):
        while True:
            self.current_angle += (self.target_angle - self.current_angle) * self.damping
            self._apply(self.current_angle)
            await asyncio.sleep_ms(20)

# --- BLE SETUP ---

# Same IDs as satellite
_SERVICE_UUID = bluetooth.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
_CHAR_UUID = bluetooth.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

class BLEGroundStation:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        ((self._handle,),) = self._ble.gatts_register_services([(_SERVICE_UUID, [(_CHAR_UUID, bluetooth.FLAG_NOTIFY),])])
        self._connections = set()
        self._ble.irq(self._irq)
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            self._connections.add(data[0])
            print("✅ CONNECTED")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            self._connections.discard(data[0])
            self._advertise()

    def _advertise(self):
        p = advertising_payload(name="MARS_C6", services=[_SERVICE_UUID])
        self._ble.gap_advertise(100_000, p)

    def send_data(self, data_str):
        if not self._connections: return
        self._ble.gatts_write(self._handle, data_str.encode())
        for c in self._connections: self._ble.gatts_notify(c, self._handle)

# --- HARDWARE INSTANCES ---
ldr = LDR(pin=0)
vibration = DigitalInterruptWindow(pin=2) # GPIO2
dht_reader = AsyncDHT22(pin_num=9)       # GPIO9
ir = IRDigital(pin=1)                     # GPIO1
servo_az = AsyncServo(pin=18)              # GPIO18
servo_alt = AsyncServo(pin=19)             # GPIO19

# Sample servo rotation, can be integrated with orbit propagator, and antenna values
async def antenna_sweep():
    """Triggers the servos to oscillate independently"""
    while True:
        servo_az.set_target(30); servo_alt.set_target(45)
        await asyncio.sleep(3)
        servo_az.set_target(150); servo_alt.set_target(90)
        await asyncio.sleep(3)

async def main_task(station):
    # START ALL BACKGROUND TASKS
    asyncio.create_task(ir.run())
    asyncio.create_task(servo_az.run())
    asyncio.create_task(servo_alt.run())
    asyncio.create_task(antenna_sweep())
    
    while True:
        temp, hum = await dht_reader.read()
        light = ldr.read()
        _, vib_recent = vibration.read()
        ir_obj = ir.read()
        
        # Dust storm is detected if IR detects dust, and light intensity is below a threshold value
        storm = 1 if (ir_obj and light < 300) else 0

        # FULL LOGGING TO CONSOLE
        print(f"\n--- TELEMETRY ---")
        print(f"TEMP: {temp}C | LDR: {light}")
        print(f"VIB: {vib_recent} | IR: {ir_obj} | STORM: {storm}")
        print(f"SERVOS: Az={servo_az.current_angle:.1f} Alt={servo_alt.current_angle:.1f}")

        station.send_data(f"{temp},{light},{1 if vib_recent else 0},{storm}")
        await asyncio.sleep(1)

# --- EXECUTION ---
station = BLEGroundStation(bluetooth.BLE())
asyncio.run(main_task(station))
