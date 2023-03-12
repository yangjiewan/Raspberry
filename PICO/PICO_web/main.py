import time
import os

if os.getcwd() == "/":
    import machine
    import wifi
else:
    from machine_simulation import *

from web_socket import SocketClass


def blink_io(pin, frequency):
    """设置io口闪烁, 板载LED为’LED‘"""
    machine_pin = machine.Pin(pin, machine.Pin.OUT)
    sleep_time = 1.0 / frequency

    machine_pin.value(1)
    time.sleep(sleep_time)

    machine_pin.value(0)
    time.sleep(sleep_time)


def main():
    # 点亮开机启动灯
    print("开机")
    # 点亮wifi连接指数灯
    if wifi.auto_connect():
        blink_io(0, 1)

    socket_obj = SocketClass()
    socket_obj.start()
    socket_obj.work()

    # 心跳指示灯
    #

if __name__ == '__main__':
    main()
