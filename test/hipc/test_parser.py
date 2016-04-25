#!/usr/bin/env python3

from hub.base.hipc import HIPCParser

msg = b"""asdfHIPC/1.0 request device/1\r\nlength: 120\r\nchecksum: 1444936211\r\nrt-component: 0\r\n\r\n{"jsonrpc": "2.0","method": "register_component","params": {"name": "wifi_link_adapter","type": "link_adapter"},"id": 1}woefiowefoihfwHIPC/1.0 request device/1\r\nlength: 120\r\nchecksum: 1444936211\r\nrt-component: 0\r\n\r\n{"jsonrpc": "2.0","method": "register_component","params": {"name": "wifi_link_adapter","type": "link_adapter"},"id": 1}fwoijwopf"""

class A(object):
    def handle_ipc(ipc):
        print(p.get_version())
        print(p.get_type())
        if p.get_type() == "request":
            print(p.get_resource())
        for k in p.get_headers().keys():
            print(k, p.get_headers()[k], sep=" ")
        print(p.get_body())

p = HIPCParser()
p.set_protocol(A)
p.parse(msg)
