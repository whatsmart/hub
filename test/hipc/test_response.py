#!/usr/bin/env python3

import socket
import time

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send(b'HIPC/1.0 response control/id/123\r\norigin: 1213\r\nchecksum: 2718902657\r\nlength: 8\r\n\r\n{"x": 4}')
sock.close
