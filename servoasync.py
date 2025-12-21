import machine
import uasyncio as asyncio

class AsyncServo:
    def __init__(
        self,
        pin,
        min_duty=40,
        max_duty=115,
        min_angle=0,
        max_angle=180,
        damping=0.15,
        update_ms=20
    ):
        self.pwm = machine.PWM(machine.Pin(pin), freq=50)
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.damping = damping
        self.update_ms = update_ms

        self.current_angle = 90
        self.target_angle = 90

        self._apply(self.current_angle)

    def _angle_to_duty(self, angle):
        angle = max(self.min_angle, min(self.max_angle, angle))
        return int(
            self.min_duty +
            (angle - self.min_angle)
            * (self.max_duty - self.min_duty)
            / (self.max_angle - self.min_angle)
        )

    def _apply(self, angle):
        self.pwm.duty(self._angle_to_duty(angle))

    def set_target(self, angle):
        self.target_angle = max(self.min_angle, min(self.max_angle, angle))

    async def run(self):
        while True:
            # Damping (exponential smoothing)
            delta = self.target_angle - self.current_angle
            self.current_angle += delta * self.damping

            self._apply(self.current_angle)

            await asyncio.sleep_ms(self.update_ms)
            
            
servo = AsyncServo(pin=3)  # GPIO14 = D5

async def servo_test():
    while True:
        servo.set_target(0)
        await asyncio.sleep(2)
        servo.set_target(90)
        await asyncio.sleep(2)
        servo.set_target(180)
        await asyncio.sleep(2)

async def main():
    asyncio.create_task(servo.run())
    await servo_test()

asyncio.run(main())


