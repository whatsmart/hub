#!/usr/bin/env python3

class ILightingControl(object):
    def __init__(self, ipc = None):
        self.ipc = ipc

    def handle(self):
        pass
