#/usr/bin/env python3

import asyncio
from .interface import icomponent
from .interface import icontrol
from .interface import idevice
from .base.hipc import HIPCSerializer

@asyncio.coroutine
def dispatch_ipc(ipc):
    itype = ipc.get_type()
    hub = ipc.get_protocol().hub
    icom = icomponent.IComponent(ipc)
    resource = ipc.get_resource()
    protocol = ipc.get_protocol()

    if itype == "response":
        origin = ipc.get_origin()
        cid = int(origin.split(":")[0].split("/")[1].strip())
        if ":" in origin:
            rest = origin[origin.find(":")+1:]
        else:
            rest = ""
        print(rest) #
        component = icom.get_component(cid)
        if component:
            ser = HIPCSerializer()
            ser.set_type("response")
            ser.set_version(ipc.get_version())
            if rest:
                ser.set_origin(rest)
            ser.set_body(ipc.get_body())
            component.transport.write(ser.get_binary())

    elif itype == "request":
        if resource.startswith("component"):
            icom = icomponent.IComponent(ipc)
            icom.handle_ipc()
        elif resource.startswith("device"):
            idev = idevice.IDevice(ipc)
            idev.handle_ipc()
        elif resource.startswith("control"):
            icon = icontrol.IControl(ipc)
            icon.handle_ipc()
        elif resource.startswith("event"):
            iev = ievent.IEvent(ipc)
            iev.handle_ipc()
        elif resource.startswith("message"):
            imess = imessage.IMessage(ipc)
            imess.handle_ipc()
