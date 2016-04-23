#!/usr/bin/env python3

from ..base.hipc import HIPCSerializer
from ..base.jsonrpc import JsonrpcRequest

class IEvent(object):

    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub
        self.transport = self.ipc.get_protocol().transport
        self.origin = self.ipc.get_origin()
        self.ocid = self.icom.get_component_by_transport(self.transport).id
        self.icom = icomponent.IComponent(self.ipc)

    def report_event(self, event):
        evname = event.get("name").strip()
        if evname in self.hub.evlisteners:
            listeners = self.hub.evlisteners.get("name")
            if len(listeners) > 0:
                ser = HIPCSerializer()
                ser.set_version("1.0")
                ser.set_type("request")
                ser.set_resource("event")

                body = {
                    "jsonrpc": "2.0",
                    "method": "report_event",
                    "params": event
                }

                bj = json.dumps(body, indent = 4)
                ser.set_body(bj)
                sb = ser.get_binary()
            for cid in listeners:
                self.icom.get_component(cid).transport.write(sb)

    def listen_event(self, names):
        for name in names:
            if name not in self.hub.evlisteners:
                self.hub.evlisteners[name] = [self.ocid]
            else:
                self.hub.evlisteners.get(name).append(self.ocid)

        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("response")

        body = {
            "jsonrpc": "2.0",
            "result": None,
            "id": JsonrpcRequest(self.ipc.get_body()).id
        }

        bj = json.dumps(body, indent = 4)
        ser.set_body(bj)
        sb = ser.get_binary()

        self.transport.write(sb)

    def handle_ipc(self):
        obj = json.loads(self.ipc.get_body())
        params = obj.get("params")
        method = obj.get("method")
        mid = obj.get("id")

        if method == "report_event":
            if not params.get("name"):
                pass
            self.report_event(params)
        elif method == "listen_event":
            self.listen_event(params)
