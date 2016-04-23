#!/usr/bin/env python3

import json
from . import idevice
from . import icomponent
from ..base.hipc import HIPCSerializer
from ..base.jsonrpc import JsonrpcRequest

class ILightingControl(object):
    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub
        self.transport = self.ipc.get_protocol().transport
        self.did = int(ipc.get_resource().split("/")[1].strip())
        self.idev = idevice.IDevice(self.ipc)
        self.icom = icomponent.IComponent(self.ipc)
        self.origin = self.ipc.get_origin()
        self.ocid = self.icom.get_component_by_transport(self.transport).id

    def power_on(self):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "power_on",
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def power_off(self):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "power_off",
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def get_power_state(self):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "get_power_state",
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def set_color(self, color):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "set_color",
            "params": {
                "color": hex(color)
            },
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def get_color(self, color):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "get_color",
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def set_brightness(self, brightness):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "set_brightness",
            "params": {
                "brightness": brightness
            },
            "id": rpcid
        }
        bj = json.dumps(body, indent = 4)

        ser.set_body(bj)
        sb = ser.get_binary()

        ct = self.icom.get_component(self.idev.get_device(self.did).cid).transport
        ct.write(sb)

    def get_brightness(self, color):
        ser = HIPCSerializer()
        ser.set_version("1.0")
        ser.set_type("request")
        ser.set_resource("control/"+str(self.did))
        ser.set_origin("component/" + str(self.ocid) + ":" + self.origin)

        rpcid = JsonrpcRequest(self.ipc.get_body()).id

        body = {
            "jsonrpc": "2.0",
            "method": "get_brightness",
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

        if method == "power_on":
            self.power_on()
        elif method == "power_off":
            self.power_off()
        elif method == "get_power_state":
            self.get_power_state()
        elif method == "set_color":
            color = int(params.get("color").strip())
            if color >= 0 and color <= 100:
                self.set_color(color)
        elif method == "get_color":
            self.get_color()
        elif method == "set_brightness":
            brightness = int(params.get("brightness").strip())
            self.set_brightness(brightness)
        elif method == "get_brightness":
            self.get_brightness()
            
