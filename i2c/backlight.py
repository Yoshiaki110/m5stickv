# https://gist.github.com/Shinichi-Ohki/a87eaf8383cccbfd9312dd702c12de1d

# M5stickVのバックライトを制御する
import lcd  #for test
from machine import I2C

i2c = I2C(I2C.I2C0, freq=400000, scl=28, sda=29)

lcd.init()                                                     #for test
lcd.draw_string(100, 100, "hello maixpy", lcd.RED, lcd.BLACK)  #for test

i2c.writeto_mem(0x34, 0x91,b'\x70')  # minimum
i2c.writeto_mem(0x34, 0x91,b'\xf0')  # maximum
