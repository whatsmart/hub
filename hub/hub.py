#!/usr/bin/env python3

"""this file is the center of smarthub, hub is a component which manages device, service, etc."""

import os
import asyncio
from .protocol import HubProtocol

class Hub (object):
    def __init__(self):
        self.devices = []
        self.services = []
        self.tasks = []
        self.components = []
        #event listeners, each is event -> [cid1, cid2, ...]
        self.evlisteners = {}
        # id -> message
        self.messages = {}
        self.protocol = None
        self.loop = asyncio.get_event_loop()

    def start(self):
        if os.access("/tmp/hub_sock", os.F_OK):
            os.remove("/tmp/hub_sock")

        self.protocol = HubProtocol
        self.protocol.hub = self
        server = self.loop.create_unix_server(self.protocol, "/tmp/hub_sock");
        self.loop.create_task(server)
        self.loop.run_forever()

if __name__ == "__main__":
    hub = Hub()

    hub.start()
