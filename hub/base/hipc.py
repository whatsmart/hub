#!/usr/bin/env python3

class HIPCParser(object):
    def __init__(self):
        self.state = "ready"
        self._interface = ""
        self._length = None
        self._body = ""
        self._data = ""
        self._cursor = 0

    def parse(self, data):
        if self.state == "ready":
            self._data = self._data + data.decode("utf-8")
            if not self._data.startswith("HIPC"):
#                print("bad package")
                pass

            for index, c in enumerate(self._data):
#                print(index)
                if c == "\n" and self._data[index-1] == "\r":
                    line = self._data[self._cursor:index]

                    if line.startswith("HIPC"):
                        tags = line.split(" ")
                        self._interface = tags[1]
#                        print(self._interface)
                    if line.startswith("length"):
                        l = line.split(":")
                        self._length = int(l[1].strip())
#                        print(self._length)
                    if self._cursor == index - 1:
#                        print("cound tem");
                        self.state = "header_found"
                        self._cursor = index + 1
                        break;
                    self._cursor = index + 1

        if self.state == "header_found":
            self._data = self._data + data.decode("utf-8")
            if len(self._data) - self._cursor >= self._length:
                self._body = self._data[self._cursor:self._cursor+self._length]
                self.state = "finished"

        return self.state

    def get_body_length(self):
        return self._length

    def get_interface(self):
        return self._interface

    def get_body(self):
        return self._body
