#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send(b'HIPC/1.0 request device\r\nlength: 51\r\nchecksum: 6259772\r\n\r\n{"jsonrpc": "2.0","method": "get_devices", "id": 1}')

while True:
    data = sock.recv(100)
    print(data.decode())
