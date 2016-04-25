#!/usr/bin/env python3

import asyncio
import json
import copy
from .dispatch import dispatch_ipc
from .base import hipc
from .base import component
from .base.hipc import HIPCParser
from .interface import icomponent

class HubProtocol(asyncio.Protocol):
    def __init__(self):
        self.ipc = hipc.HIPCParser()
        self.ipc.set_protocol(self)
        self.hub = HubProtocol.hub
        self.transport = None
#        print("protocol create")

    def connection_made(self, transport):
#        print("connection made")
        self.transport = transport
        #component
        comp = component.Component()
        comp.transport = self.transport
        
        icomp = icomponent.IComponent(self.ipc)
        icomp.add_component(comp)

    def connection_lost(self, exc):
#        print("connection lost")
        icom = icomponent.IComponent(self.ipc)
        c = icom.get_component_by_transport(self.transport)
        rm = []
        for d in self.hub.devices:
            if d.cid == c.id:
                rm.append(d)
        for d in rm:
            if d in self.hub.devices:
                self.hub.devices.remove(d)

        for k in self.hub.evlisteners:
            if c.id in self.hub.evlisteners[k]:
                self.hub.evlisteners[k].remove(c.id)

        self.hub.components.remove(c)

    def data_received(self, data):
        self.ipc.parse(data)

    def handle_ipc(self, ipc):
        cipc = HIPCParser()
        cipc._type = copy.copy(ipc.get_type())
        cipc._version = copy.copy(ipc.get_version())
        cipc._resource = copy.copy(ipc.get_resource())
        cipc._headers = copy.deepcopy(ipc.get_headers())
        cipc._body = copy.copy(ipc.get_body())
        cipc._resource = copy.copy(ipc.get_resource())
        cipc._protocol = self
        cipc._state = "finished"

        coro = dispatch_ipc(cipc)
        self.hub.loop.create_task(coro)

#        print(ipc.get_version())
#        print(ipc.get_type())
#        print(ipc.get_resource())
#        print(ipc.get_length())
#        print(ipc.get_checksum())
#        print(ipc.get_origin())
#        print(ipc.get_body())
