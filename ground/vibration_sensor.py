# Code to detect tremor using a tilt sensor, based on previous and current positions of the sensor

import machine
import time

class DigitalInterruptWindow:
    def __init__(self, pin, active_high=True, window_ms=1000):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.active_high = active_high
        self.window_ms = window_ms
        self.last_change_ms = time.ticks_ms()

        self.pin.irq(
            trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
            handler=self._irq_handler
        )
        self.current = self._read_pin()

    def _read_pin(self):
        val = self.pin.value()
        return bool(val) if self.active_high else not bool(val)

    def _irq_handler(self, pin):
        self.current = self._read_pin()
        self.last_change_ms = time.ticks_ms()

    def read(self):
        """Returns: current_state, was_changed_recently"""
        now = time.ticks_ms()
        recent = time.ticks_diff(now, self.last_change_ms) <= self.window_ms
        return self.current, recent
