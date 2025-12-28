# Use IR sensor to detect dust storm based on visibility

import machine
import uasyncio as asyncio

class IRDigital:
    def __init__(self, pin, active_low=True):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.active_low = active_low
        self.state = False

    async def run(self):
        """Background task to poll the sensor"""
        while True:
            val = self.pin.value()
            self.state = (not val) if self.active_low else bool(val)
            # Yield control to allow other tasks to run
            await asyncio.sleep_ms(10)

    def read(self):
        return self.state
