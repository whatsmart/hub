#/usr/bin/env python3

import asyncio
from .interface import icomponent
from .interface import icontrol
from .interface import idevice
from .base.hipc import HIPCSerializer

@asyncio.coroutine
def dispatch_ipc(ipc):
    itype = ipc.get_type()
    resource = ipc.get_resource()
    protocol = ipc.get_protocol()

    if itype == "response":
        #forward the message to it's requestor
        if origin.startswith("component"):
            transport = protocol.hub.get_component(cid).transport
            if transport:
                ser = HIPCSerializer()
                ser.set_version(ipc.get_version())
                ser.set_type(ipc.get_type())
                ser.set_resource(ipc.get_resource())
                ser.set_id(ipc.get_id())
                ser.set_body(ipc.get_body())
                transport.write(ser.serialize())
        elif origin.startswith("hub"):
            pass

    elif itype == "request":
        if resource.startswith("component"):
            icom = icomponent.IComponent()
            icom.handle_ipc(ipc)
        elif resource.startswith("device"):
            idev = idevice.IDevice()
            idev.handle_ipc(ipc)
        elif resource.startswith("control"):
            icon = icontrol.IControl()
            icon.handle_ipc(ipc)
                
