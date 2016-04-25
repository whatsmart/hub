#!/usr/bin/env python3

import json

class RequestParser(object):
    def __init__(self, req):
        self._req = req

    def parse(self):
        obj = json.loads(self._req)

        self.version = obj.get("jsonrpc")
        self.method = obj.get("method")
        self.params = obj.get("params")
        self.id = obj.get("id")

        return self

class RequestBuilder(object):
    def __init__(self, version = "2.0", method = "", params = None, rpcid = None):
        self.version = version
        self.method = method
        self.params = params
        self.rpcid = rpcid

    def build(self):
        obj = {
            "jsonrpc": self.version,
            "method": self.method,
        }
        if self.params:
            obj["params"] = self.params
        if self.rpcid:
            obj["id"] = self.rpcid

        return json.dumps(obj)

class ResponseParser(object):
    def __init__(self, res):
        self._res = res

    def parse(self):
        obj = json.loads(self._res)

        self.version = obj.get("jsonrpc")
        self.result = obj.get("result")
        self.error = obj.get("error")
        self.id = obj.get("id")

class ResultBuilder(object):
    def __init__(self, version = "2.0", rpcid = None, result = None):
        self.version = version
        self.result = result
        self.rpcid = rpcid

    def build(self):
        obj = {
            "jsonrpc": self.version,
            "result": self.result,
            "id": self.rpcid
        }

        return json.dumps(obj)

class ErrorBuilder(object):
    def __init__(self, version = "2.0", rpcid = None, code = None, message = "", data = None):
        self.version = version
        self.rpcid = rpcid
        self.code = code
        self.message = message
        self.data = data

    def build(self):
        obj = {
            "jsonrpc": self.version,
            "error": {
                "code": self.code,
                "message": self.message,
            },
            "id": self.rpcid
        }
        if self.data:
            obj["error"]["data"] = data

        return json.dumps(obj)
