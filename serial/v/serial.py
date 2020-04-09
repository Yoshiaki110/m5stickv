# Untitled - By: yoshi - 木 2 20 2020

import sensor, image, time
from fpioa_manager import fm, board_info
from machine import UART
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

i = 0
while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
    #data_packet = bytearray([0x41,0x42,0x43,0x44,0x45])
    data_packet = bytearray([0xFF,0xAA])
    data_packet.append(i % 256)
    uart_Port.write(data_packet)
    i += 1
    time.sleep(1)
