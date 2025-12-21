import machine

class LDR:
    def __init__(self, pin=0):
        # pin=0 → A0 on ESP8266
        self.adc = machine.ADC(pin)

    def read(self):
        """Return raw analog value (0–1023)"""
        return self.adc.read()


#from ldr import LDR
import uasyncio as asyncio

ldr = LDR()

async def main():
    while True:
        value = ldr.read()
        print("LDR:", value)
        await asyncio.sleep_ms(500)

asyncio.run(main())

