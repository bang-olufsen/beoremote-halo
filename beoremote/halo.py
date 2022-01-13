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

import logging
import multiprocessing
import re
import time
from threading import Thread

import rel
import websocket

from beoremote.configuration import Configuration
from beoremote.events.event import Event
from beoremote.events.statusEvent import StatusEvent
from beoremote.events.systemEvent import SystemEvent

rel.safe_read()


class Halo:  # pylint: disable=too-many-instance-attributes
    """
    Beoremote Halo connection controller
    Creates and maintain a WebSocket to Beoremote Halo on port 8080

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
    ):
        """

        :param host: Hostname or ipaddress of Beoremote Halo
        """
        self.websocket = websocket.WebSocketApp(
            "ws://{0}:8080".format(host),
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
        )
        self.configuration = None
        self.on_status_event = None
        self.on_power_event = None
        self.on_system_event = None
        self.on_button_event = None
        self.on_wheel_event = None
        self.on_close_event = None
        self.on_connection_open = None
        self.reconnect = True
        self.configured = False
        self.reconnect_attempts = 3
        self.reconnect_backoff_timeout = 30
        self.attempts = 3
        self.manager = multiprocessing.Manager()
        self.sendQueue = self.manager.Queue()
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

    def set_reconnect_backoff_timeout(self, timeout: int):
        """
        :param timeout: Configuration reconnect backoff timeout
        """
        self.reconnect_backoff_timeout = timeout

    def set_configuration(self, configuration: Configuration):
        """
        :param configuration: Configuration to send to Beoremote Halo
        """
        self.configuration = configuration

    def set_on_status_event_callback(self, on_status_event) -> None:
        """
        :param on_status_event: Callback for receiving status events
        """
        self.on_status_event = on_status_event

    def set_on_power_event_callback(self, on_power_event) -> None:
        """
        :param on_power_event: Callback for receiving power events
        """
        self.on_power_event = on_power_event

    def set_on_system_event_callback(self, on_system_event) -> None:
        """
        :param on_system_event: Callback for receiving system events
        """
        self.on_system_event = on_system_event

    def set_on_button_event_callback(self, on_button_event) -> None:
        """
        :param on_button_event: Callback for receiving button events
        """
        self.on_button_event = on_button_event

    def set_on_wheel_event_callback(self, on_wheel_event) -> None:
        """
        :param on_wheel_event: Callback for receiving wheel events
        """
        self.on_wheel_event = on_wheel_event

    def set_on_websocket_close_callback(self, on_close) -> None:
        """
        :param on_close: Callback when websocket is closed
        """
        self.on_close_event = on_close

    def set_auto_reconnect(self, reconnect: bool, attempts: int) -> None:
        """
        Set if client should reconnect to server in the case of connection loss
        :param reconnect: If client should reconnect
        :param attempts: Maximum number of reconnect tries
        """
        self.reconnect = reconnect
        self.attempts = attempts
        self.reconnect_attempts = attempts

    def set_on_connected(self, on_connected):
        """
        :param on_connected: Callback when websocket is opened
        """
        self.on_connection_open = on_connected

    def on_open(self, web_socket) -> None:
        """
        Calling the on_connected callback if configured when the websocket is opened
        :param web_socket: websocket.WebSocketApp handle
        """
        del web_socket
        if self.on_connection_open:
            self.on_connection_open()

    def on_message(self, web_socket, message) -> None:
        """
        Handling incoming messages from Beoremote Halo and directing them to callbacks
        :param web_socket: websocket.WebSocketApp handle
        :param message: received message on websocket
        """
        del web_socket

        logging.debug("Halo -> Client: {}".format(message))
        event = Event.from_json(message).event
        {
            "status": lambda msg: (
                self.on_status_event_callback(msg),
                self.on_status_event(self, msg)
                if self.on_status_event
                else logging.warning(
                    "status event received, on_status_event callback not configured"
                ),
            ),
            "power": lambda msg: (
                self.on_power_event(self, msg)
                if self.on_power_event
                else logging.warning(
                    "power event received, on_power_event callback not configured"
                )
            ),
            "system": lambda msg: (
                self.on_system_event_callback(msg),
                self.on_system_event(self, msg)
                if self.on_system_event
                else logging.warning(
                    "system event received, on_system_event callback not configured"
                ),
            ),
            "button": lambda msg: self.on_button_event(self, msg)
            if self.on_button_event
            else logging.warning(
                "button event received, on_button_event callback not configured"
            ),
            "wheel": lambda msg: self.on_wheel_event(self, msg)
            if self.on_wheel_event
            else logging.warning(
                "wheel event received, on_wheel_event callback not configured"
            ),
        }[event.type](event)

    def send(self, message):
        """
        Send message to Beoremote Halo
        :param message: Either a Configuration or Update
        """
        message = message if isinstance(message, str) else str(message)
        self.sendQueue.put(message)

    def on_close(self, web_socket, close_status_code, close_msg):
        """
        Called when the websocket is closed, either by Beoremote Halo or the client
        If the on_close_event callback is set, it will be called with status code and message
        :param web_socket: websocket.WebSocketApp handle
        :param close_status_code: websocket closed status code
        :param close_msg: websocket closed message
        """
        del web_socket
        logging.debug("### Connection Closed ###")
        self.reconnect = False
        if self.on_close_event:
            self.on_close_event(close_status_code, close_msg)

    def on_status_event_callback(self, event: StatusEvent):
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
            logging.debug(event.message)

    def on_system_event_callback(self, event: SystemEvent):
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

    def close_connection(self):
        rel.signal(2, rel.abort)
        while not self.sendQueue.empty():
            self.sendQueue.get_nowait()

    def send_events(self, send_queue):
        try:
            while True:
                event = send_queue.get(block=True)
                logging.debug("Client -> Halo: {}".format(event))
                self.websocket.send(event)
        except Exception:
            pass

    def connect(self):
        """
        Connect to Beoremote Halo
        """
        while self.reconnect and self.reconnect_attempts > 0:
            status = self.websocket.run_forever(
                ping_interval=self.ping_interval,
                ping_timeout=self.ping_timeout,
                dispatcher=rel,
            )
            worker = Thread(target=self.send_events, args=(self.sendQueue,))
            worker.daemon = True
            worker.start()
            rel.dispatch()

            self.reconnect_attempts = self.reconnect_attempts - 1
            self.configured = False
            if status is True and self.reconnect:
                logging.warning(
                    "### Connection to server lost, retrying again in 30 seconds ({}/{} attempts) "
                    "###".format(self.attempts - self.reconnect_attempts, self.attempts)
                )
                time.sleep(self.reconnect_backoff_timeout)
            else:
                self.reconnect = False
