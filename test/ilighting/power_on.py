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
        if cmd.split()[0].strip() == "power_on":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("control/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "power_on","id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "power_off":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("control/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "power_off","id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "get_power_state":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("control/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "get_power_state","id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "get_color":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("control/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "get_color","id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "set_color":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            parser.add_argument("-c", dest="color", type=int, required=True, help="the color to set")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue
            ser = HIPCRequestSerializer("control/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "set_color","params":{"color": ' + str(args.color) + '},"id": 1}')
            print(ser.get_string())
            sock.send(ser.get_binary())

            del args

def display():
    while True:
        data = sock.recv(100)
        print(data)

dth = Thread(target = display)
dth.start()

sth = Thread(target = sendcmd)
sth.start()
