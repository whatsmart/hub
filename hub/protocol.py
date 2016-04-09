#!/usr/bin/env python3

import asyncio
import json
import copy
from .dispatch import dispatch_rpc
from .base import hipc
from .base import component
from .interface import icomponent

class HubProtocol(asyncio.Protocol):
    def __init__(self):
        print("protocol create")

    def connection_made(self, transport):
        print("connection made")
        #init
        self.ipc = hipc.HIPCParser()
        self.ipc.set_protocol(self)
        self.hub = HubProtocol.hub
        self.transport = transport
        #component
        comp = component.Component()
        comp.state = "not_detailed"
        comp.transport = self.transport
        self.hub.add_component(comp)

    def conection_lost(self, exc):
        pass

    def data_received(self, data):
        self.ipc.parse(data)

    def handle_rpc(self, ipc):
        protocol = copy.copy(self)
        cipc = copy.copy(ipc)

        coro = dispatch_rpc(protocol, cipc)
        self.hub.loop.create_task(coro)

        print(ipc.get_version())
        print(ipc.get_type())
        print(ipc.get_resource())
        print(ipc.get_length())
        print(ipc.get_checksum())
        print(ipc.get_origin())
        print(ipc.get_pid())
        print(ipc.get_rid())
        print(ipc.get_body())
