

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
$ pip install synlinkpy
```

### Examples

```python
from synlinkpy import SynLinkPy

pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

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
    print(inlet['id'], inlet['inletCurrentRms'], inlet["inletVoltageRms"])


# Modify Configuration 
# https://synaccess.com/support/webapi#configuration
pdu1.conf.set({"lcdOutletControlEnabled": False})

```

### HTTP API Documentation

<https://synaccess.com/support/webapi>

### Authentication

Authentication can occur with [Personal Access Token (PATs)](https://synaccess.com/support/webapi#personal-access-token-based) or Username & Password. It is recommended to use Personal Access Tokens.

**Authenticating with Username and Password**
```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

print(pdu1.device.info())
```

**Authenticating with Personal Access Token**
```python
pdu1 = SynLinkPy("http://192.168.1.100", { "token": "9wxBwnck6JpEH0b1DyI" })

print(pdu1.device.info())
```


### Python Library Commands

#### Outlet Commands

Outlet API Information
https://synaccess.com/support/webapi#outlets

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

# Change outlet state for a given PDU (Power Distribution Unit)
pdu1.outlets.set_state("1", "OFF") # accepts outlet number
pdu1.outlets.set_state("1-1200578", "ON") # accepts unique outlet ID
pdu1.outlets.set_state("2", "REBOOT") # acceptable states are "OFF", "ON", "REBOOT"

# Change outlet name for a given PDU
pdu1.outlets.change_config("1", { "outletName": "example name" })

# Get information of all outlets
outlet_response = pdu1.outlets.list()

for outlet in outlet_response:
    print(outlet['id'], outlet['outletName'], outlet['state'])

# OUTPUT
# 1-1200578 Outlet 1 ON
# 2-1200578 Rectifier #1 ON
# 3-1200578 Outlet 3 ON
# 4-1200578 Outlet 4 ON
```

#### Inlet Commands

Inlet API Information
https://synaccess.com/support/webapi#inlets

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

inlet_response = pdu1.inlets.list()
for inlet in inlet_response:
    print(inlet['id'], inlet['inletPlug'], inlet['inletCurrentRms'] )

# OUTPUT
# I1-1000036 0.0 117.4000015258789
```


#### Bank Commands

Bank API Information
https://synaccess.com/support/webapi#banks

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

banks_response = pdu1.banks.list()

for bank in banks_response:
    print(bank['id'], bank['currentRms'])

# OUTPUT
# 1200578 0.0
```


#### Device Commands

Device API Information
https://synaccess.com/support/webapi#device

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

device_response = pdu1.device.info() 

print (device_response['modelNumber'], device_response['enclosureSerialNumber'], device_response['formFactor'])

# OUTPUT
# 5001AIE-0E 1000036 Compact
```

#### Groups Commands

Groups API Information
https://synaccess.com/support/webapi#groups

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

groups_response = pdu1.groups.list()
for group in groups_response:
    print(group['id'], group['groupName'], group["outlets"])

# OUTPUT
# 1 Example Group [...] 
# 2 Important Equipment [...]
# 3 Non Essential Equipment [...]

# Create new group with name, to add outlets use groups.modify
pdu1.groups.create("Example Name")

# outlets value must be an array and will override pre-existing outlet's value. First argument is group ID
pdu1.groups.modify(1, { "outlets": ["1-200578", "3-200578"] })

# switch all outlets of the group, will switch according to sequencing time setting
pdu1.groups.set_state(1, "OFF")

# permanently remove based off of group ID
pdu1.groups.delete(1)

```

#### Configuration Commands

Configuration API Information
https://synaccess.com/support/webapi#configuration

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

conf_response = pdu1.conf.list()
print(conf_response["macAddr"], conf_response["deviceName"], conf_response["lcdOrientation"])

# OUTPUT
# 0C:73:EB:BE:00:27 Demo Compact PDU 90

# Set configuration with key value pairs
pdu1.conf.set({ "lcdOutletControlEnabled" : False })

```

#### Sensors Commands

Sensors API Information
https://synaccess.com/support/webapi#sensors

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

sensors_response = pdu1.sensors.list()
for sensor in sensors_response:
    print(sensor['sensorPort'], sensor['sensorName'], sensor['sensorTempInC'], sensor['sensorHumidity'])

# OUTPUT
# B Temperature & Humidity Sensor 22.9057 39.50677

```


#### Event & Action Commands

Events API Information
https://synaccess.com/support/webapi#events

Actions API Information
https://synaccess.com/support/webapi#actions

```python
pdu1 = SynLinkPy("http://192.168.1.100", { "username": "admin", "password": "admin" })

# List all events
event_response = pdu1.events.list()
for events in event_response:
    print(events['id'], events['name'], events['code'], events['params'], events['actions'], events['triggered'])
# OUTPUT
# 1 Example High Current Event for Bank #1 31 ['2003757', '16', '10'] [] False


# List all actions
action_response = pdu1.actions.list()
for actions in action_response:
    print(actions['id'], actions['name'], actions['code'], actions['params'])
# OUTPUT
#1 Example Power Cycle for Outlet #1 12 ['1-2003757', '', '']

# Create an action
example_action = pdu1.actions.create({ "name": "example reboot", "code": 12, "params": ["1-2003757","",""] })

# Create an event
example_event pdu1.events.create({"name": "example outlet current event", "code": 46, "params": ["1-2003757", "0.2", "3"], "actions": []})

# Modify an event
pdu1.events.modify(example_event['id'], "actions": [example_action['id']])

# Modify an action
pdu1.actions.modify(example_action['id'], { "name": "example reboot 2", "code": 12, "params": ["2-2003757","",""] })

# Delete an event
pdu1.events.delete(example_event['id'])

# Delete an action
pdu1.actions.delete(example_action['id'])


