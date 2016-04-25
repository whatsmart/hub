#!/usr/bin/env python3

from . import idevice
from . import icomponent
from ..base.hipc import HIPCRequestSerializer
from ..base import jsonrpc

class ILightingControl(object):
    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.routes = ipc.get_routes()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub
        self.did = int(ipc.get_resource().split("/")[1].strip())
        self.idev = idevice.IDevice(ipc)
        self.icom = icomponent.IComponent(ipc)
        self.ocid = self.icom.get_component_by_transport(self.protocol.transport).id

    def power_on(self):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "power_on", rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def power_off(self):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "power_off", rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def get_power_state(self):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "get_power_state", rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def set_color(self, color):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "set_color", rpcid = self.req.id, params = {"color": color}).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def get_color(self):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "get_color", rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def set_brightness(self, brightness):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "set_brightness", rpcid = self.req.id, params = {"brightness": brightness}).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def get_brightness(self, color):
        try:
            tc = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(ser)
        else:
            body = jsonrpc.RequestBuilder(method = "get_brightness", rpcid = self.req.id).build()
            ser = HIPCRequestSerializer(resource = "control/"+str(self.did), version = self.ipc_version, headers = self.routes, body = body)
            ser.set_header("rt-component", str(self.ocid))
            tc.write(ser.get_binary())

    def handle_ipc(self):
        params = self.req.params
        method = self.req.method

        if method == "power_on":
            self.power_on()
        elif method == "power_off":
            self.power_off()
        elif method == "get_power_state":
            self.get_power_state()
        elif method == "set_color":
            color = int(params.get("color"))
            self.set_color(color)
        elif method == "get_color":
            self.get_color()
        elif method == "set_brightness":
            brightness = int(params.get("brightness"))
            if brightness >= 0 and brightness <= 100:
                self.set_brightness(brightness)
        elif method == "get_brightness":
            self.get_brightness()
