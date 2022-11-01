

SynLink Python Library
-------
<!-- 
![pypi](https://img.shields.io/pypi/v/Slacker.svg)\_ ![build
status](https://img.shields.io/travis/os/slacker.svg)\_ ![pypi
downloads](https://img.shields.io/pypi/dm/slacker.svg)\_
![license](https://img.shields.io/github/license/os/slacker.svg)\_
![gitter chat](https://badges.gitter.im/Join%20Chat.svg)\_

![image](https://raw.githubusercontent.com/os/slacker/master/static/slacker.jpg) -->

### About

SynLink Python Library is a Python interface for the [SynLink Smart PDU API](https://synaccess.com/support/webapi).

### Installation

```bash
$ pip install synlink_py
```

### Examples

```python
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

```

### HTTP API Documentation

<https://synaccess.com/support/webapi>

### Commands

#### Outlet Commands

```python
pdu1 = SynLinkPy("IP_ADDRESS", "HTTP_API_TOKEN")

# Change outlet state for a given PDU (Power Distribution Unit)
pdu1.outlets.set_state("1", "OFF") # accepts outlet number
pdu1.outlets.set_state("1-1200578", "ON") # accepts unique outlet ID
pdu1.outlets.set_state("2", "REBOOT") # acceptable states are "OFF", "ON", "REBOOT"

# Get information of all outlets
outlet_response = pdu1.outlets.list()
for outlet in outlet_response:
    print(outlet['id'], outlet['outletName'], outlet['state'])

```

#### Inlet Commands

```python
pdu1 = SynLinkPy("IP_ADDRESS", "HTTP_API_TOKEN")

inlet_response = pdu1.inlets.list()

for inlet in inlet_response:
    print(inlet['id'], inlet['inletCurrentRms'])

```


#### Bank Commands

```python
pdu1 = SynLinkPy("IP_ADDRESS", "HTTP_API_TOKEN")

banks_response = pdu1.banks.list()

for bank in banks_response:
    print(bank['id'], bank['currentRms'])

```

