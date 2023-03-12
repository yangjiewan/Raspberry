import socket
import sys
import json
import time

import traceback


class SocketClass:

    def __init__(self):
        # self.host = "127.0.0.1"
        self.host = "0.0.0.0"
        # self.host = "localhost"
        self.port = 80

        self.is_start = False
        self.max_thread = 16

        self.thread_count_ = 0
        self.route_handlers = {
            "POST": {
                "/set": self.set,
                "/check_login": self.check_login,
                "/reset": self.reset,
                "/run": self.run,
                "/set_gpio": self.set_gpio
            },
            "GET": {
                "/home": self.get_home,
                "/debug": self.debug,
                "/gpio": self.get_gpio,
                "/favicon.ico": self.favicon,
                "/login": self.get_login,
                "/instructions": self.instructions
            }
        }

    def set_gpio(self, **msg):
        print(msg)
        res_info = {
            "status_code": "1",
            "gpio_number": msg.get("gpio_num"),
            "data": msg.get("status")
        }
        self.headers.send(json.dumps(res_info).encode())

    def debug(self, **msg):
        gpio_button_element = """
        <tr>
            <td>
                <div class="btn-on" onclick="change_gpio(this, gpio_namber)">
                    <label class="btn-on-circle"></label>
                    <label class="btn-on-text">关</label>
                </div>
            </td>
            <td>
                <span>gpio_info</span>
            </td>
            <td>
                <div class="btn-on" onclick="change_gpio(this, gpio_namber)">
                    <label class="btn-on-circle"></label>
                    <label class="btn-on-text">关</label>
                </div>
            </td>
            <td>
                <span>gpio_info</span>
            </td>
        </tr>
        """

        config_path = "templates/config.json"
        config_info = {}
        with open(config_path, "r", encoding="UTF-8") as file:
            config_info = json.load(file)

        gpio_info = config_info.get("GPIO", {})
        gpio_button = ""
        for key, value in gpio_info.items():
            if "gpio_namber" in gpio_button:
                gpio_button = gpio_button.replace("gpio_namber", key, 1).replace("gpio_info", value, 1)
            else:
                gpio_button += gpio_button_element.replace("gpio_namber", key, 1).replace("gpio_info", value, 1)

        replace_info = {
            "gpio_info_replace".encode(): gpio_button.encode()
        }
        page = "./templates/debug.html"
        html_page = self.read_html(page, replace_info)
        self.headers.send(html_page)

        res_info = {
            "status_code": "1",
            "gpio_number": msg.get("gpio_num"),
            "data": msg.get("status")
        }
        self.headers.send(json.dumps(res_info).encode())

    def get_gpio(self, *msg):
        GPIO_info = {
            0: 0,
            1: 1,
            2: -1,
            3: 1
        }
        self.headers.send(json.dumps(GPIO_info).encode())

    def get_home(self, *msg):
        print("home.html。。。")
        print(self.request)
        page = "./templates/send.html"
        html_page = self.read_html(page)
        self.headers.send(html_page)
        print("home.html yes..")

    def favicon(self, *msg):
        # 解决第二次get的问题
        pass

    def get_login(self, *msg):
        print("get_login。。。")

        print(self.request)
        # 设置参数
        page = "./templates/login.html"
        html_page = self.read_html(page)
        self.headers.send(html_page)
        pass

    def set(self, *msg):
        print("set。。。")
        # 设置参数
        page = "./templates/login.html"
        html_page = self.read_html(page)
        self.headers.send(html_page)
        pass

    def check_login(self, *msg):
        print("check_login。。。")
        print(self.request)
        self.get_home()
        # time.sleep(5)
        # 设置参数
        page = "./templates/login.html"
        html_page = self.read_html(page)
        self.headers.send(html_page)
        pass

    def reset(self, *msg):
        print("reset。。。")
        print(self.request)
        # 重置参数
        info = b'{"password": "1234","username": "987654321"}'
        self.headers.send(info)

    def run(self, *msg):
        # 开始工作
        print("run。。。")
        print(self.request)
        info = b'{"password": "1234","username": "987654321"}'
        self.headers.send(info)

    def instructions(self, *msg):
        # 功能介绍，用法说明
        print("test。。。")

        print(self.request)
        # 设置参数
        page = "./templates/end1.html"
        html_page = self.read_html(page)
        self.headers.send(html_page)

    def start(self):
        self.service = socket.socket()
        self.service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.service.bind((self.host, self.port))
        self.service.listen(1)  # 1个还没有接手处理或正在进行的连接
        self.is_start = True
        print("启动端口监听。。。")

    def get_header_info(self):
        self.headers = None
        try:
            self.headers, self.addr = self.service.accept()
            return self.headers
        except KeyboardInterrupt as error:
            print(error)
            traceback.print_exc()
        except Exception as error:
            print(error.args)
            traceback.print_exc()

    def get_request_info(self):
        # 接收客户端发送的消息
        data = self.headers.recv(1024).decode()
        # HTTP请求报文解析，获取请求报文行
        request_header = data.split('\r\n')
        if not request_header:
            # 未捕获数据
            pass

        self.request = {
            "method": "GET",
            "url": "/",
            "msg": {}
        }

        request_first_line = request_header[0].split(' ')
        if len(request_first_line) > 1:
            self.request["method"] = request_first_line[0]
            self.request["url"] = request_first_line[1]

        if self.request["method"] == "POST":
            try:
                self.request["msg"] = json.loads(request_header[-1])
            except:
                msg_list = request_header[-1].split('&')
                info = {}
                for m in msg_list:
                    par = m.split('=')
                    if len(par) == 2:
                        info[par[0]] = par[1]
                self.request["msg"] = info

    def application(self):
        # 在请求中，找对的方法
        method = self.request.get("method")  # 默认是get, home页面
        url = self.request.get("url")  # 默认是get, home页面
        msg = self.request.get("msg")  # 默认是get, home页面

        route_handler = self.route_handlers.get(method, "GET")  # 默认是帮助
        # 需要首先匹配路径，失败后跳转home
        init_func = self.route_handlers.get("GET").get("/home")
        func = route_handler.get(url, init_func)
        func(**msg)  # 执行操作

    def read_html(self, file, replace_info={}):
        res = ""
        with open(file, 'rb') as fp:
            res = fp.read()

        # 替换数据
        for old, new in replace_info.items():
            res = res.replace(old, new)

        return res

    def work(self):
        while True:
            try:
                if self.get_header_info() is None:
                    continue
                self.get_request_info()
                self.application()
            except:
                print("error")
                traceback.print_exc()
            finally:
                self.is_start = False
                self.headers.close()
        # 处理多个端口访问
        # self.client_thread_(self.headers, self.addr)


        # if self.max_threads_ == 0:
        #     self.thread_count_ += 1
        #     self.client_thread_(client_socket_, client_addr_)
        # else:
        #     try:
        #         # _thread.start_new_thread(self.client_thread_, (client_socket_, client_addr_))
        #         self.client_thread_(client_socket_, client_addr_)
        #         self.thread_count_ += 1
        #     except OSError as ex:
        #         print(str(ex))
        #     while self.thread_count_ >= self.max_threads_:
        #         time.sleep(0.1)


def main(name):
    print("开始运行。。。")
    socket_obj = SocketClass()
    socket_obj.start()
    socket_obj.work()

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
