#!/usr/bin/env python3

import socket
import time

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send(b'HIPC/2.0 request control/id/123\r\norigin: user/123\r\npid: 1213\r\nchecksum: 2718902657\r\nlength: 8\r\n\r\n{"x": 4}HI')
sock.send(b'PC/3.0 request control/id/1543\r\norigin: user/123\r\npid: 1213\r\nchecksum: 589887208\r\nlength: 16\r\n\r\n{"x": 4, "y": 5}')
sock.close
