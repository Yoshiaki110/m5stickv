// https://hellobreak.net/m5stickv-pwm-10-9/

'''
MG996Rなど一般的なサーボ
・周期：20[ms]、周波数：50[Hz]
・パルス幅：0.5～2.4[ms]
・Duty：2.5～12[%](パルス幅/周期×100)

'''
from machine import Timer,PWM
import lcd
import image
import time
import sys

FREQ = 20
PULSE_MIN = 0.5
PULSE_MAX = 2.4

lcd.init()
img = image.Image()

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=50, duty=2.5, pin=34)
arg = {-90:2.5, 0:7.25, 90:12}	# arg:duty

def setAngle(ang):
    diff = PULSE_MAX - PULSE_MIN
    pich = diff / 180
    pulse = ang * pich + PULSE_MIN
    duty = pulse / FREQ * 100
    print(duty)
    ch.duty(duty)

try:
    while True:
    ch.duty(arg[0])
    img.draw_string(60, 100, "arg 0", scale=3)
    lcd.display(img)
    time.sleep(1)
    img.clear()

    ch.duty(arg[-90])
    img.draw_string(60, 100, "arg -90", scale=3)
    lcd.display(img)
    time.sleep(1)
    img.clear()

    ch.duty(arg[0])
    img.draw_string(60, 100, "arg 0", scale=3)
    lcd.display(img)
    time.sleep(1)
    img.clear()

    ch.duty(arg[90])
    img.draw_string(60, 100, "arg +90", scale=3)
    lcd.display(img)
    time.sleep(1)
    img.clear()
except:
    lcd.clear()
    ch.deinit()
    sys.exit()
