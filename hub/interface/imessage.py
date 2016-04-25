#!/usr/bin/env python3

from ..base.hipc import HIPCResponseSerializer
from ..base import jsonrpc
from . import ievent
import json
import traceback

class IMessage(object):

    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.routes = ipc.get_routes()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub
        self.iev = ievent.IEvent(ipc)

    def get_message(self, mid):
        try:
            msg = self.hub.messages.get(mid)
            assert(msg)
        except Exception:
            traceback.print_exc()
            body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
        else:
            body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = msg).build()
        finally:
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
            sb = ser.get_binary()
            self.protocol.transport.write(sb)

    def send_message(self, message):
        try:
            if len(self.hub.messages) > 0:
                mid = max(self.hub.messages.keys()) + 1
            else:
                mid = 0
            self.hub.messages[mid] = message

            event = {
                "name": "message_arrived",
                "data": {
                    "id": mid
                }
            }
        except Exception:
            traceback.print_exc()
            body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
            self.protocol.transport.write(ser.get_binary())
        else:
            body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
            self.protocol.transport.write(ser.get_binary())
            self.iev.report_event(event)

    def handle_ipc(self):
        params = self.req.params
        method = self.req.method

        if method == "get_message":
            mid = int(params.get("id"))
            self.get_message(mid)
        elif method == "send_message":
            msg = params.get("message")
            self.send_message(msg)
