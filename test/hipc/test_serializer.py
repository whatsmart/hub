#!/usr/bin/env python3

from hub.base.hipc import HIPCRequestSerializer

ser = HIPCRequestSerializer("device/1")
#ser.set_header("rt-component", "0")
ser.set_body('{"jsonrpc": "2.0","method": "register_component", "params": {"name": "wifi_link_adapter","type": "link_adapter"}, "id": 1}')
print(ser.serialize())
