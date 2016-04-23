#!/usr/bin/env python3

import socket
from hub.base.hipc import HIPCSerializer

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
ser = HIPCSerializer()
ser.set_type("request")
ser.set_resource("device/0")
ser.set_body('{"jsonrpc": "2.0","method": "get_position","id": 1}')
s = ser.get_binary()
sock.send(s)

while True:
    data = sock.recv(100)
    print(data.decode("utf-8"))
