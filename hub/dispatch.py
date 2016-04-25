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
    protocol = ipc.get_protocol()

    if itype == "response":
        if "rt-component" in ipc.get_headers():
            cid = int(ipc.get_header("rt-component"))
            component = icom.get_component(cid)
            if component:
                ser = HIPCResponseSerializer()
                ser.set_version(ipc.get_version())
                for k in ipc.get_headers().keys():
                    if "rt-" in k and k != "rt-component":
                        headers[k] = ipc.get_headers()[k]
                ser.set_headers(headers)
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
