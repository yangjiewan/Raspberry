import network
import json
import time

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
            time.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print('ip = ' + status[0])


def auto_connect():
    """通过读取config.json文件的WIFI字段，自动连接WIFI, 成功返回True, 失败False"""
    config_path = "PICO_web/templates/config.json"
    config_info = {}
    with open(config_path, "r", encoding="UTF-8") as file:
        config_info = json.load(file)

    wifi_list = config_info.get("WIFI", [])
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for wifi in wifi_list:
        ssid = wifi.get("ssid")
        password = wifi.get("password")
        wlan.connect(ssid, password)

        timeout = 5  # 设置最长等待连接时间为 5 秒
        while timeout > 0:
            if wlan.status() < 0 or wlan.status() >= 3:  # 如果WiFi连接成功或者失败
                break  # 跳出循环
            timeout -= 1
            time.sleep(1)  # 延时1秒

        if wlan.status() == 3:  # 如果WiFi连接成功
            status = wlan.ifconfig()
            print('ip = ' + status[0])
            return True
    return False

