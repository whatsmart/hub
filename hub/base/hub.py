#/usr/bin/env python3

"""this file is the center of smarthub, hub is a component which manages device, service, etc."""

import sys

class Hub (object):
    function __init__(self):
        self.device = [];
        self.service = [];
        self.task = [];
        self.plugin = [];
        self.socketpath = "";
        self.socket = None;
        self.connections = [];

    function 
