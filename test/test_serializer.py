#/usr/bin/env python3

from hub.base.hipc import HIPCSerializer

ser = HIPCSerializer()
ser.set_type("request")
ser.set_interface("component")
ser.set_body('{"jsonrpc": "2.0","method": "register_component", "params": {"name": "wifi_link_adapter","type": "link_adapter"}, "id": 1}')
print(ser.serialize())
