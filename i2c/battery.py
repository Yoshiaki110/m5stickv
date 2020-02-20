# https://gist.github.com/Shinichi-Ohki/b113b3d7b90cfb0aa52b97b955127542

# M5StickVのバッテリ電圧と放電電流を取得
import lcd
import utime
import sys
from machine import I2C
from Maix import GPIO
from fpioa_manager import *

i2c = I2C(I2C.I2C0, freq=400000, scl=28, sda=29)
# And a short delay to wait until the I2C port has finished activating.
utime.sleep_ms(100)

fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP) #PULL_UP is required here!

lcd.init()
i2c.writeto_mem(0x34, 0x82,b'\xff')  # all ADC eneble
i2c.writeto_mem(0x34, 0xb8, b'\x80')  # Coulomb counter eneble
i2c.writeto_mem(0x34, 0x91, b'\xa0')  # LCD Backlight

while 1:
    if but_a.value() == 0: #If dont want to run the demo
        sys.exit()

    buf = int.from_bytes(i2c.readfrom_mem(0x34, 0x78, 1), 'big')
    buf2 = int.from_bytes(i2c.readfrom_mem(0x34, 0x79, 1), 'big')
    lcd.draw_string(0, 0, "Battery Voltage " +
                    str(((buf << 4)+buf2)*1.4)+" mV", lcd.RED, lcd.BLACK)
    buf = int.from_bytes(i2c.readfrom_mem(0x34, 0x7c, 1), 'big')
    buf2 = int.from_bytes(i2c.readfrom_mem(0x34, 0x7d, 1), 'big')
    lcd.draw_string(0, 16, "Battery discharge " +
                    str(((buf << 5)+buf2)*0.5)+" mA", lcd.GREEN, lcd.BLACK)

    """
    buf1 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb0, 1), 'big')
    buf2 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb1, 1), 'big')
    buf3 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb2, 1), 'big')
    buf4 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb3, 1), 'big')
    coin = ((buf1 << 24)+(buf2 << 16)+(buf3 << 8)+buf4)
    lcd.draw_string(0, 32, "Battery charge "+str(coin*0.5) +
                    " mAh", lcd.BLUE, lcd.BLACK)
    buf1 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb4, 1), 'big')
    buf2 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb5, 1), 'big')
    buf3 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb6, 1), 'big')
    buf4 = int.from_bytes(i2c.readfrom_mem(0x34, 0xb7, 1), 'big')
    coout = ((buf1 << 24)+(buf2 << 16)+(buf3 << 8)+buf4)
    lcd.draw_string(0, 48, "Battery discharge " +
                    str(coout*0.5)+" mAh", lcd.BLUE, lcd.BLACK)
    ccc = (coin - coout) * 65536 * 0.5 / 3600 / 25
    lcd.draw_string(0, 64, "Battery charge "+str(ccc)+" mAh", lcd.WHITE, lcd.BLACK)
    """
    utime.sleep(1)
