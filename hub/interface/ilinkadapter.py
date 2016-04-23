#!/usr/bin/env python3

from ..base.hipc import HIPCSerializer
from ..base.jsonrpc import JsonrpcRequest

class ILinkAdapter(object):

    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub
        self.transport = self.ipc.get_protocol().transport
        self.did = int(ipc.get_resource().split("/")[1].strip())
        self.origin = self.ipc.get_origin()
        self.ocid = self.icom.get_component_by_transport(self.transport).id

    def set_visibility(self, visible, time):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "set_visibility",
            "params": {
                "visible": visible,
                "time": time
            },
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def handle_ipc(self):
        obj = json.loads(self.ipc.get_body())
        params = obj.get("params")
        method = obj.get("method")
        mid = obj.get("id")

        if method == "set_visibility":
            visible = params.get("visible")
            time = params.get("time")
            self.set_visibility(visible, time)
