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
import socket
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

import beoremote
from beoremote.cli.cli import cli
from beoremote.configuration import Configuration


class BeoremoteHaloCliTest(unittest.TestCase):
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        expected_string = (
            "beoremote-halo package version: {}\n"
            "beoremote-halo cli version: {}\n"
            "API version: {}\n".format(
                beoremote.__version__,
                beoremote.cli.__version__,
                Configuration.APIVersion,
            )
        )
        self.assertEqual(result.output, expected_string)
        print(cli.options_metavar)

    @patch("beoremote.halo.Halo")
    def test_cli_listen(self, mock_halo):
        runner = CliRunner()
        runner.invoke(cli, ["--log=DEBUG", "listen", "--ip=127.0.0.1"])

        self.assertEqual(1, mock_halo.call_count)
        self.assertEqual("127.0.0.1", mock_halo.call_args.args[0])
        self.assertEqual(1, mock_halo.return_value.connect.call_count)

    @patch("beoremote.halo.Halo")
    @patch("socket.gethostbyname")
    def test_cli_listen_serial(
        self, mock_gethostbyname: MagicMock, mock_halo: MagicMock
    ):
        mock_gethostbyname.return_value = "127.0.0.1"
        runner = CliRunner()
        runner.invoke(cli, ["listen", "--serial=12345678"])

        self.assertEqual(1, mock_halo.call_count)
        self.assertEqual("127.0.0.1", mock_halo.call_args.args[0])
        self.assertEqual(1, mock_gethostbyname.call_count)

    @patch("beoremote.halo.Halo")
    def test_cli_listen_no_arguments(self, mock_halo: MagicMock):
        runner = CliRunner()
        runner.invoke(cli, ["listen"])

        self.assertEqual(0, mock_halo.call_count)

    @patch("beoremote.halo.Halo")
    def test_cli_scan_serial_use_ip(self, mock_halo: MagicMock):
        runner = CliRunner()

        runner.invoke(cli, ["listen", "--ip=12345678"])
        self.assertFalse(mock_halo.called)

    @patch("beoremote.cli.backend.backend")
    def test_cli_demo(self, mock_demo):
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--ip=127.0.0.1"])

        self.assertEqual(1, mock_demo.call_count)
        self.assertEqual("127.0.0.1", mock_demo.call_args.args[0])

    @patch("beoremote.cli.backend.backend")
    @patch("socket.gethostbyname")
    def test_cli_demo_serial(self, mock_gethostbyname: MagicMock, mock_demo: MagicMock):
        mock_gethostbyname.return_value = "127.0.0.1"
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--serial=12345678"])

        self.assertEqual(1, mock_demo.call_count)
        self.assertEqual("127.0.0.1", mock_demo.call_args.args[0])
        self.assertEqual(1, mock_gethostbyname.call_count)

    @patch("beoremote.cli.backend.backend")
    @patch("socket.gethostbyname")
    def test_cli_demo_serial_gaierror(
        self, mock_gethostbyname: MagicMock, mock_demo: MagicMock
    ):
        mock_gethostbyname.side_effect = unittest.mock.Mock(side_effect=socket.gaierror)
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--serial=12345678"])

        self.assertFalse(mock_demo.called)

    @patch("beoremote.cli.backend.backend")
    def test_cli_demo_serial_invalid_serial(self, mock_demo: MagicMock):
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--serial=a2345678"])

        self.assertFalse(mock_demo.called)

    @patch("beoremote.cli.backend.backend")
    def test_cli_demo_serial_use_ip(self, mock_demo: MagicMock):
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--ip=12345678"])
        self.assertFalse(mock_demo.called)

    @patch("beoremote.cli.backend.backend")
    def test_cli_demo_no_arguments(self, mock_demo: MagicMock):
        runner = CliRunner()
        runner.invoke(cli, ["demo"])

        self.assertEqual(0, mock_demo.call_count)

    @patch("beoremote.cli.discover.discover")
    def test_cli_scan(self, mock_discover):
        runner = CliRunner()
        runner.invoke(cli, ["scan"])

        self.assertEqual(1, mock_discover.call_count)

    def test_cli_invalid_log_type(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--log=None"])

        self.assertEqual(2, result.exit_code)
        self.assertRegex(result.output, "Invalid value for '--log'")

    def test_cli_mutually_exclusive(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["demo", "--ip=127.0.0.1", "--serial=12345678"])

        self.assertEqual(2, result.exit_code)
        self.assertRegex(
            result.output,
            "Error: Illegal usage: `ip` is mutually exclusive with arguments `serial`.\n",
        )

    def test_cli_mutually_exclusive2(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["demo", "--serial=12345678", "--ip=127.0.0.1"])

        self.assertEqual(2, result.exit_code)
        self.assertRegex(
            result.output,
            "Error: Illegal usage: `serial` is mutually exclusive with arguments `ip`.\n",
        )
