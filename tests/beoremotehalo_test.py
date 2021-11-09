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
from unittest.mock import MagicMock, patch

MockWebsocket = MagicMock()
modules = {
    "websocket": MockWebsocket,
    "websocket.WebSocketApp": MockWebsocket.WebSocketApp,
    "time": MagicMock,
}

patcher = patch.dict("sys.modules")
patcher.start()

# pylint: disable=wrong-import-position
from beoremote.beoremote_config_example import BeoremoteHaloExmaple
from beoremote.beoremotehalo import BeoremoteHalo
from beoremote.icons import Icons
from beoremote.update import Update
from beoremote.updateButton import UpdateButton


class MyTestCase(unittest.TestCase):
    @patch("time.sleep")
    @patch("websocket.WebSocketApp.run_forever")
    def test_reconnect(self, mock_run_forever, mock_sleep):
        mock_run_forever.return_value = True

        remote = BeoremoteHalo("192.168.1.127")
        remote.connect()

        mock_sleep.assert_called_with(30)
        mock_run_forever.assert_called_with(ping_interval=30, ping_timeout=5)
        self.assertEqual(3, mock_run_forever.call_count)
        self.assertEqual(3, mock_sleep.call_count)

    @patch("time.sleep")
    @patch("websocket.WebSocketApp.run_forever")
    def test_connect_closing(self, mock_run_forever, mock_sleep):
        mock_run_forever.return_value = False

        remote = BeoremoteHalo("192.168.1.127")
        remote.connect()
        mock_run_forever.assert_called_with(ping_interval=30, ping_timeout=5)
        self.assertEqual(1, mock_run_forever.call_count)
        self.assertEqual(0, mock_sleep.call_count)

    def test_connect(self):
        on_system_event = MagicMock()
        on_status_event = MagicMock()
        on_power_event = MagicMock()
        on_button_event = MagicMock()
        on_wheel_event = MagicMock()
        config = BeoremoteHaloExmaple()
        remote = BeoremoteHalo(
            "192.168.1.127",
            on_status_event=on_status_event,
            on_system_event=on_system_event,
            on_power_event=on_power_event,
            on_button_event=on_button_event,
            on_wheel_event=on_wheel_event,
            configuration=config,
        )

        remote.set_auto_reconnect(True, 1)
        remote.set_verbosity(True)

        mock_send = MagicMock()
        websocket = MagicMock()
        remote.websocket = websocket
        mock_run_forever = MagicMock()

        def on_message_system_event(*args, **kwargs):
            del args, kwargs
            remote.on_message(
                websocket, r'{"event":{"type":"system","state":"active"}}'
            )

        def on_message_status_event(*args, **kwargs):
            del args, kwargs
            remote.on_message(
                websocket,
                r'{"event":{"type":"status","state":"ok","message":"Configuration"}}',
            )

        mock_run_forever.return_value = False
        mock_run_forever.side_effect = on_message_system_event
        mock_send.side_effect = on_message_status_event

        remote.websocket.send = mock_send
        remote.websocket.run_forever = mock_run_forever

        remote.connect()

        config_string = (
            R'\{"configuration":\{"version":"1\.0\.1","id":"\b[0-9a-f]{8}\b-[0-9a-f]{'
            R'4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","pages":\[\{'
            R'"title":"Kitchen","id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-['
            R'0-9a-f]{4}-\b[0-9a-f]{12}\b","buttons":\[\{"id":"\b[0-9a-f]{8}\b-['
            R'0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Kitchen\ '
            R'Light","subtitle":"On","value":95,"state":"active","content":\{'
            R'"icon":"lights"\},"default":false\},\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{'
            R'4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Oven\ Timer",'
            R'"subtitle":"Temperature\ 200\\u00b0C","value":0,"state":"inactive",'
            R'"content":\{"text":"01:35"\},"default":true\},\{"id":"\b[0-9a-f]{8}\b-['
            R'0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Dining\ '
            R'Table","subtitle":"Off","value":80,"state":"inactive","content":\{'
            R'"icon":"lights"\},"default":false\}\]\},\{"title":"living\ room",'
            R'"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","buttons":\[\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-['
            R'0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Fire\ Place","subtitle":"Ignite",'
            R'"state":"inactive","content":\{"icon":"lights"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"Blinds","subtitle":"Closed","value":100,'
            R'"state":"active","content":\{"icon":"blinds"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"TV\ Backlight","subtitle":"off","value":0,'
            R'"state":"inactive","content":\{"icon":"rgb_lights"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"Thermostat","subtitle":"Heating","value":55,'
            R'"state":"inactive","content":\{"text":"21\\u00b0C"\},'
            R'"default":true\}\]\}\]\}\}'
        )

        self.assertRegex(mock_send.call_args.args[0], config_string)
        self.assertTrue(mock_send.called)
        self.assertTrue(mock_run_forever.called)
        self.assertFalse(websocket.called)

    def test_connect_invalid_config(self):
        on_system_event = MagicMock()
        on_status_event = MagicMock()
        on_power_event = MagicMock()
        on_button_event = MagicMock()
        on_wheel_event = MagicMock()
        config = BeoremoteHaloExmaple()
        remote = BeoremoteHalo(
            "192.168.1.127",
            on_status_event=on_status_event,
            on_system_event=on_system_event,
            on_power_event=on_power_event,
            on_button_event=on_button_event,
            on_wheel_event=on_wheel_event,
            configuration=config,
        )

        remote.set_auto_reconnect(True, 1)
        remote.set_verbosity(True)

        mock_send = MagicMock()
        websocket = MagicMock()
        remote.websocket = websocket
        mock_run_forever = MagicMock()

        def on_message_system_event(*args, **kwargs):
            del args, kwargs
            remote.on_message(
                websocket, r'{"event":{"type":"system","state":"active"}}'
            )

        def on_message_status_event(*args, **kwargs):
            del args, kwargs
            remote.on_message(
                websocket,
                r'{"event":{"type":"status","state":"error","message":"Invalid Configuration, '
                r'button uuid @page: cfbe9c83-413d-11ec-92ac-b7df6f9ee3e2"}}',
            )

        mock_run_forever.return_value = False
        mock_run_forever.side_effect = on_message_system_event
        mock_send.side_effect = on_message_status_event

        remote.websocket.send = mock_send
        remote.websocket.run_forever = mock_run_forever

        remote.connect()

        config_string = (
            R'\{"configuration":\{"version":"1\.0\.1","id":"\b[0-9a-f]{8}\b-[0-9a-f]{'
            R'4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","pages":\[\{'
            R'"title":"Kitchen","id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-['
            R'0-9a-f]{4}-\b[0-9a-f]{12}\b","buttons":\[\{"id":"\b[0-9a-f]{8}\b-['
            R'0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Kitchen\ '
            R'Light","subtitle":"On","value":95,"state":"active","content":\{'
            R'"icon":"lights"\},"default":false\},\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{'
            R'4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Oven\ Timer",'
            R'"subtitle":"Temperature\ 200\\u00b0C","value":0,"state":"inactive",'
            R'"content":\{"text":"01:35"\},"default":true\},\{"id":"\b[0-9a-f]{8}\b-['
            R'0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Dining\ '
            R'Table","subtitle":"Off","value":80,"state":"inactive","content":\{'
            R'"icon":"lights"\},"default":false\}\]\},\{"title":"living\ room",'
            R'"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","buttons":\[\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-['
            R'0-9a-f]{4}-\b[0-9a-f]{12}\b","title":"Fire\ Place","subtitle":"Ignite",'
            R'"state":"inactive","content":\{"icon":"lights"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"Blinds","subtitle":"Closed","value":100,'
            R'"state":"active","content":\{"icon":"blinds"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"TV\ Backlight","subtitle":"off","value":0,'
            R'"state":"inactive","content":\{"icon":"rgb_lights"\},"default":false\},'
            R'\{"id":"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{'
            R'12}\b","title":"Thermostat","subtitle":"Heating","value":55,'
            R'"state":"inactive","content":\{"text":"21\\u00b0C"\},'
            R'"default":true\}\]\}\]\}\}'
        )

        self.assertRegex(mock_send.call_args.args[0], config_string)
        self.assertTrue(mock_send.called)
        self.assertTrue(mock_run_forever.called)
        self.assertFalse(websocket.called)
        self.assertEqual(1, mock_run_forever.call_count)

    def test_beoremote_halo_example(self):
        config = BeoremoteHaloExmaple()

        self.assertEqual(len(config.configuration.pages), 2)
        self.assertEqual(config.configuration.version, "1.0.1")
        self.assertRegex(
            config.configuration.id,
            R"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",
        )
        self.assertEqual(config.configuration.pages[0].title, "Kitchen")
        self.assertRegex(
            config.configuration.pages[0].id,
            R"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b",
        )
        self.assertEqual(len(config.configuration.pages[0].buttons), 3)
        self.assertEqual(config.configuration.pages[0].buttons[0].state, "active")

        self.assertEqual(config.configuration.pages[0].buttons[0].state, "active")

    def test_verbose(self):
        remote = BeoremoteHalo("192.168.1.127")
        self.assertEqual(remote.verbose, False)
        remote.set_verbosity(True)
        self.assertEqual(remote.verbose, True)
        remote.set_verbosity(False)
        self.assertEqual(remote.verbose, False)

    @patch("websocket.WebSocketApp.send")
    def test_send(self, send):
        remote = BeoremoteHalo("192.168.1.127")
        button = Update(
            UpdateButton(
                "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "string",
                "string",
                100,
                UpdateButton.State.active,
                Icons(Icons.Icon.LIGHTS),
            )
        )

        remote.send(button)

        assert send.called
        self.assertEqual(1, send.call_count)

    @patch("builtins.print")
    def test_close(self, print):  # pylint: disable=redefined-builtin
        mock_close_callback = MagicMock()
        remote = BeoremoteHalo("192.168.1.127", on_close_event=mock_close_callback)
        remote.set_verbosity(True)
        remote.on_close(None, None, None)
        self.assertTrue(print.called)
        mock_close_callback.assert_called_with(None, None)

    def test_on_message(self):
        on_system_event = MagicMock()
        on_status_event = MagicMock()
        on_power_event = MagicMock()
        on_button_event = MagicMock()
        on_wheel_event = MagicMock()

        remote = BeoremoteHalo(
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
        status_event = on_status_event.call_args.args[1]
        self.assertEqual("status", status_event.type)
        self.assertEqual("ok", status_event.state)
        self.assertEqual("string", status_event.message)

    def test_find_button_none(self):
        config = BeoremoteHaloExmaple()
        self.assertIsNone(config["d9f95569-f200-484f-99cb-fd80cfe0045b"])

    def test_find_button(self):
        config = BeoremoteHaloExmaple()
        button = config.configuration.pages[0].buttons[0]
        self.assertEqual(button, config[button.id])

    def test_button_toggle(self):
        config = BeoremoteHaloExmaple()
        button = config.configuration.pages[0].buttons[0]
        self.assertEqual("active", button.state)
        button.toggle_state()
        self.assertEqual("inactive", button.state)
        button.toggle_state()
        self.assertEqual("active", button.state)
