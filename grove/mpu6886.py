# https://riscv.love/025

'''
    MPU6886 Class - 6 Axis acc sensor class (for test)
'''

import sys
import time
from machine import I2C
from Maix import GPIO
from fpioa_manager import *

class MPU6886_Class:
    ADDRESS = 0x68

    WHOAMI           = 0x75
    ACCEL_INTEL_CTRL = 0x69
    SMPLRT_DIV       = 0x19
    INT_PIN_CFG      = 0x37
    INT_ENABLE       = 0x38
    ACCEL_XOUT_H     = 0x3B
    TEMP_OUT_H       = 0x41
    GYRO_XOUT_H      = 0x43
    USER_CTRL        = 0x6A
    PWR_MGMT_1       = 0x6B
    PWR_MGMT_2       = 0x6C
    CONFIG           = 0x1A
    GYRO_CONFIG      = 0x1B
    ACCEL_CONFIG     = 0x1C
    ACCEL_CONFIG2    = 0x1D
    FIFO_EN          = 0x23

    global i2c
    global aRes
    global gRes

    def __init__(self):
        global i2c
        global aRes
        global gRes

        i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER, scl=board_info.MPU_SCL, sda=board_info.MPU_SDA, freq=400000)
        devices = i2c.scan()
        time.sleep_ms(10)

        if self.ADDRESS in devices:
            pass
        else:
            print("Illegal hardware")
            sys.exit()

        whoami = i2c.readfrom_mem(self.ADDRESS, self.WHOAMI, 1)
        # time.sleep_ms(10)
        if whoami != b'\x19':
            print("Device not found")
            sys.exit()

        # Set MPU6886 Power Management
        i2c.writeto_mem(self.ADDRESS, self.PWR_MGMT_1, bytearray([0x00]))
        time.sleep_ms(10)
        i2c.writeto_mem(self.ADDRESS, self.PWR_MGMT_1, bytearray([0x01<<7]))
        time.sleep_ms(10)
        i2c.writeto_mem(self.ADDRESS, self.PWR_MGMT_1, bytearray([0x01<<0]))
        time.sleep_ms(10)

        # Initialize all settings
        i2c.writeto_mem(self.ADDRESS, self.ACCEL_CONFIG, bytearray([0x10]))
        i2c.writeto_mem(self.ADDRESS, self.GYRO_CONFIG, bytearray([0x18]))
        i2c.writeto_mem(self.ADDRESS, self.CONFIG, bytearray([0x01]))
        i2c.writeto_mem(self.ADDRESS, self.SMPLRT_DIV, bytearray([0x05]))
        i2c.writeto_mem(self.ADDRESS, self.INT_ENABLE, bytearray([0x00]))
        i2c.writeto_mem(self.ADDRESS, self.ACCEL_CONFIG2, bytearray([0x00]))
        i2c.writeto_mem(self.ADDRESS, self.USER_CTRL, bytearray([0x00]))
        i2c.writeto_mem(self.ADDRESS, self.FIFO_EN, bytearray([0x00]))
        i2c.writeto_mem(self.ADDRESS, self.INT_PIN_CFG, bytearray([0x22]))
        i2c.writeto_mem(self.ADDRESS, self.INT_ENABLE, bytearray([0x01]))
        time.sleep_ms(100)

        # Setting rate
        self.aRes = 8.0 / 32768
        self.gRes = 2000 / 32768


    def get_accel(self):
        accel = i2c.readfrom_mem(self.ADDRESS, self.ACCEL_XOUT_H, 6)

        accel_x = (accel[0]<<8) | accel[1]
        if accel_x > 32768:
            accel_x -= 65536
        accel_y = (accel[2]<<8) | accel[3]
        if accel_y > 32768:
            accel_y -= 65536
        accel_z = (accel[4]<<8) | accel[5]
        if accel_z > 32768:
            accel_z -= 65536

        return [accel_x*self.aRes, accel_y*self.aRes, accel_z*self.aRes]


    def get_gyro(self):
        gyro = i2c.readfrom_mem(self.ADDRESS, self.GYRO_XOUT_H, 6)

        gyro_x = (gyro[0]<<8) | gyro[1]
        if gyro_x > 32768:
            gyro_x -= 65536
        gyro_y = (gyro[2]<<8) | gyro[3]
        if gyro_y > 32768:
            gyro_y -= 65536
        gyro_z = (gyro[4]<<8) | gyro[5]
        if gyro_z > 32768:
            gyro_z -= 65536

        return [gyro_x*self.gRes, gyro_y*self.gRes, gyro_z*self.gRes]


    def get_temp(self):
        temp = i2c.readfrom_mem(self.ADDRESS, self.TEMP_OUT_H, 2)
        return ((temp[0]<<8) | temp[1]) / 326.8


global mpu6886
mpu6886=MPU6886_Class()

if __name__=="__main__":
    import lcd
    lcd.init()
    lcd.rotation(2)
    lcd.draw_string(10, 10, "MPU6886 test", lcd.WHITE)
    while True:
        ax, ay, az = mpu6886.get_accel()
        gx, gy, gz = mpu6886.get_gyro()
        tmp = mpu6886.get_temp()

        lcd.draw_string(30, 24, "aX = %.2f[G]  "%(ax), lcd.WHITE)
        lcd.draw_string(30, 38, "aY = %.2f[G]  "%(ay), lcd.WHITE)
        lcd.draw_string(30, 52, "aZ = %.2f[G]  "%(az), lcd.WHITE)

        lcd.draw_string(30, 70, "gX = %.2f[deg/s]  "%(gx), lcd.WHITE)
        lcd.draw_string(30, 84, "gY = %.2f[deg/s]  "%(gy), lcd.WHITE)
        lcd.draw_string(30, 98, "gZ = %.2f[deg/s]  "%(gz), lcd.WHITE)

        lcd.draw_string(30,116, "Temp = %.1f[rise]  "%(tmp), lcd.WHITE)

        time.sleep_ms(100)
