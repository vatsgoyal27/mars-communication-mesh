from machine import I2C
import struct

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

        # Wake up MPU6050
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def _read(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 14)
        return struct.unpack('>hhhhhhh', data)

    def get_accel(self):
        ax, ay, az, _, _, _, _ = self._read(0x3B)
        return ax/16384, ay/16384, az/16384

    def get_gyro(self):
        _, _, _, gx, gy, gz, _ = self._read(0x3B)
        return gx/131, gy/131, gz/131

    def get_temp(self):
        _, _, _, _, _, _, temp = self._read(0x3B)
        return temp / 340 + 36.53

