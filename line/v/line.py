## This Source is M5StickV MaixPy
import network, socket, time, sensor, image,lcd
from Maix import GPIO
from fpioa_manager import fm, board_info
from machine import UART

#M5StickV Camera Start
clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(time = 2000)
#M5StickV GPIO_UART
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
#M5StickV ButtonA
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
while True:
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img)
#   IF Button A Push Then Image Send UART
    if but_a.value() == 0:
        print('shutter!!')
        img_buf = img.compress(quality=70)
        img_size1 = (img.size()& 0xFF0000)>>16
        img_size2 = (img.size()& 0x00FF00)>>8
        img_size3 = (img.size()& 0x0000FF)>>0
        data_packet = bytearray([0xFF,0xD8,0xEA,0x01,img_size1,img_size2,img_size3,0x00,0x00,0x00])
        uart_Port.write(data_packet)
        uart_Port.write(img_buf)
        time.sleep(1.0)
#   Send UART End
uart_Port.deinit()
del uart_Port
print("finish")
