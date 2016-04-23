#!/usr/bin/env python3

from .idevice import IDevice
from .ilightingcontrol import ILightingControl
from .ilinkadapter import ILinkAdapter

class IControl(object):

    def __init__(self, ipc):
        self.ipc = ipc
        self.hub = self.ipc.get_protocol().hub

    def handle_ipc(self):
        resource = self.ipc.get_resource()
        resource = resource.split("/")

        if len(resource) == 2:
            did = int(resource[1].strip())
            idev = IDevice(self.ipc)
            device = idev.get_device(did)
            if device and device.type.lower() == "lighting".lower():
                lc = ILightingControl(self.ipc)
                lc.handle_ipc()
            elif device and device.type.lower() == "linkAdapter".lower():
                lc = ILinkAdapter(self.ipc)
                lc.handle_ipc()
