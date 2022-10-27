

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

pdu1 = SynLinkPy("HTTP_API_TOKEN", "IP_ADDRESS")

# Change outlet state for a given PDU (Power Distribution Unit)
pdu1.outlets.set_state("1", "OFF") # accepts outlet number
pdu1.outlets.set_state("1-1200578", "ON") # accepts unique outlet ID
pdu1.outlets.set_state("2", "REBOOT") # acceptable states are "OFF", "ON", "REBOOT"
# returns outlet state?

# Get information of all outlets
outlet_response = pdu1.outlets.list()
outlets = outlet_response.body['outlets']

# Get information on inlet(s)
inlet_response = pdu1.inlets.list()
inlets = inlet_response.body['inlets']

# Modify Configuration 
# https://synaccess.com/support/webapi#configuration
pdu1.config.set("lcdOutletControlEnabled", false)

```

### Documentation

<https://synaccess.com/support/webapi>
