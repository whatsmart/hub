#/usr/bin/env python3

import asyncio
from .interface import icomponent

@asyncio.coroutine
def dispatch_rpc(protocol, ipc):
    itype = ipc.get_type()
    resource = ipc.get_resource()
    if resource.startswith("component") and itype == "request":
        icom = icomponent.IComponent(ipc)
        icom.handle()

