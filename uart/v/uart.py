# Untitled - By: shts - 土 12 28 2019

import sensor, image, time
from fpioa_manager import fm
from machine import UART

# setup GPIO
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)

cnt = 0

'''
while(True):
    uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
    data_packet = "{} M5StickV : Hello World\n".format(cnt)
    uart_Port.write(data_packet)
    read_data = uart_Port.readline()
    print(read_data)
    time.sleep(1)
    cnt += 1
'''
while(True):
    uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
    read_data = uart_Port.readline()
    print(read_data)
    time.sleep(0.1)
