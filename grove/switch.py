# touchセンサーは使えたけど、buttonスイッチはボタンを押すと電源が落ちる
# force=TrueとGPIO.PULL_UPなくても動く

import utime
from Maix import GPIO
from fpioa_manager import fm

fm.register(34, fm.fpioa.GPIOHS0, force=True)
p34=GPIO(GPIO.GPIOHS0,GPIO.IN, GPIO.PULL_UP)

while True:
    print(p34.value())
    utime.sleep_ms(100)
