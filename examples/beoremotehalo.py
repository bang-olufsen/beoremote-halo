"""
The MIT License (MIT)

Copyright (c) 2021 Bang & Olufsen a/s

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import time
import uuid
from types import SimpleNamespace

import websocket


def remove_nones(dictionary):
    """

    :param dictionary:
    :return:
    """
    return {k: v for k, v in dictionary.__dict__.items() if v is not None}


def remove_empty_elements(dictionary):
    """
    recursively remove empty lists, empty dicts, or None elements from a dictionary
    https://gist.github.com/nlohmann/c899442d8126917946580e7f84bf7ee7

    :param dictionary
    """

    def empty(check_object):
        """

        :param check_object:
        :return:
        """
        return check_object is None or check_object == {} or check_object == []

    if not isinstance(dictionary, (dict, list)):  # pylint: disable=no-else-return
        return dictionary
    elif isinstance(dictionary, list):
        return [v for v in (remove_empty_elements(v) for v in dictionary) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in dictionary.items()) if
                not empty(v)}


class BeoRemoteHaloConfig:
    """
    Configuration object for Beoremote Halo tied to spec available at
    https://bang-olufsen.github.io/beoremote-halo/
    """
    version = '1.0.1'

    def __init__(self, pages):
        if isinstance(pages, list):
            pages = [pages]
        self.configuration = {'version': BeoRemoteHaloConfig.version, 'id': str(uuid.uuid1()),
                              'pages': pages}

    def to_json(self, indent=None) -> str:
        """

        :param indent:
        :return:
        """
        return json.dumps(self, default=lambda o: remove_empty_elements(remove_nones(o)),
                          indent=indent)

    def __getitem__(self, item):
        for page in self.configuration['pages']:
            for button in page.buttons:
                if button.id == item:
                    return button
        return None

    class Page:  # pylint: disable=too-few-public-methods
        """
        Page object
        """

        def __init__(self, title: str, buttons=None):
            self.title = title
            self.id = str(uuid.uuid1())  # pylint: disable=invalid-name
            if isinstance(buttons, list):
                buttons = [buttons]
            self.buttons = buttons

    class Button:
        """
        Button object
        """

        # pylint: disable=too-many-arguments
        def __init__(self, title, content, subtitle=None, value=None, state=None, default=None):
            self.id = str(uuid.uuid1())  # pylint: disable=invalid-name
            self.title = title
            self.subtitle = subtitle
            self.value = value
            self.state = state
            self.content = content
            self.default = default

        def set_subtitle(self, subtitle: str):
            """

            :param subtitle:
            """
            self.subtitle = subtitle

        def set_value(self, value: int):
            """

            :param value:
            """
            self.value = value

        def set_state(self, state: bool):
            """

            :param state:
            """
            self.state = "active" if state else "inactive"

        def toggle_state(self):
            """
            Toggle button active/inactive state
            """
            if self.state == "active":
                self.state = "inactive"
            else:
                self.state = "active"

        def set_default(self, default=bool()):
            """

            :param default:
            """
            self.default = default

    class ContentIcon:  # pylint: disable=too-few-public-methods
        """
        Button Content for icons
        """

        def __init__(self, icon):
            self.icon = icon

    class ContentText:  # pylint: disable=too-few-public-methods
        """
        Button Content for text
        """

        def __init__(self, text):
            self.text = text


class BeoRemoteHaloUpdateButton:  # pylint: disable=too-few-public-methods
    """
    Update object for Buttons
    """

    # pylint: disable=too-many-arguments
    def __init__(self, button_id, content=None, title=None, subtitle=None, value=None, state=None):
        self.update = {"type": "button", "id": button_id, "content": content, "title": title,
                       "subtitle": subtitle,
                       "value": value, "state": state}

    def to_json(self):
        """

        :return:
        """
        return json.dumps(self, default=lambda o: remove_empty_elements(remove_nones(o)))


class BeoRemoteHalo:  # pylint: disable=too-many-instance-attributes
    """
    Beoremote connection controller
    Creates and maintain a websocket to Beoremote Halo on port 8080

    Add callbacks to received events from Beoremote Halo
    Supported callbacks
        - Status event
        - Power event
        - System Event
        - Button Event
    """

    # pylint: disable=too-many-arguments
    def __init__(self, host, configuration=None, on_status_event=None, on_power_event=None,
                 on_system_event=None,
                 on_button_event=None, on_wheel_event=None):
        self.websocket = websocket.WebSocketApp("ws://{0}:8080".format(host),
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
        self.events = [self.on_status_event, on_power_event, on_system_event, on_button_event,
                       on_wheel_event]

    def set_verbosity(self, verbose):
        """

        :param verbose:
        """
        self.verbose = verbose

    def on_message(self, web_socket, message):
        """

        :param web_socket:
        :param message:
        """
        del web_socket
        if self.verbose:
            print("Halo -> client: {}".format(message))

        if any(self.events):
            event = json.loads(message, object_hook=lambda d: SimpleNamespace(**d)).event
            {
                'status': lambda msg: self.on_status_event(self, msg),
                'power': lambda msg: self.on_power_event(self, msg),
                'system': lambda msg: self.on_system_event(self, msg),
                'button': lambda msg: self.on_button_event(self, msg),
                'wheel': lambda msg: self.on_wheel_event(self, msg)
            }[event.type](event)

    def send(self, update):
        """

        :param update:
        """
        message = update if isinstance(update, str) else update.to_json()
        if self.verbose:
            print("Client -> Halo: {}".format(message))
        self.websocket.send(message)

    def on_close(self, web_socket, close_status_code, close_msg):
        """

        :param web_socket:
        :param close_status_code:
        :param close_msg:
        """
        del web_socket, close_status_code, close_msg
        if self.verbose:
            print("### Connection Closed ###")

    def on_open(self, web_socket):
        """
        Open connection to Beoremote Halo send the configuration
        :param web_socket:
        """
        del web_socket
        time.sleep(1)
        if self.configuration is not None:
            self.send(self.configuration)

    def connect(self):
        """
        Connect to Beoremote Halo
        """
        self.websocket.run_forever()


class BeoremoteHaloExmaple(BeoRemoteHaloConfig):  # pylint: disable=too-few-public-methods
    """
    Example configuration for Beoremote Halo
    """

    def __init__(self):
        kitchen_light = BeoRemoteHaloConfig.Button("Kitchen Light",
                                                   BeoRemoteHaloConfig.ContentIcon("lights"))
        kitchen_light.set_value(95)
        kitchen_light.set_state(True)
        kitchen_light.set_subtitle("On")

        oven_timer = BeoRemoteHaloConfig.Button("Oven Timer",
                                                BeoRemoteHaloConfig.ContentText("01:35"))
        oven_timer.set_subtitle("Temperature 200°C")
        oven_timer.set_default(True)
        oven_timer.set_value(0)

        dining_table = BeoRemoteHaloConfig.Button("Dining Table",
                                                  BeoRemoteHaloConfig.ContentIcon("lights"))
        dining_table.set_value(80)
        dining_table.set_state(False)
        dining_table.set_subtitle("Off")

        fireplace = BeoRemoteHaloConfig.Button("Fire Place",
                                               BeoRemoteHaloConfig.ContentIcon("fireplace"))
        fireplace.set_subtitle("Ignite")
        fireplace.set_state(False)

        blinds = BeoRemoteHaloConfig.Button("Blinds", BeoRemoteHaloConfig.ContentIcon("blinds"))
        blinds.set_subtitle("Closed")
        blinds.set_value(100)
        blinds.set_state(True)

        tv_back_light = BeoRemoteHaloConfig.Button("TV Backlight",
                                                   BeoRemoteHaloConfig.ContentIcon("rgb_lights"))
        tv_back_light.set_subtitle("Off")
        tv_back_light.set_value(0)
        tv_back_light.set_state(False)

        living_room_thermostat = BeoRemoteHaloConfig.Button("Thermostat",
                                                            BeoRemoteHaloConfig.ContentText("21°C"))
        living_room_thermostat.set_subtitle("Heating")
        living_room_thermostat.set_value(55)
        living_room_thermostat.set_default(True)
        living_room_thermostat.set_state(False)

        kitchen = BeoRemoteHaloConfig.Page("Kitchen", [kitchen_light, oven_timer, dining_table])
        living_room = BeoRemoteHaloConfig.Page("Kitchen", [fireplace, blinds, tv_back_light,
                                                           living_room_thermostat])

        BeoRemoteHaloConfig.__init__(self, [kitchen, living_room])
