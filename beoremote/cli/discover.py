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
import time

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

devices = []
config = {"verbose": True}


class BeoremoteHaloListener(ServiceListener):
    """
    Discovers and prints Beoremote Halo's on the network
    """

    @classmethod
    def remove_service(cls, zc, type_, name) -> None:
        """
        Function is unused in this example
            Provided for code correctness
        :param zc:
        :param type_:
        :param name:
        :return: None
        """
        del zc, type_, name  # unused

    @classmethod
    def add_service(cls, zc, type_, name):
        """
        Discovers and prints Beoremote Halo's on the network
        :param zc:
        :param type_:
        :param name:
        """
        info = zc.get_service_info(type_, name)
        if info:
            device = {
                "serial": info.server[14:-7],
                "address": info.parsed_addresses()[0],
            }
            if config["verbose"]:
                print("Serial: {}, {}".format(device["serial"], device["address"]))
            devices.append(device)

    @classmethod
    def update_service(cls, zc, type_, name):
        """
        Function is unused in this example
            Provided for code correctness
        :param zc:
        :param type_:
        :param name:
        :return:
        """
        del zc, type_, name  # unused


def discover(timeout=None):
    zeroconf = Zeroconf()
    listener = BeoremoteHaloListener()
    browser = ServiceBrowser(zeroconf, "_zenith._tcp.local.", listener)

    try:
        if timeout:
            config["verbose"] = False
            time.sleep(timeout)
        else:
            input(
                "Discovering Beoremote Halo on network...\r\n"
                "If Beoremote Halo does not appear on the list, try waking it "
                "up while discovery in running.\r\nPress enter to exit...\n\n"
            )
    except KeyboardInterrupt:
        browser.cancel()
    finally:
        zeroconf.close()

    return devices
