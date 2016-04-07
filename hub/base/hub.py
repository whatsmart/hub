#!/usr/bin/env python3

"""this file is the center of smarthub, hub is a component which manages device, service, etc."""

import os
import asyncio
from hipc import *
from component import *

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
        

class Hub (object):
    def __init__(self):
        self.devices = []
        self.services = []
        self.tasks = []
        self.components = []
        self.socketpath = "dasfasdf"
        self.socket = None
        self.connections = []
        self.protocol = None
        self.loop = asyncio.get_event_loop()

    def set_protocol(self, protocol):
        self.protocol = protocol

    def add_component(self, component):
        self.components.append(component)

    def get_component_by_transport(self, tranpsort):
        pass

    def start(self):
        if os.access("/tmp/hub_sock", os.F_OK):
            os.remove("/tmp/hub_sock")
        self.protocol.hub = self
        server = self.loop.create_unix_server(self.protocol, "/tmp/hub_sock");
        self.loop.run_until_complete(server)
        self.loop.run_forever()

if __name__ == "__main__":
    hub = Hub()
    hub.set_protocol(HubProtocol)

    hub.start()
