# https://hrkz.tokyo/m5stickv-grove/

# PWM出力でブザーを鳴らす
from machine import Timer,PWM
from fpioa_manager import *
from Maix import GPIO
import utime

fm.register(34, fm.fpioa.GPIO0)
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=440, duty=1, pin=34)

freq = 0
loop = 0
dir = True

while True:
    if dir:
        freq += 1
    else:
        freq -= 1

    if freq>440:
        frew = 440
        dir = False
    elif freq<262:
        freq = 262
        dir = True
        loop += 1

    time.sleep(0.01)
    ch.freq(freq)
    if loop>1:
        ch.disable()
