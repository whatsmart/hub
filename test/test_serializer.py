#!/usr/bin/env python3

from hub.base.hipc import HIPCSerializer

ser = HIPCSerializer()
#ser.set_version("2.0")
ser.set_type("request")
ser.set_resource("component")
ser.set_pid(123)
ser.set_rid(456)
ser.set_origin("component/123")
ser.set_body('{"jsonrpc": "2.0","method": "register_component", "params": {"name": "wifi_link_adapter","type": "link_adapter"}, "id": 1}')
print(ser.serialize())
