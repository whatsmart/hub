#!/usr/bin/env python3

class IControl(object):

    def __init__(self, ipc):
        self.ipc = ipc

    def handle(self):
        resource = self.ipc.get_resource()
        params = resource.split("/")
        hub = self.ipc.protocol.hub

        if len(params) == 2:
            did = int(params[1])
            device = hub.get_device(did)
            if device and device.type == "lighting":
                lc = LightingControl(self.ipc)
