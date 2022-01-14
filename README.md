
[<img src="https://github.com/bang-olufsen/beoremote-halo/raw/main/docs/images/Beoremote_Halo.png" width="30%">](https://www.bang-olufsen.com/en/us/accessories/beoremote-halo)
# Beoremote Halo Open API
[![build](https://github.com/bang-olufsen/beoremote-halo/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/bang-olufsen/beoremote-halo/actions/workflows/ci.yaml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Version](https://img.shields.io/pypi/v/beoremote-halo?color=g)](https://pypi.org/project/beoremote-halo)
[![Downloads](https://img.shields.io/pypi/dm/beoremote-halo)](https://pypi.org/project/beoremote-halo)


The [Beoremote Halo](https://www.bang-olufsen.com/en/us/accessories/beoremote-halo) Open API is an open source async API that allows you to interact with a Beoremote Halo from a home automation system.
<br />
<br />
Using a WebSocket to communicate with the Beoremote Halo, it is possible to create a configuration of buttons to interact with your home automation to control your home applications.
<br />
<br />
Beoremote Halo supports buttons with icons or text for most general home automation applications.
You can find a list of the [supported icons](https://github.com/bang-olufsen/beoremote-halo/wiki/Icons) on our wiki pages.
For further details on the Open API list of commands please refer to the [API description](https://bang-olufsen.github.io/beoremote-halo/).
<br />


## Installation
The Python package `beoremote-halo` requires [Python 3.9](https://www.python.org/downloads/) or higher and contains a library for communicating with Beoremote Halo and a CLI tool for discovering Beoremote Halo on the network.

Install using pip:
```
pip3 install beoremote-halo
```

## Basic Usage
In the following example a client instance connects to Beoremote Halo and listens for events. When a `SystemEvent` is received the `on_system_event` callback is executed and prints the Beoremote Halo's system state. Please refer to the [API](https://bang-olufsen.github.io/beoremote-halo) for details on each type of event.
```python
from beoremote import Halo
from beoremote.events import SystemEvent

def on_system_event(client: Halo, event: SystemEvent):
    print(event)


remote = Halo("BeoremoteHalo-xxxxxxxx.local")
remote.set_on_system_event_callback(on_system_event)
remote.connect()
```

## Example
Use the `beoremote-halo` CLI tool to discover and then run a demo by connecting to your Beoremote Halo.

<img src="https://github.com/bang-olufsen/beoremote-halo/raw/main/docs/images/beoremote-halo-demo.gif">

In the above demo the CLI is used to locate Beoremote Halo on the network.
```
beoremote-halo scan
```
Afterwards the CLI demo is run by passing the serial number of the discovered Beoremote Halo.
```
beoremote-halo demo --serial xxxxxxxx
```
The demo configures the Beoremote Halo and reacts to events received from Halo. The callbacks each handle a specific type of [event](https://bang-olufsen.github.io/beoremote-halo/#message-event).

`on_system_event` is provided but unused in this example.

`on_wheel_event` changes the indicator ring on the centered/controlled button.

`on_button_event` changes the active/inactive state of a button, will start/pause/resume the timer if the "Oven Timer" button is pressed.
