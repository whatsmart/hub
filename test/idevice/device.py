#!/usr/bin/env python3

import socket
import argparse
import sys
import json
from threading import Thread
from hub.base.hipc import HIPCRequestSerializer
from hub.base import jsonrpc

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
        if cmd.split()[0].strip() == "add_device":

            print("请输入设备的属性")
            vender = input("厂商：")
            uniqid = input("唯一ID：")
            hwversion = input("硬件版本：")
            swversion = input("软件版本：")
            dtype = input("类型：")
            operations = input("操作：")
            operations = operations.split()

            dev = {
                "vender": vender,
                "uniqid": uniqid,
                "hwversion": hwversion,
                "swversion": swversion,
                "type": dtype,
                "operations": operations
            }

            body = jsonrpc.RequestBuilder(method = "add_device", rpcid = 1, params = dev).build()

            ser = HIPCRequestSerializer("device")
            ser.set_body(body)
            sock.send(ser.get_binary())

        elif cmd.split()[0].strip() == "remove_device":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("device")
            ser.set_body('{"jsonrpc": "2.0","method": "remove_device","params":{"id": ' + str(args.devid) + '},"id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "get_devices":

            ser = HIPCRequestSerializer("device")
            ser.set_body('{"jsonrpc": "2.0","method": "get_devices","id": 1}')
            sock.send(ser.get_binary())

        elif cmd.split()[0].strip() == "get_name":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="设备的id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("device/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "get_name","params":{"id": ' + str(args.devid) + '},"id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "set_name":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            parser.add_argument("-n", dest="name", type=str, required=True, help="要设置的名称")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue
            ser = HIPCRequestSerializer("device/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "set_name","params":{"name": "' + str(args.name) + '"},"id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "get_position":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue

            ser = HIPCRequestSerializer("device/" + str(args.devid))
            ser.set_body('{"jsonrpc": "2.0","method": "get_position","id": 1}')
            sock.send(ser.get_binary())

            del args

        elif cmd.split()[0].strip() == "set_position":

            parser = argparse.ArgumentParser()
            parser.add_argument("-d", dest="devid", type=int, required=True, help="the device id")
            parser.add_argument("-p", dest="position", type=str, required=True, help="要设置的位置")
            args = None
            try:
                args = parser.parse_args(cmd.split()[1:])
            except Exception:
                del args
                continue
            else:
                ser = HIPCRequestSerializer("device/" + str(args.devid))
                ser.set_body('{"jsonrpc": "2.0","method": "set_position","params":{"position": "' + str(args.position) + '"},"id": 1}')
                sock.send(ser.get_binary())
                del args

def display():
    ser = HIPCRequestSerializer("component")
    ser.set_body('{"jsonrpc": "2.0","method": "register_component","params":{"name": "zigbee link adapter", "type": "ZigbeeLinkAdapter"},"id": 1}')
    sock.send(ser.get_binary())
    while True:
        data = sock.recv(100)
        print(data)

dth = Thread(target = display)
dth.start()

sth = Thread(target = sendcmd)
sth.start()
