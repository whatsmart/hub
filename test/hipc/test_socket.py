#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")
sock.send(b"asdfHIPC/1.0 request control/123\r\nchecksum: 2745614147\r\nlength: 2\r\n\r\n{}")
sock.close
