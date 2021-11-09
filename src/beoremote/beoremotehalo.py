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

import time
import uuid

import websocket

from beoremote.configuration import Configuration
from beoremote.event import Event
from beoremote.icons import Icons
from beoremote.statusEvent import StatusEvent
from beoremote.systemEvent import SystemEvent
from beoremote.text import Text


class BeoremoteHalo:  # pylint: disable=too-many-instance-attributes
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

    def __init__(
        self,
        host,
        configuration=None,
        on_status_event=None,
        on_power_event=None,
        on_system_event=None,
        on_button_event=None,
        on_wheel_event=None,
    ):  # pylint: disable=too-many-arguments
        self.websocket = websocket.WebSocketApp(
            "ws://{0}:8080".format(host),
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
        )
        self.configuration = configuration
        self.verbose = False
        self.on_status_event = on_status_event
        self.on_power_event = on_power_event
        self.on_system_event = on_system_event
        self.on_button_event = on_button_event
        self.on_wheel_event = on_wheel_event
        self.reconnect = True
        self.configured = False
        self.reconnect_attempts = 3
        self.attempts = 3
        self.ping_interval = 30
        self.ping_timeout = 5
        self.events = any(
            [
                self.on_status_event,
                self.on_power_event,
                self.on_system_event,
                self.on_button_event,
                self.on_wheel_event,
            ]
        )

    def set_auto_reconnect(self, reconnect: bool, attempts: int):
        self.reconnect = reconnect
        self.attempts = attempts
        self.reconnect_attempts = attempts

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

        event = Event.from_json(message).event
        {
            "status": lambda msg: (
                self._on_status_event_callback(msg),
                self.on_status_event(self, msg),
            ),
            "power": lambda msg: self.on_power_event(self, msg),
            "system": lambda msg: (
                self._on_system_event_callback(msg),
                self.on_system_event(self, msg),
            ),
            "button": lambda msg: self.on_button_event(self, msg),
            "wheel": lambda msg: self.on_wheel_event(self, msg),
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
        self.reconnect = False

    def _on_status_event_callback(self, event: StatusEvent):
        if (
            isinstance(event, StatusEvent)
            and event.state == StatusEvent.State.ok
            and event.message == "Configuration"
        ):
            self.configured = True
            self.reconnect_attempts = self.attempts

    def _on_system_event_callback(self, event: SystemEvent):
        if (
            self.configured is False
            and event.state == SystemEvent.State.active
            and self.configuration is not None
        ):
            self.send(self.configuration)

    def on_open(self, web_socket):
        """
        Open connection to Beoremote Halo send the configuration
        :param web_socket:
        """
        del web_socket

        if self.verbose:
            print("### Connection Open ###")

    def connect(self):
        """
        Connect to Beoremote Halo
        """
        while self.reconnect and self.reconnect_attempts > 0:
            status = self.websocket.run_forever(
                ping_interval=self.ping_interval, ping_timeout=self.ping_timeout
            )
            self.reconnect_attempts = self.reconnect_attempts - 1
            self.configured = False
            if status is True and self.reconnect:
                print(
                    "### Connection to server lost, retrying again in 30 seconds ({}/{} attempts) "
                    "###".format(self.attempts - self.reconnect_attempts, self.attempts)
                )
                time.sleep(30)  # wait 30 second before trying to reconnect
            else:
                self.reconnect = False


class BeoremoteHaloExmaple(Configuration):
    """
    Example configuration for Beoremote Halo
    """

    def __init__(self):
        kitchen_light = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Kitchen Light",
            "On",
            95,
            Configuration.Configuration.Pages.Buttons.State.ACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        oven_timer = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Oven Timer",
            "Temperature 200°C",
            0,
            Configuration.Configuration.Pages.Buttons.State.INACTIVE,
            Text("01:35"),
            True,
        )

        dining_table = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Dining Table",
            "Off",
            80,
            Configuration.Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        fireplace = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Fire Place",
            "Ignite",
            None,
            Configuration.Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        blinds = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Blinds",
            "Closed",
            100,
            Configuration.Configuration.Pages.Buttons.State.ACTIVE,
            Icons(Icons.Icon.BLINDS),
        )

        tv_back_light = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "TV Backlight",
            "off",
            0,
            Configuration.Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.RGB_LIGHTS),
        )

        living_room_thermostat = Configuration.Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Thermostat",
            "Heating",
            55,
            Configuration.Configuration.Pages.Buttons.State.INACTIVE,
            Text("21°C"),
            True,
        )

        kitchen = Configuration.Configuration.Pages(
            "Kitchen", str(uuid.uuid1()), [kitchen_light, oven_timer, dining_table]
        )

        living_room = Configuration.Configuration.Pages(
            "living room",
            str(uuid.uuid1()),
            [fireplace, blinds, tv_back_light, living_room_thermostat],
        )

        Configuration.__init__(
            self, Configuration.Configuration(str(uuid.uuid1()), [kitchen, living_room])
        )
