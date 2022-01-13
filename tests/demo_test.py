"""
The MIT License (MIT)

Copyright (c) 2022 Bang & Olufsen a/s

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
import signal
import unittest
from unittest.mock import MagicMock, patch

from beoremote.cli.backend import (
    backend,
    clamp,
    config,
    on_button_event,
    on_power_event,
    on_status_event,
    on_system_event,
    on_wheel_event,
    oven_timer_function,
    processes,
)
from beoremote.configuration import Configuration
from beoremote.events.buttonEvent import ButtonEvent
from beoremote.events.statusEvent import StatusEvent
from beoremote.events.text import Text
from beoremote.events.update import Update
from beoremote.events.updateButton import UpdateButton
from beoremote.events.wheelEvent import WheelEvent


def test_on_power_event():
    on_power_event(MagicMock(), MagicMock())


def test_on_system_event():
    on_system_event(MagicMock(), MagicMock())


class DemoTestCase(unittest.TestCase):
    @patch("beoremote.cli.backend.Halo")
    def test_backend(self, mock_halo):
        process = MagicMock()
        process.terminate = MagicMock()
        processes.append(process)

        backend("BeoremoteHalo-xxxxxxxx.local")

        self.assertTrue(mock_halo.called)
        self.assertTrue(mock_halo.return_value.set_on_status_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_system_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_power_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_button_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_wheel_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_configuration.called)
        self.assertTrue(mock_halo.return_value.set_on_connected.called)
        self.assertTrue(mock_halo.return_value.connect.called)

        process.terminate.assert_called_once()
        processes.pop()

    @patch("beoremote.cli.backend.Halo")
    def test_backend_sigint(self, mock_halo):
        process = MagicMock()
        process.terminate = MagicMock()
        processes.append(process)

        mock_halo.connect = MagicMock()

        def signal_side_effect(*args, **kwargs):
            del args, kwargs
            signal.raise_signal(signal.SIGINT)

        mock_halo.return_value.connect.side_effect = signal_side_effect
        with patch("sys.exit") as exit_mock:
            backend("BeoremoteHalo-xxxxxxxx.local")
            self.assertTrue(exit_mock.called)

        self.assertTrue(mock_halo.called)
        self.assertTrue(mock_halo.return_value.set_on_status_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_system_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_power_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_button_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_on_wheel_event_callback.called)
        self.assertTrue(mock_halo.return_value.set_configuration.called)
        self.assertTrue(mock_halo.return_value.connect.called)

        process.terminate.assert_called_once()
        processes.pop()

    def test_clamp(self):
        self.assertEqual(100, clamp(120, 0, 100))
        self.assertEqual(100, clamp(100, 0, 100))
        self.assertEqual(90, clamp(90, 0, 100))
        self.assertEqual(0, clamp(0, 0, 100))
        self.assertEqual(0, clamp(-10, 0, 100))

    @patch("beoremote.cli.backend.logging")
    def test_on_status_event(self, mock_log):
        event = StatusEvent("status", StatusEvent.State.ok)
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()
        on_status_event(mock_halo, event)

        event = StatusEvent("status", StatusEvent.State.error, "error")
        on_status_event(mock_halo, event)
        mock_log.warning.assert_called_once_with("error")
        self.assertFalse(mock_halo.send.called)

    def test_on_wheel_event_unknow_id(self):
        event = WheelEvent("wheel", "cf4c7ccf-866c-4e73-bae3-e8a296d5562b", 1)
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()
        on_wheel_event(mock_halo, event)

        self.assertFalse(mock_halo.send.called)

    def test_on_wheel_event(self):
        button_id = config.configuration["pages"][0].buttons[0].id
        event = WheelEvent("wheel", button_id, -1)
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()
        on_wheel_event(mock_halo, event)
        update = Update(
            UpdateButton(
                id=button_id,
                value=90,
                title=None,
                subtitle=None,
                state=None,
                content=None,
            )
        )
        self.assertEqual(str(mock_halo.send.call_args.args[0]), str(update))

    @patch("time.sleep")
    def test_oven_timer_function(self, mock_sleep):
        mock_queue = MagicMock()
        mock_queue.put = MagicMock()
        text = Text("00:03")
        oven_timer_function(mock_queue, "cf4c7ccf-866c-4e73-bae3-e8a296d5562b", text)

        self.assertTrue(mock_sleep.called)
        self.assertEqual(4, mock_queue.put.call_count)

        self.assertRegex(mock_queue.put.call_args_list[0].args[0], "00:03")
        self.assertRegex(mock_queue.put.call_args_list[1].args[0], "00:02")
        self.assertRegex(mock_queue.put.call_args_list[2].args[0], "00:01")
        self.assertRegex(mock_queue.put.call_args_list[3].args[0], "00:00")

    @patch("time.sleep")
    def test_oven_timer_function_exception(self, mock_sleep):
        mock_queue = MagicMock()
        mock_queue.put = MagicMock()
        text = Text("00:03")
        mock_queue.put.side_effect = unittest.mock.Mock(side_effect=KeyboardInterrupt())
        oven_timer_function(mock_queue, "cf4c7ccf-866c-4e73-bae3-e8a296d5562b", text)
        self.assertFalse(mock_sleep.called)

    def test_on_button_event(self):
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()

        button_id = config.configuration["pages"][0].buttons[0].id
        event = ButtonEvent("button", button_id, ButtonEvent.State.released)
        on_button_event(mock_halo, event)

        self.assertTrue(mock_halo.send.called)
        self.assertEqual(
            Configuration.Pages.Buttons.State.INACTIVE,
            mock_halo.send.call_args.args[0].update.state,
        )

    @patch("beoremote.cli.backend.Process")
    def test_on_button_event_oven_timer(self, mock_process):
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()

        button_id = config.configuration["pages"][0].buttons[1].id
        event = ButtonEvent("button", button_id, ButtonEvent.State.released)
        on_button_event(mock_halo, event)
        on_button_event(mock_halo, event)
        on_button_event(mock_halo, event)
        self.assertTrue(mock_halo.send.called)
        self.assertTrue(mock_process.called)
        self.assertEqual(3, mock_halo.send.call_count)
        self.assertTrue(mock_process.return_value.start.called)

    def test_on_button_event_unknow_id(self):
        mock_halo = MagicMock()
        mock_halo.send = MagicMock()
        event = ButtonEvent(
            "button", "cf4c7ccf-866c-4e73-bae3-e8a296d5562b", ButtonEvent.State.pressed
        )
        on_button_event(mock_halo, event)

        event = ButtonEvent(
            "button", "cf4c7ccf-866c-4e73-bae3-e8a296d5562b", ButtonEvent.State.released
        )
        on_button_event(mock_halo, event)
        self.assertFalse(mock_halo.send.called)
