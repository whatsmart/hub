#!/usr/bin/env python3

import socket
import argparse
import sys
import json
from threading import Thread
from hub.base.hipc import HIPCRequestSerializer

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/tmp/hub_sock")

def no_exit(self, status=0, message=None):
    if message:
        self._print_message(message, sys.stderr)

argparse.ArgumentParser.exit = no_exit

def sendcmd():
    while True:
        cmd = input(">>> ")
        if len(cmd.split()) == 0:
            continue
        if cmd.split()[0].strip() == "send_message":

            parser = argparse.ArgumentParser()
            parser.add_argument("-m", dest="msg", type=str, required=True, help="要发送的消息")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("message")
            ser.set_body('{"jsonrpc": "2.0","method": "send_message","params":{"message": "' + str(args.msg) + '"},"id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "get_message":

            parser = argparse.ArgumentParser()
            parser.add_argument("-m", dest="mid", type=int, required=True, help="the message id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("message")
            ser.set_body('{"jsonrpc": "2.0","method": "get_message","params":{"id":' + str(args.mid) + '},"id": 1}')
            sock.send(ser.get_binary())

            del args

def display():
    ser = HIPCRequestSerializer("component")
    ser.set_body('{"jsonrpc": "2.0","method": "register_component","params":{"name": "human machine interaction", "type": "Iteraction"},"id": 1}')
    sock.send(ser.get_binary())

    while True:
        data = sock.recv(100)
        print(data)

dth = Thread(target = display)
dth.start()

sth = Thread(target = sendcmd)
sth.start()
