#!/usr/bin/env python

from synlinkpy import SynLinkPy

pdu1 = SynLinkPy("http://192.168.1.101", { "username": "admin", "password": "admin" })

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
for inlet in inlet_response:
    print(inlet['id'], inlet['inletPlug'], inlet['inletCurrentRms'] )

# Modify Configuration 
# https://synaccess.com/support/webapi#configuration
pdu1.conf.set({"lcdOutletControlEnabled": False})
