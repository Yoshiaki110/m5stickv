// https://hellobreak.net/m5stickv-pwm-10-9/

from machine import Timer,PWM
import lcd
import image
import time
import sys

lcd.init()
img = image.Image()

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=50, duty=2.5, pin=34)
arg = {-90:2.5, 0:7.25, 90:12}	# arg:duty

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
