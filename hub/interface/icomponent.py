
import json
from ..base.hipc import HIPCSerializer
from ..base import component

class IComponent(object):
    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub

    def handle_ipc(self):
        resource = ipc.get_resource()
        body = self.ipc.get_body()

        obj = json.loads(body)
        if "method" in obj.keys():
            method = obj["method"]
        if "params" in obj.keys():
            params = obj["params"]


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

    def register_component(self, obj):
        params = obj["params"]
        rid = obj["id"]
        try:
            hub = self.ipc.get_protocol().hub

            name = params["name"]
            ctype = params["type"]
            com = self.hub.get_component_by_transport(self.ipc.get_protocol().transport)
            com.name = name
            com.type = ctype
            cid = com.id
        except NameError:
            pass
        else:
            o = {}
            o["id"] = rid
            o["jsonrpc"] = "2.0"
            o["result"] = {}
            o["result"]["code"] = "success"
            o["result"]["id"] = cid
            j = json.dumps(o)
#            print(j)
            ser = HIPCSerializer()
            ser.set_resource(self.ipc.get_resource())
            ser.set_type("response")
            ser.set_body(j)
            s = ser.serialize()
            #lock is not necessary here, in distpach_rpc, there is no yield
            self.ipc.protocol.transport.write(s)
