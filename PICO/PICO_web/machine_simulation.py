# 用于本地仿真

gpio = {key:0 for key in range(30)}


class Pin:
    OUT = 1
    PULL_UP = 1
    gpio = {

    }
    def __init__(self, num, mode=0, pull=0):
        self.num = num
        self.mode = mode
        self.pull = pull

    def value(self, val=None):
        global gpio
        if val is not None:
            gpio[self.num] = val
        return gpio.get(self.num)


class wifi:
    @staticmethod
    def auto_connect():
        pass