
import json
from ..base.hipc import HIPCSerializer

class IComponent(object):
    def __init__(self, ipc):
        self.ipc = ipc

    def handle(self):
        body = self.ipc.get_body()
        obj = json.loads(body)
        method = obj["method"]
        params = obj["params"]

        m = eval("self." + method)
        m(obj)
#        self.echo_com_name()

    def register_component(self, obj):
        params = obj["params"]
        rid = obj["id"]
        try:
            hub = self.ipc.get_protocol().hub

            name = params["name"]
            ctype = params["type"]
            com = hub.get_component_by_transport(self.ipc.get_protocol().transport)
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
            if self.ipc.get_pid():
                ser.set_rid(self.ipc.get_pid())
            ser.set_body(j)
            s = ser.serialize()
            #lock is not necessary here, in distpach_rpc, there is no yield
            self.ipc.protocol.transport.write(s)
            
    
    def echo_com_name(self):
        hub = self.ipc.get_protocol().hub
        for com in hub.components:
            print(com.id, com.name, com.type, sep=" ")
    
