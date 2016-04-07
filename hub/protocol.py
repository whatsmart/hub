#!/usr/bin/env python3

import asyncio
from .base.hipc import *
from .base.component import *

class HubProtocol(asyncio.Protocol):
    def __init__(self):
        print("protocol create")

    def connection_made(self, transport):
        print("connection made")
        #init
        self.ipc = HIPCParser()
        self.ipc.set_protocol(self)
        self.hub = HubProtocol.hub
        self.transport = transport
        #component
        component = Component()
        component.transport = self.transport
        self.hub.add_component(component)

    def conection_lost(self, exc):
        pass

    def data_received(self, data):
        self.ipc.parse(data)

    def handle_rpc(self, ipc):
#        pass
        print(ipc.get_interface())
        print(ipc.get_body_length())
        print(ipc.get_checksum())
        print(ipc.get_body())
