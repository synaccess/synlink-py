#!/usr/bin/env python
"""List outlets in PDU"""


from synlink_py import SynLinkPy

from synlink_py import SynLinkPy

pdu1 = SynLinkPy("IP_ADDRESS", "HTTP_API_TOKEN")

# Change outlet state for a given PDU (Power Distribution Unit)
pdu1.outlets.set_state("1", "OFF") # accepts outlet number
pdu1.outlets.set_state("1-1200578", "ON") # accepts unique outlet ID
pdu1.outlets.set_state("2", "REBOOT") # acceptable states are "OFF", "ON", "REBOOT"

# Get information of all outlets
outlet_response = pdu1.outlets.list()
for outlet in outlet_response:
    print(outlet['id'], outlet['outletName'], outlet['state'])

# Get information on inlet(s)
inlet_response = pdu1.inlets.list()
inlets = inlet_response.body['inlets']

# Modify Configuration 
# https://synaccess.com/support/webapi#configuration
pdu1.config.set("lcdOutletControlEnabled", false)
