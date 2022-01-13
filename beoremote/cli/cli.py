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
import re
import socket
import sys

import click
from click import Option, UsageError

import beoremote
from beoremote import halo
from beoremote.cli import __version__, backend, discover
from beoremote.configuration import Configuration


class MutuallyExclusiveOptions(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help_string = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help_string + (
                " - NOTE: This argument is mutually exclusive with"
                " arguments: [" + ex_str + "]"
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super().handle_parse_result(ctx, opts, args)


def serial_to_ip(serial: str) -> str:
    ip = None
    if serial and re.match(R"\d{8}", serial):
        hostname = "BeoremoteHalo-{}.local".format(serial)
        try:
            click.echo(
                "Searching for Beoremote Halo with serial {} on the network".format(
                    serial
                )
            )
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            click.echo(
                "Unable to locate serial {} on network, try specifying ip address".format(
                    serial
                )
            )
            sys.exit(1)
    else:
        click.echo("{} is not a valid serial number".format(serial))
        sys.exit(1)
    return ip


@click.group()
@click.option(
    "--log",
    help="Set logging level, default INFO",
    default="DEBUG",
    type=click.Choice(["DEBUG", "INFO"], case_sensitive=False),
)
@click.version_option(
    prog_name="beoremote-halo",
    version="beoremote-halo package version: {}"
    "\nbeoremote-halo cli version: {}"
    "\nAPI version: {}".format(
        beoremote.__version__, __version__, Configuration.APIVersion
    ),
    message="%(version)s",
)
@click.pass_context
def cli(ctx, log):
    """cli provided by Bang & Olufsen a/s used to scan the network for Beoremote Halo on local
    network

    \b
    Project source files are located at github:
    https://github.com/bang-olufsen/beoremote-halo
    API documentation is located available at:
    https://bang-olufsen.github.io/beoremote-halo/

    \b
    Please report bugs or issues at:
    https://github.com/bang-olufsen/beoremote-halo/issues
    \b
    For command specific help message type:
    beoremote-halo [command] --help
    """
    del ctx
    numeric_level = getattr(logging, log.upper(), None)
    logging.basicConfig(
        format="%(levelname)-5s | %(message)s",
        level=numeric_level,
    )


@cli.command(help="Scan the network for active Beoremote Halo.")
def scan():
    discover.discover()


@cli.command(help="Interactive Home Automation Demo")
@click.option(
    "--ip",
    "ip",
    help="ip address of Beoremote Halo",
    type=str,
    cls=MutuallyExclusiveOptions,
    mutually_exclusive=["serial"],
)
@click.option(
    "--serial",
    "serial",
    type=str,
    help="Serial number of Beoremote Halo",
    cls=MutuallyExclusiveOptions,
    mutually_exclusive=["ip"],
)
def demo(ip, serial):
    if not ip and not serial:
        click.echo(demo.get_help(click.get_current_context()))
        sys.exit(0)

    if serial:
        ip = serial_to_ip(serial)

    backend.backend(ip)


@cli.command(help="Connect to a Halo and listen for events")
@click.option(
    "--ip",
    "ip",
    help="ip address of Beoremote Halo",
    type=str,
    cls=MutuallyExclusiveOptions,
    mutually_exclusive=["serial"],
)
@click.option(
    "--serial",
    "serial",
    type=str,
    help="Serial number of Beoremote Halo",
    cls=MutuallyExclusiveOptions,
    mutually_exclusive=["ip"],
)
def listen(ip, serial):
    if not ip and not serial:
        click.echo(demo.get_help(click.get_current_context()))
        sys.exit(0)

    if serial:
        ip = serial_to_ip(serial)

    remote = halo.Halo(ip)
    remote.set_on_connected(lambda: print("Listening on events from: {}".format(ip)))
    remote.connect()
