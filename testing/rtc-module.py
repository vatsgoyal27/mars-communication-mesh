# Testing RTC Module code

import machine
import pcf8563

class RTC:
    def __init__(self, scl=5, sda=4):
        self.i2c = machine.I2C(
            scl=machine.Pin(scl),
            sda=machine.Pin(sda)
        )
        self.rtc = pcf8563.PCF8563(self.i2c)

    def now(self):
        """
        Returns:
        (year, month, day, weekday, hour, minute, second)
        """
        return self.rtc.datetime()

    def set(self, dt):
        """
        dt = (year, month, day, weekday, hour, minute, second)
        """
        self.rtc.datetime(dt)
