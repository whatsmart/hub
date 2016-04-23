#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send('''HIPC/1.0 request device\r\nlength: 267\r\nchecksum: 1008906891\r\n\r\n{"jsonrpc": "2.0","method": "add_device","params": {"vender": "Obama","type": "lighting","hwversion": "1.2","swversion": "2.3","uniqid": "siufhwoe9232o3df","operations": ["power_on", "power_off", "set_brightness", "get_brightness", "set_color", "get_color"]},"id": 1}'''.encode("utf-8"))

while True:
    data = sock.recv(100)
    print(data)
