import socket
import sys
import json


class SocketClass:

    def __init__(self):
        # self.host = "127.0.0.1"
        self.host = "localhost"
        self.port = 80

        self.is_start = False
        self.max_thread = 16

        self.thread_count_ = 0
        self.route_handlers = {
            "POST": {
                "set": self.set,
                "reset": self.reset,
                "run": self.run
            },
            "GET": {
                "home": self.get_home,
                "instructions": self.instructions
            }
        }

    def set(self):
        # 设置参数
        pass

    def reset(self):
        # 重置参数
        pass

    def run(self):
        # 开始工作
        pass

    def instructions(self):
        # 功能介绍，用法说明
        pass


    def start(self):
        self.service = socket.socket()
        # self.service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.service.bind((self.host, self.port))
        self.service.listen(1)  # 1个还没有接手处理或正在进行的连接
        self.is_start = True

    def get_header_info(self):
        self.headers = None
        try:
            self.headers, self.addr = self.service.accept()
            return self.headers
        except KeyboardInterrupt as error:
            print("KeyboardInterrupt")
        except Exception as error:
            print(error.args)
            sys.print_exception(error)

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
        route_handler = self.route_handlers.get(method, "GET")  # 默认是帮助
        # 需要首先匹配路径，失败后跳转home
        func = route_handler.get(self.request.get("url"), self.home)
        func(self.request.get("msg"))  # 执行操作

    def read_html(self, file, replace_info={}):
        res = ""
        with open(file, 'rb') as fp:
            res = fp.read()

        # 替换数据
        for old, new in replace_info.items():
            res.replace(old, new)

        return res

    def work(self):
        try:
            while True:
                if self.get_header_info() is None:
                    continue
                self.get_request_info()
                self.application()
        except:
            print("error")
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


def main():
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置监听端口
    s.bind(('localhost', 80))
    s.listen(1)
    print("启动监听。。。。")
    # 循环等待客户端连接
    while True:
        # 接受客户端连接
        conn, addr = s.accept()
        # 接收客户端发送的消息
        data = conn.recv(1024).decode()
        # HTTP请求报文解析，获取请求报文行
        request_header = data.split('\r\n')
        request_first_line = request_header[0].split(' ')

        if len(request_first_line) < 2:
            continue

        elif request_first_line[0] == "POST":
            msg = request_header[-1]
            msg_list = msg.split('&')
            info = {}
            for m in msg_list:
                par = m.split('=')
                if len(par) == 2:
                    info[par[0]] = par[1]
            print("POST", info)
        elif request_first_line[0] == "GET":
            print("GET", request_header[-1])

        print(request_header)
        # 获取请求路径
        request_path = request_first_line[1]
        # 如果请求路径是根路径，返回页面
        if request_path == '/':
            # HTTP响应报文，状态行
            response_first_line = 'HTTP/1.1 200 OK\r\n'
            # HTTP响应报文，首部
            response_header = 'Content-Type: text/html;charset=utf-8\r\n'
            # HTTP响应报文，使用HTML页面
            response_body = '<html><body><h1>使用Python Socket库搭建HTML页面</h1></body></html>'
            # 拼接响应报文
            response = response_first_line + response_header + '\r\n' + response_body
            # 发送响应报文
            encode_response = response.encode()
            conn.send(encode_response)
        elif request_path == '/c':
            # HTTP响应报文，状态行
            response_first_line = '' \
                                  '' \
                                  '' \
                                  '\r\n'
            # HTTP响应报文，首部
            response_header = 'Content-Type: text/html;charset=utf-8\r\n'
            # HTTP响应报文，使用HTML页面
            response_body = """
                        <html><body><h1>1111  使用Python Socket库搭建HTML %s</h1></body></html>"""
            # 拼接响应报文
            response = response_first_line + response_header + '\r\n' + response_body
            response = response % request_path

            with open('web/control_page.html', encoding='utf-8') as fp:
                html_tempt = fp.read()
            response = html_tempt
            # response = html_tempt % request_path
            # 发送响应报文
            conn.send(response.encode())
        else:
            # HTTP响应报文，状态行
            response_first_line = 'HTTP/1.1 200 OK\r\n'
            # HTTP响应报文，首部
            response_header = 'Content-Type: text/html;charset=utf-8\r\n'
            # HTTP响应报文，使用HTML页面
            response_body = """
            <html><body><h1>1111  使用Python Socket库搭建HTML %s</h1></body></html>"""
            # 拼接响应报文
            response = response_first_line + response_header + '\r\n' + response_body
            response = response % request_path

            with open('web/login.html', 'rb') as fp:
                # with open('login.html') as fp:
                html_tempt = fp.read()
            # response = bytes(html_tempt, encoding='UTF-8')

            # response = html_tempt % (request_path, 1, 3)
            # response = html_tempt % request_path
            encode_response = html_tempt
            # 发送响应报文
            # conn.send(response.encode("utf-8"))
            # encode_response = response.encode()
            conn.send(encode_response)
            # conn.send(response)

        # 关闭连接
        conn.close()

if __name__ == '__main__':
    print("程序运行中。。。。")
    main()
    