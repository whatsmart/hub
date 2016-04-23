#!/usr/bin/env python3

import json

class JsonrpcRequest(object):
    def __init__(self, req):
        obj = json.loads(req)

        self.version = obj.get("jsonrpc")
        self.method = obj.get("method")
        self.params = obj.get("params")
        self.id = obj.get("id")

        try:
            assert(self.version)
            assert(self.method)
        except AssertionError:
            print("jsonrpc request object must contain \"jsonrpc\" and \"method\" field")

class JsonrpcResponse(object):
    def __init__(self, res):
        obj = json.loads(res)

        self.version = obj.get("jsonrpc")
        self.result = obj.get("result")
        self.error = obj.get("error")
        self.id = obj.get("id")

        try:
            assert(self.version)
            assert(self.id)
            assert(self.result or self.error)
        except AssertionError:
            print("jsonrpc response object must contain \"jsonrpc\", \"id\" and one of \"result\", \"error\" field")

class JsonrpcResult(object):
    def __init__(self, version = "2.0", jid = None, result = None):
        self.res = {
            "jsonrpc": version,
            "result": result,
            "id": jid
        }
    def get_string(self):
        return self.res

class JsonrpcError(object):
    def __init__(self, version = "2.0", jid = None, code = None, message = None, data = None):
        self.err = {
            "jsonrpc": version,
            "error": {
                "code": code,
                "message": message,
            },
            "id": jid
        }
        if data:
            self.err["error"]["data"] = data
    def get_string(self):
        return self.err
