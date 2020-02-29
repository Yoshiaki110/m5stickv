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

uart = UART(UART.UART1, 9600,8,0,0, timeout=1000, read_buf_len=4096)



while(True):
    img = sensor.snapshot()
    lcd.display(img)
    print("image size1:" + str(img.size()))
    img_buf = img.compress(quality=50)
    print("image size2:" + str(img_buf.size()))
    sz = 879
    img_size1 = (sz & 0xFF0000)>>16
    img_size2 = (sz & 0x00FF00)>>8
    img_size3 = (sz & 0x0000FF)>>0
    print(">" + str(img.size()) + ":"+ str(img_buf.size()) + " " + str(img_size1) + "-" + str(img_size2) + "-" + str(img_size3))
    data_packet = bytearray([0xFF,0xD8,0xEA,0x01,0x00,0x00,0x00,img_size1,img_size2,img_size3])

    uart.write(data_packet)
    #uart.write(img_buf)
    #for d in img_buf:
    #    uart.write(d)
    #img.save("/sd/img.bmp")    #SDカードに保存
    #img_buf.save("/sd/img_buf.bmp")    #SDカードに保存
    #img.save("/sd/img.jpg")    #SDカードに保存
    #img_buf.save("/sd/img_buf.jpg")    #SDカードに保存
    with open('/sd/test02.jpg', 'rb') as f:
        i = 0
        while True:
            d = f.read(1)
            if len(d) == 0:
                break
            print('%d / %d (%x) ' % (i+1, img.size(), ord(d)))
            uart.write(d)
            i += 1
    time.sleep(5)

