import json
import time
import uuid
from types import SimpleNamespace

import websocket


def remove_nones(d):
    return {k: v for k, v in d.__dict__.items() if v is not None}


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""
    """https://gist.github.com/nlohmann/c899442d8126917946580e7f84bf7ee7"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


class BeoRemoteHaloConfig:
    version = '1.0.1'

    def __init__(self, pages):
        if type(pages) != list:
            pages = [pages]
        self.configuration = {'version': BeoRemoteHaloConfig.version, 'id': str(uuid.uuid1()), 'pages': pages}

    def to_json(self, indent=None):
        return json.dumps(self, default=lambda o: remove_empty_elements(remove_nones(o)), indent=indent)

    def __getitem__(self, item):
        for page in self.configuration['pages']:
            for button in page.buttons:
                if button.id == item:
                    return button
        return None

    class Page:
        def __init__(self, title, buttons=None):
            self.title = title
            self.id = str(uuid.uuid1())
            if type(buttons) != list:
                buttons = [buttons]
            self.buttons = buttons

    class Button:
        def __init__(self, title, content, subtitle=None, value=None, state=None, default=None):
            self.id = str(uuid.uuid1())
            self.title = title
            self.subtitle = subtitle
            self.value = value
            self.state = state
            self.content = content
            self.default = default

        def set_subtitle(self, subtitle=str()):
            self.subtitle = subtitle

        def set_value(self, value=int()):
            self.value = value

        def set_state(self, state=bool()):
            self.state = "active" if state else "inactive"

        def toggle_state(self):
            if self.state == "active":
                self.state = "inactive"
            else:
                self.state = "active"

        def set_default(self, default=bool()):
            self.default = default

    class ContentIcon:
        def __init__(self, icon):
            self.icon = icon

    class ContentText:
        def __init__(self, text):
            self.text = text


class BeoRemoteHaloUpdateButton:
    def __init__(self, id, content=None, title=None, subtitle=None, value=None, state=None):
        self.update = {"type": "button", "id": id, "content": content, "title": title, "subtitle": subtitle,
                       "value": value, "state": state}

    def to_json(self):
        return json.dumps(self, default=lambda o: remove_empty_elements(remove_nones(o)))


class BeoRemoteHalo:

    def __init__(self, host, configuration=None, on_status_event=None, on_power_event=None, on_system_event=None,
                 on_button_event=None, on_wheel_event=None):
        self.ws = websocket.WebSocketApp("ws://{0}:8080".format(host),
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_close=self.on_close)
        self.configuration = configuration
        self.verbose = True
        self.on_status_event = on_status_event
        self.on_power_event = on_power_event
        self.on_system_event = on_system_event
        self.on_button_event = on_button_event
        self.on_wheel_event = on_wheel_event
        self.events = [self.on_status_event, on_power_event, on_system_event, on_button_event, on_wheel_event]

    def set_verbosity(self, verbose):
        self.verbose = verbose

    def on_message(self, ws, message):
        if self.verbose:
            print(message)

        if any(self.events):
            event = json.loads(message, object_hook=lambda d: SimpleNamespace(**d)).event
            {
                'status': lambda msg: self.on_status_event(ws, msg),
                'power': lambda msg: self.on_power_event(ws, msg),
                'system': lambda msg: self.on_system_event(ws, msg),
                'button': lambda msg: self.on_button_event(ws, msg),
                'wheel': lambda msg: self.on_wheel_event(ws, msg)
            }[event.type](event)

    def on_close(self, ws, close_status_code, close_msg):
        if self.verbose:
            print("### Connection Closed ###")

    def on_open(self, ws):
        time.sleep(1)
        if self.configuration is not None:
            ws.send(self.configuration.to_json())
            if self.verbose:
                print(self.configuration.to_json(2))

    def connect(self):
        self.ws.run_forever()


class BeoremoteHaloExmaple(BeoRemoteHaloConfig):
    def __init__(self):
        kitchen_light = BeoRemoteHaloConfig.Button("Kitchen Light", BeoRemoteHaloConfig.ContentIcon("lights"))
        kitchen_light.set_value(95)
        kitchen_light.set_state(True)
        kitchen_light.set_subtitle("On")

        oven_timer = BeoRemoteHaloConfig.Button("Oven Timer", BeoRemoteHaloConfig.ContentText("01:35"))
        oven_timer.set_subtitle("Temperature 200°C")
        oven_timer.set_default(True)
        oven_timer.set_value(0)

        dining_table = BeoRemoteHaloConfig.Button("Dining Table", BeoRemoteHaloConfig.ContentIcon("lights"))
        dining_table.set_value(80)
        dining_table.set_state(False)
        dining_table.set_subtitle("Off")

        fireplace = BeoRemoteHaloConfig.Button("Fire Place", BeoRemoteHaloConfig.ContentIcon("fireplace"))
        fireplace.set_subtitle("Ignite")
        fireplace.set_state(False)

        blinds = BeoRemoteHaloConfig.Button("Blinds", BeoRemoteHaloConfig.ContentIcon("blinds"))
        blinds.set_subtitle("Closed")
        blinds.set_value(100)
        blinds.set_state(True)

        tv_back_light = BeoRemoteHaloConfig.Button("TV Backlight", BeoRemoteHaloConfig.ContentIcon("rgb_lights"))
        tv_back_light.set_subtitle("Off")
        tv_back_light.set_value(0)
        tv_back_light.set_state(False)

        living_room_thermostat = BeoRemoteHaloConfig.Button("Thermostat", BeoRemoteHaloConfig.ContentText("21°C"))
        living_room_thermostat.set_subtitle("Heating")
        living_room_thermostat.set_value(55)
        living_room_thermostat.set_default(True)
        living_room_thermostat.set_state(False)

        kitchen = BeoRemoteHaloConfig.Page("Kitchen", [kitchen_light, oven_timer, dining_table])
        living_room = BeoRemoteHaloConfig.Page("Kitchen", [fireplace, blinds, tv_back_light, living_room_thermostat])

        BeoRemoteHaloConfig.__init__(self, [kitchen, living_room])
