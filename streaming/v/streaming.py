from machine import UART
from board import board_info
from fpioa_manager import fm
from Maix import GPIO
import sensor, lcd

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_vflip(1)
#sensor.set_hmirror(1)
sensor.run(1)
sensor.skip_frames(time = 2000)


fm.register(35, fm.fpioa.UART1_TX, force=True)
fm.register(34, fm.fpioa.UART1_RX, force=True)

uart = UART(UART.UART1, 115200,8,0,0, timeout=1000, read_buf_len=4096)



while(True):
    img = sensor.snapshot()
    lcd.display(img)
    buf = uart.readline()
    if buf and len(buf) == 3:
        print(buf)
        img_buf = img.compress(quality=50)
        sz = img_buf.size()
        img_size1 = (sz & 0xFF0000)>>16
        img_size2 = (sz & 0x00FF00)>>8
        img_size3 = (sz & 0x0000FF)>>0
        data_packet = bytearray([img_size1,img_size2,img_size3])
        uart.write(data_packet)
        uart.write(img_buf)
        data_packet = bytearray([0xAA,0x55,0xFF])
        uart.write(data_packet)

