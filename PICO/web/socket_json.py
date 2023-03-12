import socket
import json


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

        # try:
        #     msg = conn.recv(1024).decode()
        #     recvmsg = json.loads(msg)
        #     print("\nrecvmsg\n", recvmsg)
        # except:
        #     pass
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
