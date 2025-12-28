# Code for getting temperature from DHT sensor

import dht
import machine
import uasyncio as asyncio
import time

class AsyncDHT22:
    def __init__(self, pin_num, min_interval_ms=2000):
        self.sensor = dht.DHT22(machine.Pin(pin_num))
        self.min_interval = min_interval_ms
        self.last_read = 0
        self.temp = 22.0
        self.hum = 40.0

    async def read(self):
        """Polls the sensor respecting the hardware's 2s limit"""
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_read) < self.min_interval:
            return self.temp, self.hum

        try:
            self.sensor.measure()
            self.temp = self.sensor.temperature()
            self.hum = self.sensor.humidity()
            self.last_read = now
        except Exception:
            pass # Return last known good values on failure
        
        return self.temp, self.hum
