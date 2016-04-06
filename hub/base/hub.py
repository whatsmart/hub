#!/usr/bin/env python3

"""this file is the center of smarthub, hub is a component which manages device, service, etc."""

import os
import asyncio
from hipc import *

class HubProtocol(asyncio.Protocol):
    def __init__(self):
        self.ipc = HIPCParser()

    def connection_made(self, transport):
        print("asdf")
        print(HubProtocol.hub.socketpath)

    def conection_lost(self, exc):
        pass

    def data_received(self, data):
        if (self.ipc.parse(data) == "finished"):
            print(self.ipc.get_interface())
            print(self.ipc.get_body_length())
            print(self.ipc.get_body())
            

class Hub (object):
    def __init__(self):
        self.device = []
        self.service = []
        self.task = []
        self.plugin = []
        self.socketpath = "dasfasdf"
        self.socket = None
        self.connections = []
        self.protocol = None
        self.loop = asyncio.get_event_loop()

    def set_protocol(self, protocol):
        self.protocol = protocol

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
