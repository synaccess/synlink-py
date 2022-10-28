#!/usr/bin/env python
"""List outlets in PDU"""


from synlink_py import SynLinkPy

# compactPdu1 = SynLinkPy("http://192.168.1.179", "9wxBwnck6JhEH0b1DyI")
compactPdu1 = SynLinkPy("http://192.168.1.179", { "token": "9wxBwnck6JhEH0b1DyI" })

# compactPdu1 = SynLinkPy("http://192.168.1.179", { "token": "9wxBwnck6JhEH0b1DyI" })
switchedPdu1 = SynLinkPy("http://192.168.1.103", { "username": "admin", "password": "admin" })

# compact_outlets = compactPdu1.outlets.list()
# switched_outlets = switchedPdu1.outlets.list()
print(switchedPdu1.outlets.list())
print(compactPdu1.inlets.list())
# print("--------")
# for outlet in switched_outlets:
#     print(outlet['id'], outlet['outletName'], outlet['state'])
# print("--------")

# print("state of outlet1:", switched_outlets[0]['state'], switched_outlets[0]['state'] == 'ON')

# print("state of outlet2:", switched_outlets[1]['state'], switched_outlets[1]['state'] == 'ON')


# if (switched_outlets[0]['state'] == 'ON'):
#     switchedPdu1.outlets.set_state(1, 'OFF')
#     print("Switched PDU outlet 1 is now OFF") 
# else:
#     switchedPdu1.outlets.set_state(1, 'ON')
#     print("Switched PDU outlet 1 is now ON")


# if (switched_outlets[1]['state'] == 'ON'):
#     switchedPdu1.outlets.set_state(2, 'OFF')
#     print("Switched PDU outlet 2 is now OFF") 
# else:
#     switchedPdu1.outlets.set_state(2, 'ON')
#     print("Switched PDU outlet 2 is now ON")



# switchedPdu1.outlets.set_state(1, "OFF")