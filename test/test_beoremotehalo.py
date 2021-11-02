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

import unittest
import uuid
from unittest.mock import MagicMock, patch

MockWebsocket = MagicMock()
modules = {
    "websocket": MockWebsocket,
    "websocket.WebSocketApp": MockWebsocket.WebSocketApp,
}

patcher = patch.dict("sys.modules")
patcher.start()
# pylint: disable=wrong-import-position
from examples.beoremotehalo import (
    BeoRemoteHalo,
    BeoRemoteHaloConfig,
    BeoremoteHaloExmaple,
    BeoRemoteHaloUpdateButton,
)


class MyTestCase(unittest.TestCase):
    @patch("websocket.WebSocketApp.run_forever")
    def test_connect(self, run_forever):
        remote = BeoRemoteHalo("192.168.1.127")
        remote.connect()
        assert run_forever.called
        self.assertEqual(1, run_forever.call_count)

    def test_beoremote_halo_exmaple(self):
        config = BeoremoteHaloExmaple()

        self.assertEqual(len(config.configuration["pages"]), 2)
        self.assertEqual(config.configuration["version"], "1.0.1")
        self.assertRegex(
            config.configuration["id"],
            R"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",
        )
        self.assertEqual(config.configuration["pages"][0].title, "Kitchen")
        self.assertRegex(
            config.configuration["pages"][0].id,
            R"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",
        )
        self.assertEqual(len(config.configuration["pages"][0].buttons), 3)
        self.assertEqual(config.configuration["pages"][0].buttons[0].state, "active")

        config.configuration["pages"][0].buttons[0].toggle_state()
        self.assertEqual(config.configuration["pages"][0].buttons[0].state, "inactive")
        config.configuration["pages"][0].buttons[0].toggle_state()
        self.assertEqual(config.configuration["pages"][0].buttons[0].state, "active")

    def test_beoremote_halo_update_button(self):
        button = BeoRemoteHaloUpdateButton(str(uuid.uuid1()))
        self.assertRegex(
            button.to_json(),
            R"\{\"update\"\:\s\{\"type\"\:\s\"button\",\s\"id\"\:\s\"\b[0-9a-f]{"
            R"8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b\"\}\}",
        )

    def test_verbose(self):
        remote = BeoRemoteHalo("192.168.1.127")
        self.assertEqual(remote.verbose, True)
        remote.set_verbosity(False)
        self.assertEqual(remote.verbose, False)

    @patch("websocket.WebSocketApp.send")
    def test_send(self, send):
        remote = BeoRemoteHalo("192.168.1.127")
        button = BeoRemoteHaloUpdateButton(str(uuid.uuid1()))

        remote.send(button)
        assert send.called
        self.assertEqual(1, send.call_count)

    @patch("builtins.print")
    def test_close(self, print):  # pylint: disable=redefined-builtin
        remote = BeoRemoteHalo("192.168.1.127")

        remote.on_close(None, None, None)
        self.assertTrue(print.called)

    @patch("websocket.WebSocketApp.send")
    def test_open(self, send):
        config = BeoRemoteHaloConfig([])
        remote = BeoRemoteHalo("192.168.1.127", config)

        remote.on_open(None)
        self.assertTrue(send.called)

    def test_on_message(self):
        on_system_event = MagicMock()
        on_status_event = MagicMock()
        on_power_event = MagicMock()
        on_button_event = MagicMock()
        on_wheel_event = MagicMock()

        remote = BeoRemoteHalo(
            "192.168.1.127",
            on_status_event=on_status_event,
            on_system_event=on_system_event,
            on_power_event=on_power_event,
            on_button_event=on_button_event,
            on_wheel_event=on_wheel_event,
        )

        remote.on_message(
            None, r'{"event": {"type": "status","state": "ok","message": "string"}}'
        )
        on_status_event.assert_called_once()
        self.assertEqual(1, on_status_event.call_count)

    def test_find_button_none(self):
        config = BeoremoteHaloExmaple()
        self.assertIsNone(config["d9f95569-f200-484f-99cb-fd80cfe0045b"])

    def test_find_button(self):
        config = BeoremoteHaloExmaple()
        button = config.configuration["pages"][0].buttons[0]
        self.assertEqual(button, config[button.id])

    def test_create_config(self):
        content = BeoRemoteHaloConfig.ContentText("some text")
        button = BeoRemoteHaloConfig.Button("test button", content)
        page = BeoRemoteHaloConfig.Page("Page title", button)

        config = BeoRemoteHaloConfig(page)

        self.assertEqual(1, len(config.configuration["pages"]))
