import dht
import machine
import uasyncio as asyncio
import time

sensor = dht.DHT22(machine.Pin(9))

class AsyncDHT22:
    def __init__(self, sensor, min_interval_ms=2000):
        self.sensor = sensor
        self.min_interval = min_interval_ms
        self.last_read = 0

    async def read(self):
        now = time.ticks_ms()

        # Respect DHT22 minimum read interval
        if time.ticks_diff(now, self.last_read) < self.min_interval:
            return None

        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()

            # Validate ranges
            if -40 < temp < 80 and 0 <= hum <= 100:
                self.last_read = now
                return temp, hum

        except Exception:
            pass

        return None
    
async def dht_task(dht_reader):
    while True:
        data = await dht_reader.read()
        if data:
            t, h = data
            print("Temperature:", t, "°C")
            print("Humidity:", h, "%")

        # Yield control (non-blocking)
        await asyncio.sleep_ms(100)

async def main():
    dht_reader = AsyncDHT22(sensor)
    await dht_task(dht_reader)

asyncio.run(main())


