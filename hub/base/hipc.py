#!/usr/bin/env python3

import binascii

class HIPCParser(object):
    def __init__(self):
        self._state = "ready"
        self._type = ""
        self._version = ""
        self._resource = ""
        self._length = None
        self._checksum = None
        self._origin = ""
        self._body = ""
        self._data = ""
        self._cursor = 0
        self._protocol = None

    def parse(self, data):
        self._data = self._data + data.decode("utf-8")
        if self._state == "ready":
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
                        self._version = tags[0].strip().split("/")[1].strip()
                        self._type = tags[1].strip()
                        self._resource = tags[2].strip()
#                        print(self._resource)
                    if line.strip().startswith("length"):
                        l = line.split(":")
                        self._length = int(l[1].strip())
#                        print(self._length)
                    if line.strip().startswith("checksum"):
                        s = line.split(":")
                        self._checksum = int(s[1].strip())
                    if line.strip().startswith("origin"):
                        p = line.split(":")
                        self._origin = int(p[1].strip())
                    if self._cursor == index - 1:
#                        print("cound tem");
                        self._state = "header_found"
                        self._cursor = index + 1
                        break;
                    self._cursor = index + 1

        if self._state == "header_found":
            if len(self._data) - self._cursor >= self._length:
                self._body = self._data[self._cursor:self._cursor+self._length]
                sum = binascii.crc32(self._body.encode("utf-8"))
                if sum != self._checksum:
                    self._data = self._data[4:]
                    self.parse(bytes())
                else:
                    self._state = "finished"
                    self._protocol.handle_ipc(self)

                    if len(self._data) - self._cursor > self._length:
#                       print(len(self._data) - self._cursor - self._length)
                        self.get_ready()
#                       print(self._data)
                        self.parse(bytes())
                    else:
                        self.get_ready()


    def get_ready(self):
        
        self._resource = ""
        self._body = ""
        if len(self._data) - self._cursor > self._length:
            self._data = self._data[self._cursor+self._length:]
        else:
            self._data = ""
        self._type = ""
        self._version = ""
        self._checksum = None
        self._id = None
        self._cursor = 0
        self._length = None
        self._state = "ready"

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def get_version(self):
        return self._version

    def get_type(self):
        return self._type

    def get_resource(self):
        return self._resource

    def get_length(self):
        return self._length

    def get_checksum(self):
        return self._checksum

    def get_origin(self):
        return self._origin

    def get_body(self):
        return self._body

class HIPCSerializer(object):
    def __init__(self, mtype = "", version = "", resource = "", origin = "", body = ""):
        self._version = version
        self._type = mtype
        self._resource = resource
        self._length = None
        self._checksum = None
        self._origin = origin
        self._body = body

    def set_version(self, version):
        self._version = version

    def set_type(self, ptype):
        self._type = ptype

    def set_resource(self, resource):
        self._resource = resource

    def set_origin(self, origin):
        self._origin = origin

    def set_body(self, body):
        self._body = body

    def serialize(self):
        try:
            assert self._type
            if self._type == "request":
                assert self._resource
        except AssertionError:
            print("Please confirm type, resource are not null")

        be = self._body.encode("utf-8")
        s = ""
        if self._version:
            s += "HIPC/" + self._version + " " + self._type
        else:
            s += "HIPC/1.0" + " " + self._type
        if self._type == "response":
            s += "\r\n"
        elif self._type == "request":
            s += " " + self._resource + "\r\n"
        s += "length: " + str(len(be)) + "\r\n"
        s += "checksum: " + str(binascii.crc32(be)) + "\r\n"
        if self._origin:
            s += "origin: " + str(self._origin) + "\r\n"
        s += "\r\n"
        s += self._body
        return s

    def get_binary(self):
        return self.serialize().encode("utf-8")

    def get_string(self):
        return self.serialize()
