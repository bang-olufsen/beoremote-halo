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
import unittest
from unittest.mock import MagicMock, patch

from zeroconf import ServiceInfo

from beoremote.cli.discover import BeoremoteHaloListener, discover


class MyTestCase(unittest.TestCase):
    @patch("builtins.input")
    @patch("beoremote.cli.discover.Zeroconf")
    @patch("beoremote.cli.discover.ServiceBrowser")
    def test_discover(self, mock_serviceBrowser, mock_zeroconf, mock_input):
        discover()

        self.assertEqual(1, mock_input.call_count)
        self.assertEqual(1, mock_serviceBrowser.call_count)
        self.assertEqual(mock_serviceBrowser.call_args.args[1], "_zenith._tcp.local.")
        self.assertEqual(1, mock_zeroconf.return_value.close.call_count)

    @patch("time.sleep")
    @patch("beoremote.cli.discover.Zeroconf")
    @patch("beoremote.cli.discover.ServiceBrowser")
    def test_discover_timeout(self, mock_serviceBrowser, mock_zeroconf, mock_sleep):
        discover(5)

        self.assertEqual(1, mock_sleep.call_count)
        mock_sleep.assert_called_with(5)
        self.assertEqual(1, mock_serviceBrowser.call_count)
        self.assertEqual(mock_serviceBrowser.call_args.args[1], "_zenith._tcp.local.")
        self.assertEqual(1, mock_zeroconf.return_value.close.call_count)

    @patch("builtins.input")
    @patch("beoremote.cli.discover.Zeroconf")
    @patch("beoremote.cli.discover.ServiceBrowser")
    def test_discover_raises(self, mock_serviceBrowser, mock_zeroconf, mock_input):
        mock_input.side_effect = unittest.mock.Mock(side_effect=KeyboardInterrupt())
        discover()
        self.assertEqual(1, mock_input.call_count)
        self.assertEqual(1, mock_serviceBrowser.call_count)
        self.assertEqual(mock_serviceBrowser.call_args.args[1], "_zenith._tcp.local.")
        self.assertEqual(1, mock_zeroconf.return_value.close.call_count)

    @patch("builtins.print")
    def test_BeoremoteHaloListener_add_service(self, mock_print):
        conf_type = "_zenith._tcp.local."
        name = "BeoremoteHalo-XXXXXXXX._zenith._tcp.local."
        zero_conf = MagicMock()

        # zero_conf.get_service_info = MagicMock()
        zero_conf.get_service_info.return_value = ServiceInfo(
            type_="_zenith._tcp.local.",
            name="BeoremoteHalo-xxxxxxxx._zenith._tcp.local.",
            addresses=[b"\n\xdf\xcf\x88"],
            port=80,
            weight=0,
            priority=0,
            server="BeoremoteHalo-xxxxxxxx.local.",
            properties={
                b"mac": b"00:09:A7:37:E0:DF",
                b"type": b"3054",
                b"serial": b"33284713",
                b"item": b"1305400",
                b"productType": b"T38",
                b"name": b"Beoremote Halo",
            },
            interface_index=None,
        )

        BeoremoteHaloListener.add_service(zero_conf, conf_type, name)

        self.assertTrue(mock_print.called)
        self.assertTrue(zero_conf.get_service_info.called)
        mock_print.assert_called_with("Serial: xxxxxxxx, 10.223.207.136")

    def test_BeoremoteHaloListener_remove_service(self):
        conf_type = "_zenith._tcp.local."
        name = "BeoremoteHalo-XXXXXXXX._zenith._tcp.local."
        zero_conf = MagicMock()

        # zero_conf.get_service_info = MagicMock()
        zero_conf.get_service_info.return_value = ServiceInfo(
            type_="_zenith._tcp.local.",
            name="BeoremoteHalo-xxxxxxxx._zenith._tcp.local.",
            addresses=[b"\n\xdf\xcf\x88"],
            port=80,
            weight=0,
            priority=0,
            server="BeoremoteHalo-xxxxxxxx.local.",
            properties={
                b"mac": b"00:09:A7:37:E0:DF",
                b"type": b"3054",
                b"serial": b"33284713",
                b"item": b"1305400",
                b"productType": b"T38",
                b"name": b"Beoremote Halo",
            },
            interface_index=None,
        )

        BeoremoteHaloListener.remove_service(zero_conf, conf_type, name)
        self.assertFalse(zero_conf.get_service_info.called)

    def test_BeoremoteHaloListener_update_service(self):
        conf_type = "_zenith._tcp.local."
        name = "BeoremoteHalo-xxxxxxxx._zenith._tcp.local."
        zero_conf = MagicMock()

        # zero_conf.get_service_info = MagicMock()
        zero_conf.get_service_info.return_value = ServiceInfo(
            type_="_zenith._tcp.local.",
            name="BeoremoteHalo-xxxxxxxx._zenith._tcp.local.",
            addresses=[b"\n\xdf\xcf\x88"],
            port=80,
            weight=0,
            priority=0,
            server="BeoremoteHalo-xxxxxxxx.local.",
            properties={
                b"mac": b"00:09:A7:37:E0:DF",
                b"type": b"3054",
                b"serial": b"33284713",
                b"item": b"1305400",
                b"productType": b"T38",
                b"name": b"Beoremote Halo",
            },
            interface_index=None,
        )

        BeoremoteHaloListener.update_service(zero_conf, conf_type, name)
        self.assertFalse(zero_conf.get_service_info.called)
