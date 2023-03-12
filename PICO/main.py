"""
PICO 测试用例
运行的main.py要运行在根目录下。  main.py -> main.py
C:\Users\Carter\AppData\Local\Programs\Python\Python39\python.exe C:\Users\Carter\AppData\Roaming\JetBrains\PyCharm2021.2\plugins\intellij-micropython/scripts/microupload.py -C C:/Users/Carter/Desktop/Raspberry/PICO -v COM4 C:/Users/Carter/Desktop/Raspberry/PICO
"""

import machine
import utime

import network
import urequests

def blink_io(pin, frequency):
    """设置io口闪烁, 板载LED为’LED‘"""
    machine_pin = machine.Pin(pin, machine.Pin.OUT)
    sleep_time = 1.0 / frequency

    machine_pin.value(1)
    utime.sleep(sleep_time)

    machine_pin.value(0)
    utime.sleep(sleep_time)


class WifiClass:
    def __init__(self):
        self.mac_address = "28:CD:C1:08:91:5F"

    @staticmethod
    def get_wifi():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        access_points = wlan.scan()
        for ap in access_points:
            print(ap)

    @staticmethod
    def get_mac():
        # 本机 MAC 地址:28:cd:c1:08:91:5f
        # 本机 MAC 地址:28:CD:C1:08:91:5F
        import ubinascii

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
        print(f"MAC: {mac}")

    @staticmethod
    def link_wifi(ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            utime.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print('ip = ' + status[0])


WifiClass.get_mac()
WifiClass.get_wifi()

ssid = 'HUAWEI-123'
password = 'abcd1234'
WifiClass.link_wifi(ssid, password)

# 发起网络请求
r = urequests.get('http://api.seniverse.com/v3/weather/now.json?key=SwwwfskBjB6fHVRon&location=nanjing&language=en&unit=c')
print(r.content)
r.close()
# b'{"results":[{"location":{"id":"WTSQQYHVQ973","name":"Nanjing","country":"CN","path":"Nanjing,Nanjing,Jiangsu,China","timezone":"Asia/Shanghai
# ","timezone_offset":"+08:00"},"now":{"text":"Sunny","code":"0","temperature":"14"},"last_update":"2023-03-03T17:14:28+08:00"}]}'


from machine import RTC
from machine import Pin
from machine import I2C
from adafruit_ssd1306 import SSD1306_I2C
from machine import Timer
# import dht
#
#
# def clock_time(tim):
#     timee = clockk.datetime()
#     oled.fill(0)
#     oled.text("Date:", 0, 0)
#     oled.text(str(timee[0]) + '-' + str(timee[1]) + '-' + str(timee[2]) + '-' + week[timee[3]], 0, 10)
#     oled.text(str(timee[4]) + '-' + str(timee[5]) + '-' + str(timee[6]), 0, 20)
#
#     d.measure()
#     oled.text("Temperature:" + str(d.temperature()) + 'C', 0, 40)
#     oled.text("Humidity:" + str(d.humidity()) + '%', 0, 50)
#
#     oled.show()
#
#
# i2c = I2C(1, sda=Pin(2), scl=Pin(3))
# oled = SSD1306_I2C(128, 64, i2c, addr=0X3c)
#
# week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
# clockk = RTC()
# # clockk.datetime((2022,10,30,6,17,25,0,0))#设置初始时间，年、月、日、星期、时、分、秒
#
# d = dht.DHT11(Pin(0))

# tim = Timer(-1)
# tim.init(period=300, mode=Timer.PERIODIC, callback=clock_time)

# oled.text("Date:", 0, 0)

#
# from machine import Pin, I2C
# from ssd1306 import SSD1306_I2C
# import time
#
# addr = 0x3c  # 60
# i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
# oled = SSD1306_I2C(128, 64, i2c, addr)
#
#
# # print(i2c.scan())  #60
#
# class chinese:
#     chinese = [
#         0x00, 0x20, 0x20, 0x20, 0x20, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0x40, 0x20, 0x10, 0x08, 0x00, 0x00,
#         0x20, 0x60, 0x20, 0x10, 0x10, 0xFF, 0x00, 0x00, 0x00, 0x3F, 0x40, 0x40, 0x40, 0x40, 0x78, 0x00,  # 北,0
#
#         0x04, 0x04, 0x04, 0xE4, 0x24, 0x24, 0x25, 0x26, 0x24, 0x24, 0x24, 0xE4, 0x04, 0x04, 0x04, 0x00,
#         0x00, 0x40, 0x20, 0x1B, 0x02, 0x42, 0x82, 0x7E, 0x02, 0x02, 0x02, 0x0B, 0x10, 0x60, 0x00, 0x00,  # 京,1
#
#         0x04, 0x24, 0x44, 0x84, 0x64, 0x9C, 0x40, 0x30, 0x0F, 0xC8, 0x08, 0x08, 0x28, 0x18, 0x00, 0x00,
#         0x10, 0x08, 0x06, 0x01, 0x82, 0x4C, 0x20, 0x18, 0x06, 0x01, 0x06, 0x18, 0x20, 0x40, 0x80, 0x00,  # 欢,2
#
#         0x40, 0x40, 0x42, 0xCC, 0x00, 0x00, 0xFC, 0x04, 0x02, 0x00, 0xFC, 0x04, 0x04, 0xFC, 0x00, 0x00,
#         0x00, 0x40, 0x20, 0x1F, 0x20, 0x40, 0x4F, 0x44, 0x42, 0x40, 0x7F, 0x42, 0x44, 0x43, 0x40, 0x00,  # 迎,3
#
#         0x00, 0x80, 0x60, 0xF8, 0x07, 0x40, 0x20, 0x18, 0x0F, 0x08, 0xC8, 0x08, 0x08, 0x28, 0x18, 0x00,
#         0x01, 0x00, 0x00, 0xFF, 0x00, 0x10, 0x0C, 0x03, 0x40, 0x80, 0x7F, 0x00, 0x01, 0x06, 0x18, 0x00,  # 你,4
#     ]
#
#
# def ByteOpera(num, dat):
#     byte = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
#     if dat & byte[num]:
#         return 1
#     else:
#         return 0
#
#
# def LedShowCH_16x16(n, x_axis, y_axis):
#     for i in range(2):
#         for a in range(16):
#             for b in range(8):
#                 if (ByteOpera(b, chinese.chinese[n * 32 + i * 16 + a])):
#                     oled.pixel(x_axis + a, y_axis + i * 8 + b, 1)
#                 else:
#                     oled.pixel(x_axis + a, y_axis + i * 8 + b, 0)
#
#
# def main():
#     oled.fill(0)
#     for i in range(0, 5, 1):
#         LedShowCH_16x16(i, i * 16, 16)
#         # oled.text("Hi",24,28)
#     oled.show()
#
#
# if __name__ == "__main__":
#     main()
#
while True:
    blink_io("LED", 2)
#
# from machine import Pin, I2C
# # from time import sleep
# # import ssd1306   #引用了ssd1306.py
# i2c0 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
#
# i2c1 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
#
# i2c1 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
# i2c1.scan()
# i2c1.writeto(76, b'123')
# i2c1.readfrom(76, 4)
#
# i2c0 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
# i2c0.scan()
# i2c0.writeto_mem(76, 6, b'456')
# i2c0.readfrom_mem(76, 6, 4)



#
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
#
# oled.text('Hello, World 1!', 0, 0)
# oled.text('Hello, World 2!', 0, 10)
# oled.text('Hello, World 3!', 0, 20)
#
# oled.show()

