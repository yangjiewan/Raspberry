import machine
import ssd1306

i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
print("I2C设备号：" + str(i2c.scan()[0]))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.text("Raspberry Pi", 0, 0)
oled.text("Pico", 80, 10)
oled.text("MicroPython", 0, 20)
oled.text("OLED(ssd1306)", 0, 40)
oled.show()
