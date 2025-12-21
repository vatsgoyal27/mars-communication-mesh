import machine
import uasyncio as asyncio

class IRDigital:
    def __init__(self, pin, active_low=True):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.active_low = active_low
        self.state = False

    async def run(self):
        while True:
            val = self.pin.value()
            self.state = (not val) if self.active_low else bool(val)

            # yield to event loop
            await asyncio.sleep_ms(1)

    def read(self):
        return self.state
    
import uasyncio as asyncio
#from ir_digital import IRDigital

ir = IRDigital(pin=1)  # GPIO4 = D2

async def main():
    asyncio.create_task(ir.run())

    while True:
        if ir.read():
            print("Object detected")
        else:
            print("No object")

        await asyncio.sleep_ms(100)

asyncio.run(main())

