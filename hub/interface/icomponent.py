#!/usr/bin/env python3

from ..base.hipc import HIPCResponseSerializer
from ..base import jsonrpc
from ..base import component

class IComponent(object):
    def __init__(self, ipc):
        if ipc._state == "finished":
            self.ipc_version = ipc.get_version()
            self.routes = ipc.get_routes()
            self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub

    def handle_ipc(self):
        if self.req.method == "register_component":
            self.register_component(req.params)

    def add_component(self, comp):
        cids = []
        for com in self.hub.components:
            cids.append(com.id)

        if len(cids) > 0:
            for i in range(len(cids)+1):
                if i not in cids:
                    comp.id = i
        else:
            comp.id = 0;

        self.hub.components.append(comp)

    def get_component_by_transport(self, transport):
        for com in self.hub.components:
            if transport is com.transport:
                return com
        return None

    def get_component(self, cid):
        for com in self.hub.components:
            if com.id == cid:
                return com
        return None

    def register_component(self, params):
        cid = None
        try:
            name = params.get("name") if params.get("name") else ""
            ctype = params.get("type") if params.get("type") else ""

            com = self.hub.get_component_by_transport(self.protocol.transport)
            com.name = name
            com.type = ctype
            cid = com.id
        except Exception:
            body = jsonrpc.ErrorBuilder(code = 0, message = "unknown error", rpcid = self.req.id).build()
        else:
            body = jsonrpc.ResultBuilder(result = cid, rpcid = self.req.id).build()
        finally:
            ser = HIPCResponseSerializer(version = self.ipc_version, headers = self.routes, body = body).get_binary()
            self.protocol.transport.write(s)
