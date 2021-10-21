# Examples

This directory contains three examples

1. Connect and
   Listen: [connect_and_listen.py](https://github.com/bang-olufsen/beoremote-halo/blob/main/examples/connect_and_listen.py)

   Creates a websocket client to Beoremote Halo on port 8080 and listen for event
   ```
   python connect_and_listen.py connect_and_listen.py BeoremoteHalo-XXXXXXXX.local
   Halo -> client: {"event":{"type":"system","state":"active"}}
   Halo -> client: {"event":{"type":"power","capacity":100,"state":"discharging"}}
   Halo -> client: {"event":{"type":"power","capacity":100,"state":"discharging"}}
   ...
   ```
2. Connect and
   Configure: [connect_and_configure.py](https://github.com/bang-olufsen/beoremote-halo/blob/main/examples/connect_and_configure.py)

   Creates a websocket client to Beoremote Halo on port 8080 and sends
   an [example configuration](https://github.com/bang-olufsen/beoremote-halo/blob/main/examples/beoremotehalo.py#L292)
    ```
    $ python connect_and_configure.py BeoremoteHalo-XXXXXXXX.local
    Client -> Halo: {"configuration": {"version": "1.0.1", ...}}
    Halo -> client: {"event":{"type":"system","state":"active"}}
    Halo -> client: {"event":{"type":"power","capacity":100,"state":"discharging"}}
    Halo -> client: {"event":{"type":"status","state":"ok","message":"Configuration"}}
    ...
    ```
3. Connect and
   Interact: [connect_and_interact.py](https://github.com/bang-olufsen/beoremote-halo/blob/main/examples/connect_and_interact.py)

   Creates a websocket client to Beoremote Halo on port 8080 and sends
   an [example configuration](https://github.com/bang-olufsen/beoremote-halo/blob/main/examples/beoremotehalo.py#L292)
   while also reaction to events received from Halo. The callbaks are located here and each handle a specific type of
   event.

   `on_system_event` is provided but unused in this example.

   `on_wheel_event` changes the indicator ring on the centered/controlled button.

   `on_button_event` Changed the active/inactive state of a button, will start/pause/resume the timer if the "Oven Timer" button is pressed.

   ```
   $ python connect_and_interact.py BeoremoteHalo-XXXXXXXX.local
   Client -> Halo: {"configuration": {"version": "1.0.1", ...}}
   Halo -> client: {"event":{"type":"system","state":"active"}}
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
