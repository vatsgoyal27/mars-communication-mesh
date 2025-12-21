import machine

class Microphone:
    def __init__(self, pin=3): # on gpio 3
        # pin=0 → A0 on ESP8266
        self.adc = machine.ADC(pin)

    def read(self):
        """Return raw analog value (0–1023)"""
        return self.adc.read()

#from mic import Microphone
import uasyncio as asyncio

mic = Microphone()

async def main():
    while True:
        print("Mic:", mic.read())
        await asyncio.sleep_ms(50)

asyncio.run(main())
