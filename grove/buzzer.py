# https://hrkz.tokyo/m5stickv-grove/

# ブザーを鳴らす
from fpioa_manager import *
from Maix import GPIO
import utime

fm.register(34, fm.fpioa.GPIO0)
buzzer = GPIO(GPIO.GPIO0, GPIO.OUT)

while True:
    buzzer.value(1)
    utime.sleep(0.1)
    buzzer.value(0)
    utime.sleep(0.9)
