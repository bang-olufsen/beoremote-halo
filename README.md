# Beoremote Halo

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20CI%20silver%20wall.png" width=40% height=40% align="right">




Welcome to the public GitHub page for the Bang & Olufsen Beoremote Halo.
Beoremote Halo gives you all the convenience of a simple user interface to operate your Bang & Olufsen music system. When you get close to Beoremote Halo, the display lights up and offers you a one button press to select your music. There is no need to use your mobile device or to pull anything out of your pocket and fiddle around trying to find the right app to get started. With the Home Automation System API your remote can also be extended to control your Home.
<br />
<br />
You can find out more about Beoremote Halo on the Bang & Olufsen retail website [here](https://www.bang-olufsen.com/en/us/accessories/beoremote-halo)
<br />
<br />
<br />

## API
The Home Automation System API is an open source Async API that allows you to interact with a Beoremote Halo from a control system.
Using a websocket to communicate with the Beoremote Halo, it is possible to create a configuration of buttons on the Beoremote Halo to work with your Home automation and control all your Home Automation systems with an easily accessible and well crafted remote.
The API works with both the wall mounted and table versions of the Beoremote Halo.
Beoremote Halo supports adding buttons with icons or text for most general Home automation applications.
<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20flow%200.png" width=100% height=100% align="center">
<br />

### Connecting to Beoremote Halo
Connection to Beoremote Halo is done using a websocket client and connecting to Beoremote Halos Websocket server using Beoremote Halos IP address on Port:8080.
Once connection is established a configuration must be sent to Beoremote Halo for it to configure the screens and buttons.
The Beoremote Halo will answer back if the configuration was successful or not.
<br />
The following MSC chart shows an example of sending a configuration with 1 button on a screen and then pressing that button.

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo_MSC_config_button_press.png" width=70% height=70% align="center">

For further details on the Open API including list of commands, examples and icons please also refer to the API description [here](https://bang-olufsen.github.io/beoremote-halo/)

Below you will also find some examples in Python to get you started.

## Python Package: `beoremote-halo`
The python package `beoremote-halo` contains a python library for communicating to Beoremote Halo and a command line tool for discovering Beoremote Halo on the network.

Install using pip:
```
$ pip3 install beoremote-halo
```
Scan for Beoremote Halo on the network by running in the terminal
```
$ beoremote-halo scan
If Beoremote Halo does not appear on the list, try waking it up while discovery in running.
Press enter to exit...

BeoremoteHalo-XXXXXXXX.local
...
```
To tryout the Home Automation controls on Beoremote Halo run the bundle demo using the discovered Beoremote Halo hostname:
```
$ beoremote-halo demo --hostname BeoremoteHalo-XXXXXXXX.local
```



### "beoremote-halo" usage
Listen for events from Beoremote Halo using the `beoremote-halo` tool. It will create a websocket client and connect to Beoremote Halo on port 8080 and listen for events
```
$ beoremote-halo listen --hostname BeoremoteHalo-XXXXXXXX.local
Halo -> client: {"event":{"type":"system","state":"active"}}
Halo -> client: {"event":{"type":"power","capacity":100,"state":"discharging"}}
Halo -> client: {"event":{"type":"power","capacity":100,"state":"discharging"}}
...
 ```
### Interactive demo
This demo creates a websocket client to Beoremote Halo on port 8080. Configures Beoremote Halo and reaction to events received from Halo. The callbacks are located here and each handle a specific type of event.

`on_system_event` is provided but unused in this example.

`on_wheel_event` changes the indicator ring on the centered/controlled button.

`on_button_event` Changed the active/inactive state of a button, will start/pause/resume the timer if the "Oven Timer" button is pressed.

```
$ beoremote-halo demo --hostname BeoremoteHalo-XXXXXXXX.local
Halo -> client: {"event":{"type":"system","state":"active"}}
Client -> Halo: {"configuration": {"version": "1.0.1", ...}}
Halo -> client: {"event":{"type":"status","state":"ok","message":"Configuration"}}
Halo -> client: {"event":{"type":"button","id":"c7f6247f-3260-11ec-bd30-51f891360684","state":"pressed"}}
Halo -> client: {"event":{"type":"button","id":"c7f6247f-3260-11ec-bd30-51f891360684","state":"released"}}
Client -> Halo: {"update": {"type": "button", "id": "c7f6247f-3260-11ec-bd30-51f891360684", "state": "active"}}
Halo -> client: {"event":{"type":"status","state":"ok","message":"Update"}}
Client -> Halo: {"update": {"type": "button", "id": "c7f6247f-3260-11ec-bd30-51f891360684", "content": {"text": "01:35"}}}
Halo -> client: {"event":{"type":"status","state":"ok","message":"Update"}}
...
Client -> Halo: {"update": {"type": "button", "id": "c7f6247f-3260-11ec-bd30-51f891360684", "content": {"text": "01:22"}}}
Halo -> client: {"event":{"type":"status","state":"ok","message":"Update"}}
...
```
### Getting started with `beoremote-halo` package
In the following example a client instance is created and connects to a Beoremote Halo and listens for events. When a `SystemEvent` is received the `on_system_event` callback is executed and prints the Beoremote Halo's system state.
```python
from beoremote.beoremotehalo import BeoremoteHalo
from beoremote.systemEvent import SystemEvent

def on_system_event(client: BeoremoteHalo, event: SystemEvent):
    print("System event: {}".format(event.state))

remote = BeoremoteHalo(
    host="BeoremoteHalo-XXXXXXXX.local",
    on_system_event=on_system_event
)
remote.set_verbosity(True)
remote.connect()
```
