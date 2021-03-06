#!/usr/bin/env python3

from ..base.hipc import HIPCRequestSerializer, HIPCResponseSerializer
from ..base import jsonrpc
from . import icomponent

class IEvent(object):

    def __init__(self, ipc):
        self.ipc_version = ipc.get_version()
        self.dest = ipc.get_dest()
        self.req = jsonrpc.RequestParser(ipc.get_body()).parse()
        self.protocol = ipc.get_protocol()
        self.hub = self.protocol.hub
        self.icom = icomponent.IComponent(ipc)
        self.ocid = self.icom.get_component_by_transport(self.protocol.transport).id

    def report_event(self, event):
        evname = event.get("name").strip()
        if evname in self.hub.evlisteners.keys():
            listeners = self.hub.evlisteners.get(evname)
            if listeners and len(listeners) > 0:
                body = jsonrpc.RequestBuilder(method = "report_event", params = event).build()
                ser = HIPCRequestSerializer(resource = "event", version = self.ipc_version, body = body)
                sb = ser.get_binary()
                for cid in listeners:
                    if cid != self.ocid:
                        self.icom.get_component(cid).transport.write(sb)

    def listen_event(self, names):
        try:
            for name in names:
#                print(name.strip())
                if name.strip() not in self.hub.evlisteners:
                    self.hub.evlisteners[name.strip()] = [self.ocid]
                else:
                    if self.ocid not in self.hub.evlisteners.get(name.strip()):
                        self.hub.evlisteners.get(name.strip()).append(self.ocid)
        except Exception:
            body = jsonrpc.ErrorBuilder(rpcid = self.req.id, code = 0, message = "unknown error").build()
        else:
            body = jsonrpc.ResultBuilder(rpcid = self.req.id, result = None).build()
        finally:
            ser = HIPCResponseSerializer(dest = self.dest, version = self.ipc_version, body = body)
            sb = ser.get_binary()
            self.protocol.transport.write(sb)

    def handle_ipc(self):
        params = self.req.params
        method = self.req.method

        if method == "report_event":
            if not params.get("name"):
                pass
            else:
                self.report_event(params)
        elif method == "listen_event":
            self.listen_event(params)
