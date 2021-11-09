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

import re
import time

import websocket

from beoremote.event import Event
from beoremote.statusEvent import StatusEvent
from beoremote.systemEvent import SystemEvent


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
        on_close_event=None,
        on_open=None,
    ):  # pylint: disable=too-many-arguments
        """

        :param host: Hostname or ipaddress of Beoremote Halo
        :param configuration: Configuration to send to Beoremote Halo
        :param on_status_event: Callback for receiving status events
        :param on_power_event: Callback for receiving power events
        :param on_system_event: Callback for receiving system events
        :param on_button_event: Callback for receiving button events
        :param on_wheel_event: Callback for receiving wheel events
        :param on_close_event: Callback when websocket is closed
        :param on_open: Callback when websocket is opened
        """
        self.websocket = websocket.WebSocketApp(
            "ws://{0}:8080".format(host),
            on_open=on_open,
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
        self.on_close_event = on_close_event
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
        """
        Set if client should reconnect to server in the case of connection loss
        :param reconnect: If client should reconnect
        :param attempts: Maximum number of reconnect tries
        """
        self.reconnect = reconnect
        self.attempts = attempts
        self.reconnect_attempts = attempts

    def set_verbosity(self, verbose: bool):
        """
        Configure verbosity
        :param verbose: Set verbosity True/False
        """
        self.verbose = verbose

    def on_message(self, web_socket, message):
        """
        Handling incoming messages from Beoremote Halo and directing them to callbacks
        :param web_socket: websocket.WebSocketApp handle
        :param message: received message on websocket
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

    def send(self, message):
        """
        Send message to Beoremote Halo
        :param message: Either a Configuration or Update
        """
        message = message if isinstance(message, str) else message.to_json()
        if self.verbose:
            print("Client -> Halo: {}".format(message))
        self.websocket.send(message)

    def on_close(self, web_socket, close_status_code, close_msg):
        """
        Called when the websocket is closed, either by Beoremote Halo or the client
        If the on_close_event callback is set, it will be called with status code and message
        :param web_socket: websocket.WebSocketApp handle
        :param close_status_code: websocket closed status code
        :param close_msg: websocket closed message
        """
        del web_socket
        if self.verbose:
            print("### Connection Closed ###")
        self.reconnect = False
        if self.on_close_event:
            self.on_close_event(close_status_code, close_msg)

    def _on_status_event_callback(self, event: StatusEvent):
        """
        Internal handle verifying Beoremte was configured correctly
        :param event: Status Event received from Beoremote Halo
        """
        if (
            isinstance(event, StatusEvent)
            and event.state == StatusEvent.State.ok
            and event.message == "Configuration"
        ):
            self.configured = True
            self.reconnect_attempts = self.attempts
        elif (
            isinstance(event, StatusEvent)
            and event.state == StatusEvent.State.error
            and re.match(R"Invalid Configuration", event.message)
        ):
            self.configured = False
            self.reconnect = False
            print(event.message)
        elif isinstance(event, StatusEvent):
            print(event.message)

    def _on_system_event_callback(self, event: SystemEvent):
        """
        Sends the configuration to Beoremote Halo after receiving a system state active
        :param event: System Event message
        """
        if (
            self.configured is False
            and event.state == SystemEvent.State.active
            and self.configuration is not None
        ):
            self.send(self.configuration)

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
