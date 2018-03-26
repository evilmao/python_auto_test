# -*- coding:utf-8 -*-
# author by Failymao
"""
-socket 接口测试代码
socket server 端
两个接口，add和sub
接收：
{
    "action": "add",
    "params": {"a": 1, "b": 2}
}
返回：
{
    "action": "add",
    "result": 3
}

"""
import json
import socket


def add(a, b):
    return a + b


ip_port = ('127.0.0.1', 8080)
server = socket.socket()
server.bind(ip_port)
server.listen(5)

while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    data = data.decode()

    try:
        ddata = json.loads(data)
        action = ddata.get('action')
        params = ddata.get('params')
        if action == 'add':
            res = add(**params)
            conn.send(b'{"action": "add", "result": %d}' % res)
        else:
            conn.send(b'{"code":-2, "message":"Wrong Action"}')
    except (AttributeError, ValueError):
        conn.send(b'{"code":-1, "message":"Data Error"}')
    finally:
        conn.close()
