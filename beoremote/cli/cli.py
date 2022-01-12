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

import click

import beoremote
from beoremote import halo
from beoremote.cli import backend, discover
from beoremote.configuration import Configuration


@click.option(
    "--log",
    help="Set logging level, default INFO",
    default="INFO",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
)
@click.group()
def cli(log):
    """Cli provided by Bang & Olufsen a/s used to scan the network for Beoremote Halo on local
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
    """
    numeric_level = getattr(logging, log.upper(), None)
    logging.basicConfig(format="%(levelname)-8s | %(message)s", level=numeric_level)


@cli.command(help="Scan the network for active Beoremote Halo.")
def scan():
    discover.discover()


@cli.command(help="Interactive Home Automation Demo")
@click.option("--hostname", required=True)
def demo(hostname):
    backend.backend(hostname)


@cli.command(help="Connect to a Halo and listen for events")
@click.option("--hostname", required=True)
def listen(hostname):
    remote = halo.Halo(hostname)
    remote.connect()


@cli.command(help="Version")
def version():
    print("beoremote-halo package version: {}".format(beoremote.__version__))
    print("API version: {}".format(Configuration.APIVersion))
