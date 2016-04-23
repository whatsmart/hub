#!/usr/bin/env python3

import json
import traceback
from ..base import device
from ..base.hipc import HIPCSerializer
from ..base.jsonrpc import JsonrpcRequest, JsonrpcResponse, JsonrpcResult, JsonrpcError
from .icomponent import IComponent

class IDevice(object):
    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub

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

    def get_device(self, did):
        for d in self.hub.devices:
            if d.id == did:
                return d

    def get_devices(self):
        return self.hub.devices

    def set_name(self, did, name):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                d.name = name
                break
        else:
            return "device_not_found"
    def get_name(self, did):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                return d.name
        else:
            return None

    def set_position(self, did, position):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                d.position = position
                break
        else:
            return "device_not_found"

    def get_position(self, did):
        devices = self.hub.devices
        for d in devices:
            if d.id == did:
                return d.position
        else:
            return None

    def handle_ipc(self):
        resource = self.ipc.get_resource()
        body = self.ipc.get_body()

        obj = json.loads(body)

        method = obj.get("method")
        params = obj.get("params")
        mid = obj.get("id")

        if method == "add_device":
            try:
                ndev = device.Device()
                ndev.vender = params.get("vender")
                ndev.uniqid = params.get("uniqid")
                ndev.hwversion = params.get("hwversion")
                ndev.swversion = params.get("swversion")
                ndev.type = params.get("type")
                ndev.operations = params.get("operations")
                if isinstance(ndev.vender, str) and  isinstance(ndev.uniqid, str) \
                    and isinstance(ndev.hwversion, str) and isinstance(ndev.swversion, str) \
                    and isinstance(ndev.type, str) and isinstance(ndev.operations, list):
                    icomp = IComponent(self.ipc)
                    ndev.cid = icomp.get_component_by_transport(self.ipc.get_protocol().transport).id
                    did = self.add_device(ndev)
                else:
                    raise Exception
            except Exception:
                print(traceback.print_exc())
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error")
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = did)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())

        elif method == "remove_device":
            try:
                if isinstance(params.get("id"), int):
                    self.remove_device(params.get("id"), int)
                else:
                    raise Exception
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error")
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = None)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
        elif method == "get_devices":
            try:
                result = []
                for dev in self.get_devices():
                    d = {}
                    d["id"] = dev.id
                    d["vender"] = dev.vender
                    d["uniqid"] = dev.uniqid
                    d["hwversion"] = dev.hwversion
                    d["swversion"] = dev.swversion
                    d["type"] = dev.type
                    d["operations"] = dev.operations
                    result.append(d)
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error", data = traceback.format_exc())
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = result)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
#                print(b)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
        elif method == "set_name":
            try:
                did = int(resource.split("/")[1].strip())
                if isinstance(did, int) and isinstance(params.get("name"), str):
                    ret = self.set_name(did, params.get("name"))
                else:
                    raise Exception
                if ret == "device_not_found":
                    raise Exception
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error", data=traceback.format_exc())
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = None)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
        elif method == "get_name":
            try:
                did = int(resource.split("/")[1].strip())
                if isinstance(did, int):
                    name = self.get_name(did)
                else:
                    raise Exception
                if not name:
                    raise Exception
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error")
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = name)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
        elif method == "set_position":
            try:
                did = int(resource.split("/")[1].strip())
                if isinstance(did, int) and isinstance(params.get("position"), str):
                    ret = self.set_position(did, params.get("position"))
                else:
                    raise Exception
                if ret == "device_not_found":
                    raise Exception
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error", data=traceback.format_exc())
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = None)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
        elif method == "get_position":
            try:
                did = int(resource.split("/")[1].strip())
                if isinstance(did, int):
                    position = self.get_position(did)
                else:
                    raise Exception
                if not position:
                    raise Exception
            except Exception:
                je = JsonrpcError(jid = mid, code = 0, message = "unknown error")
                body = je.get_string()
            else:
                jr = JsonrpcResult(jid = mid, result = position)
                body = jr.get_string()
            finally:
                b = json.dumps(body, indent = 4)
                ser = HIPCSerializer(mtype = "response", body = b, version = self.ipc.get_version())
                self.ipc.get_protocol().transport.write(ser.get_binary())
