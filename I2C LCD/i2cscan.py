import machine
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0,sda=sda,scl=scl, freq=400000)
print(i2c.scan())