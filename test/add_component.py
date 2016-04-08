#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send(b'HIPC request component 1.0\r\nlength: 122\r\nchecksum: 1434466359\r\n\r\n{"jsonrpc": "2.0","method": "register_component", "params": {"name": "wifi_link_adapter","type": "link_adapter"}, "id": 1}')

while True:
    data = sock.recv(100)
    print(data)
