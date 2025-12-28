# Code to return light intensity measured by LDR sensor

import machine

class LDR:
    def __init__(self, pin=0):
        # ESP32-C6: ADC(0) is typically GPIO0
        self.adc = machine.ADC(machine.Pin(pin))
        # Set attenuation for full 0-3.3V range if needed
        self.adc.atten(machine.ADC.ATTN_11DB)

    def read(self):
        """Return raw analog value"""
        return self.adc.read()
