#!/usr/bin/env python3

import binascii

class HIPCParser(object):
    def __init__(self):
        self.state = "ready"
        self._type = ""
        self._version = ""
        self._resource = ""
        self._length = None
        self._checksum = None
        self._id = None
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
                    if line.strip().startswith("id"):
                        p = line.split(":")
                        self._id = int(p[1].strip())
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
                    self.protocol.handle_ipc(self)

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
        self.state = "ready"

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol

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

    def get_id(self):
        return self._id

    def get_body(self):
        return self._body

class HIPCSerializer(object):
    def __init__(self):
        self._version = ""
        self._type = ""
        self._resource = ""
        self._length = None
        self._checksum = None
        self._id = None
        self._body = ""

    def set_version(self, version):
        self._version = version

    def set_type(self, ptype):
        self._type = ptype

    def set_resource(self, resource):
        self._resource = resource

    def set_id(self, pid):
        self._id = pid

    def set_body(self, body):
        self._body = body

    def serialize(self):
        try:
            assert self._type
            if self._type == "request":
                assert self._resource
            assert self._id
        except AssertionError:
            print("Please confirm type, resource and id are not null")

        be = self._body.encode("utf-8")
        s = ""
        if self._version:
            s += "HIPC/" + self._version + " " + self._type + " " + self._resource + "\r\n"
        else:
            s += "HIPC/1.0" + " " + self._type + " " + self._resource + "\r\n"
        s += "length: " + str(len(be)) + "\r\n"
        s += "checksum: " + str(binascii.crc32(be)) + "\r\n"
        s += "id: " + str(self._id) + "\r\n"
        s += self._body
        return s.encode("utf-8")
