from machine import I2C
i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
device = i2c.scan()
print(device)
