#!/usr/bin/env python3

import json
import traceback
from ..base import device
from ..base.hipc import HIPCSerializer
from .icomponent import IComponent

def obj2dict(obj):
    try:
        d = dict()
        d.update(obj.__dict__)
        return d
    finally:
        pass

    return json.JSONEncoder.default(self, o)

class IDevice(object):
    def __init(self, hub = None):
        self.hub = hub

    def add_device(self, dev):
        devices = self.hub.devices
        dids = []
        for d in devices:
            dids.append(d.id)

        if len(dids) > 0:
            for i in range(len(dids)+1):
                if i not in dids:
                    dev.id = i
        else:
            dev.id = 0

        devices.append(dev)
        return dev.id

    def remove_device(self, did):
        devices = self.hub.devices
        for i, d in enumerate(devices):
            if d.id == did:
                devices.pop([i])
                break

    def get_devices(self):
        return self.hub.devices

    def set_name(self, did, name):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                d.name = name
                break

    def get_name(self, did):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                return d.name

    def set_position(self, did, position):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                d.position = position
                break

    def get_position(self, did):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                return d.position

    def handle_ipc(self, ipc):
        self.hub = ipc.protocol.hub
        resource = ipc.get_resource()
        body = ipc.get_body()

        obj = json.loads(body)
        if "method" in obj.keys():
            method = obj["method"]
        if "params" in obj.keys():
            params = obj["params"]
        if "id" in obj.keys():
            mid = obj["id"]

        if method == "add_device":
            try:
                ndev = device.Device()
                for k in [i for i in params.keys() if i != "cid"]:
                    if hasattr(ndev, k):
                        setattr(ndev, k, params[k])
                icomp = IComponent(self.hub)
                ndev.cid = icomp.get_component_by_transport(ipc.get_protocol().transport).id
                did = self.add_device(ndev)
            except Exception:
                body = {
                    "jsonrpc": 2.0,
                    "error": {
                        "code": 0,
                        "message": "unknown error",
#                        "data": str(traceback.format_exc())
                    },
                    "id": mid
                }
            else:
                body = {
                    "jsonrpc": 2.0,
                    "result": did,
                    "id": mid
                }
            finally:
                j = json.dumps(body)
                ser = HIPCSerializer()
                ser.set_type("response")
                ser.set_version(ipc.get_version())
                ser.set_id(ipc.get_id())
                ser.set_body(j)
                ipc.get_protocol().transport.write(ser.serialize())

        elif method == "remove_device":
            self.remove_device(params["id"])
        elif method == "get_devices":
            devs = self.get_devices()
            j = json.dumps(devs, default = obj2dict)
            ipc.protocol.transport.write(j.encode("utf-8"))
            














        
