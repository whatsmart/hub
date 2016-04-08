#!/usr/bin/env python3

import binascii

class HIPCParser(object):
    def __init__(self):
        self.state = "ready"
        self._type = ""
        self._version = ""
        self._interface = ""
        self._length = None
        self._checksum = None
        self._body = ""
        self._data = ""
        self._cursor = 0
        self.protocol = None

    def parse(self, data):
        self._data = self._data + data.decode("utf-8")
        if self.state == "ready":
            if self._data.find("\r\n") == -1:
                return
            if not self._data.startswith("HIPC"):
                index = self._data.find("HIPC")
                if index == -1:
                    self._data = ""
                else:
                    self._data = self._data[index:]  

            for index, c in enumerate(self._data):
#                print(index)
                if c == "\n" and self._data[index-1] == "\r":
                    line = self._data[self._cursor:index]

                    if line.strip().startswith("HIPC"):
                        tags = line.split(" ")
                        self._type = tags[1].strip()
                        self._interface = tags[2].strip()
                        self._version = tags[3].strip()
#                        print(self._interface)
                    if line.strip().startswith("length"):
                        l = line.split(":")
                        self._length = int(l[1].strip())
#                        print(self._length)
                    if line.strip().startswith("checksum"):
                        s = line.split(":")
                        self._checksum = int(s[1].strip())
                    if self._cursor == index - 1:
#                        print("cound tem");
                        self.state = "header_found"
                        self._cursor = index + 1
                        break;
                    self._cursor = index + 1

        if self.state == "header_found":
            if len(self._data) - self._cursor >= self._length:
                self._body = self._data[self._cursor:self._cursor+self._length]
                sum = binascii.crc32(self._body.encode("utf-8"))
                if sum != self._checksum:
                    self._data = self._data[4:]
                    self.parse(bytes())
                else:
                    self.state = "finished"
                    self.protocol.handle_rpc(self)

                    if len(self._data) - self._cursor > self._length:
#                       print(len(self._data) - self._cursor - self._length)
                        self.get_ready()
#                       print(self._data)
                        self.parse(bytes())
                    else:
                        self.get_ready()


    def get_ready(self):
        
        self._interface = ""
        self._body = ""
        if len(self._data) - self._cursor > self._length:
            self._data = self._data[self._cursor+self._length:]
        else:
            self._data = ""
        self._cursor = 0
        self._length = None
        self.state = "ready"

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol

    def get_body_length(self):
        return self._length

    def get_interface(self):
        return self._interface

    def get_checksum(self):
        return self._checksum

    def get_body(self):
        return self._body

    def get_type(self):
        return self._type

class HIPCSerializer(object):
    def __init__(self):
        self._type = ""
        self._interface = ""
        self._length = None
        self._checksum = None
        self._body = ""

    def set_type(self, type):
        self._type = type

    def set_interface(self, interface):
        self._interface = interface

    def set_body(self, body):
        self._body = body

    def serialize(self):
        be = self._body.encode("utf-8")
        s = bytes()
        s += "HIPC ".encode("utf-8") + self._type.encode("utf-8") + " ".encode("utf-8") + self._interface.encode("utf-8") + " 1.0\r\n".encode("utf-8")
        s += "length: ".encode("utf-8") + str(len(be)).encode("utf-8") + "\r\n".encode("utf-8")
        s += "checksum: ".encode("utf-8") + str(binascii.crc32(be)).encode("utf-8") + "\r\n\r\n".encode("utf-8")
        s += be
        return s
