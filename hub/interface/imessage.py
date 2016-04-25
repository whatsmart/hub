#!/usr/bin/env python3

from ..base.hipc import HIPCResponseSerializer
from ..base import jsonrpc
from . import ievent

class IMessage(object):

    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.routes = ipc.get_routes()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = ipc.protocol.hub
        self.iev = ievent.IEvent(ipc)

    def get_message(self, mid):
        try:
            msg = self.hub.messages.get(mid)
            assert(msg)
        except Exception:
            body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
        else:
            body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = msg).build()
        finally:
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
            sb = ser.get_binary()
            self.transport.write(sb)

    def send_message(self, message):
        try:
            mid = max(self.hub.messages.keys()) + 1
            self.hub.messages[mid] = message

            event = {
                "name": "message_arrived",
                "data": {
                    "id": mid
                }
            }
        except Exception:
            body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
        else:
            body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
        finally:
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
            iev.report_event(event)

    def handle_ipc(self):
        obj = json.loads(self.ipc.get_body())
        params = obj.get("params")
        method = obj.get("method")
        mid = obj.get("id")

        if method == "get_message":
            mid = params.get("id")
            self.get_message(visible, time)
        elif method == "send_message":
            msg = prams.get("message")
            self.send_message(msg)
