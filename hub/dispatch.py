#/usr/bin/env python3

import asyncio
from .interface import icomponent
from .interface import icontrol
from .interface import idevice
from .interface import imessage
from .interface import ievent
from .base.hipc import HIPCResponseSerializer

@asyncio.coroutine
def dispatch_ipc(ipc):
    itype = ipc.get_type()
    hub = ipc.get_protocol().hub
    icom = icomponent.IComponent(ipc)
    resource = ipc.get_resource()
    route = ipc.get_last_route()
    protocol = ipc.get_protocol()

    if itype == "response":
        if route:
            if route.find("hub/"):
                cid = int(route[4:])
                component = icom.get_component(cid)
                if component:
                    ser = HIPCResponseSerializer()
                    dest = ipc.get_dest().split("@")
                    dest = "@".join(dest[0:len(dest)-1])
                    ser.set_version(dest = dest, version = ipc.get_version())
                    ser.set_headers(headers)
                    ser.set_body(ipc.get_body())
                    component.transport.write(ser.get_binary())
        else:
            #handle response by hub
            pass

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
