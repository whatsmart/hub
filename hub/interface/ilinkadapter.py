#!/usr/bin/env python3

from ..base.hipc import HIPCRequestSerializer
from ..base import jsonrpc

class ILinkAdapterControl(object):

    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.routes = ipc.get_routes()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub
        self.did = int(ipc.get_resource().split("/")[1].strip())
        self.icom = icomponent.IComponent(ipc)
        self.idev = idevice.IDevice(ipc)
        self.ocid = self.icom.get_component_by_transport(self.protocol.transport).id

    def set_visibility(self, visible, time):
        body = jsonrpc.RequestBuilder(method = "set_visibility", params = {"visible": visible, "time": time}, rpcid = self.req.id)
        ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)

        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "set_visibility", params = {"visible": visible, "time": time}, rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def handle_ipc(self):
        params = self.req.params
        method = self.req.method

        if method == "set_visibility":
            visible = params.get("visible")
            time = params.get("time")
            self.set_visibility(visible, time)
