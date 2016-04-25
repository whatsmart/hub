#!/usr/bin/env python3

import json
import traceback
from ..base import device
from ..base.hipc import HIPCResponseSerializer
from ..base import jsonrpc
from . import icomponent

class IDevice(object):
    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.resource = ipc.get_resource()
        self.routes = ipc.get_routes()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub
        self.icom = icomponent.IComponent(ipc)

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
        return None

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
        else:
            return None

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
        else:
            return None

    def handle_ipc(self):
        method = self.req.method
        params = self.req.params

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
                    ndev.cid = self.icom.get_component_by_transport(self.protocol.transport).id
                    did = self.add_device(ndev)
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = did).build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())

        elif method == "remove_device":
            try:
                if isinstance(params.get("id"), int):
                    self.remove_device(params.get("id"))
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
        elif method == "get_devices":
            try:
                result = []
                for dev in self.get_devices():
                    d = {
                        "id": dev.id,
                        "vender": dev.vender,
                        "uniqid": dev.uniqid,
                        "hwversion": dev.hwversion,
                        "swversion": dev.swversion,
                        "type": dev.type,
                        "operations": dev.operations
                    }
                    result.append(d)
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = result).build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
        elif method == "set_name":
            try:
                did = int(self.resource.split("/")[1].strip())
                if isinstance(did, int) and isinstance(params.get("name"), str):
                    ret = self.set_name(did, params.get("name"))
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
        elif method == "get_name":
            try:
                did = int(self.resource.split("/")[1].strip())
                if isinstance(did, int):
                    name = self.get_name(did)
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = name if name is not None else "").build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
        elif method == "set_position":
            try:
                did = int(self.resource.split("/")[1].strip())
                if isinstance(did, int) and isinstance(params.get("position"), str):
                    ret = self.set_position(did, params.get("position"))
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
        elif method == "get_position":
            try:
                did = int(resource.split("/")[1].strip())
                if isinstance(did, int):
                    position = self.get_position(did)
                else:
                    raise Exception
            except Exception:
                body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
            else:
                body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = position if position is not None else "").build()
            finally:
                ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body)
                self.protocol.transport.write(ser.get_binary())
