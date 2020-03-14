import utime
from Maix import GPIO
from fpioa_manager import fm

fm.register(34, fm.fpioa.GPIOHS0)
p34=GPIO(GPIO.GPIOHS0,GPIO.OUT)

while True:
   p34.value(0)
   utime.sleep_ms(1000)
   p34.value(1)
   utime.sleep_ms(1000)
