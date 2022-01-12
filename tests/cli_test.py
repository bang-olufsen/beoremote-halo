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
from unittest.mock import patch

from click.testing import CliRunner

import beoremote
from beoremote.cli.cli import cli
from beoremote.configuration import Configuration


class MyTestCase(unittest.TestCase):
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])

        expected_string = (
            "beoremote-halo package version: {}\nAPI version: {}\n".format(
                beoremote.__version__, Configuration.APIVersion
            )
        )
        self.assertEqual(result.output, expected_string)
        print(cli.options_metavar)

    @patch("beoremote.halo.Halo")
    def test_cli_listen(self, mock_halo):
        runner = CliRunner()
        runner.invoke(
            cli, ["--log=DEBUG", "listen", "--hostname=BeoremoteHalo-XXXXXXXX.local"]
        )

        self.assertEqual(1, mock_halo.call_count)
        self.assertEqual("BeoremoteHalo-XXXXXXXX.local", mock_halo.call_args.args[0])
        self.assertEqual(1, mock_halo.return_value.connect.call_count)

    @patch("beoremote.cli.backend.backend")
    def test_cli_demo(self, mock_demo):
        runner = CliRunner()
        runner.invoke(cli, ["demo", "--hostname=BeoremoteHalo-XXXXXXXX.local"])

        self.assertEqual(1, mock_demo.call_count)
        self.assertEqual("BeoremoteHalo-XXXXXXXX.local", mock_demo.call_args.args[0])

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
