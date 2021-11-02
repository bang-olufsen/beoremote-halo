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

import sys
import time
from multiprocessing import Process, Semaphore

from beoremotehalo import (
    BeoRemoteHalo,
    BeoRemoteHaloConfig,
    BeoremoteHaloExmaple,
    BeoRemoteHaloUpdateButton,
)

config = BeoremoteHaloExmaple()
semaphore = Semaphore(1)
processes = []
oven_timer = {"running": False}


def clamp(value, min_value, max_value):
    """

    :param max_value:
    :param min_value:
    :param value:
    :return:
    """
    return max(min(value, max_value), min_value)


def on_system_event(beoremote_halo, event):
    """

    :param beoremote_halo:
    :param event:
    """
    del beoremote_halo, event  # unused


def on_wheel_event(beoremote_halo, event):
    """

    :param beoremote_halo:
    :param event:
    """
    button = config[event.id]
    if button and button.value is not None:
        button.value = clamp(button.value + event.counts * 5, 0, 100)
        update = BeoRemoteHaloUpdateButton(event.id, value=button.value)
        beoremote_halo.send(update)


def oven_timer_function(beoremote_halo, button_id, content):
    """

    :param beoremote_halo:
    :param button_id:
    :param content:
    """
    try:
        minutes, seconds = content.text.split(":")
        for minute in range(int(minutes), -1, -1):
            for second in range(int(seconds), -1, -1):
                semaphore.acquire()
                semaphore.release()
                content = BeoRemoteHaloConfig.ContentText(
                    "{:02d}:{:02d}".format(minute, second)
                )
                update = BeoRemoteHaloUpdateButton(button_id, content=content)
                beoremote_halo.send(update)
                time.sleep(1)
            seconds = 59
    except KeyboardInterrupt:
        pass


def on_button_event(beoremote_halo, event):
    """

    :param beoremote_halo:
    :param event:
    """
    button = config[event.id]
    if event.state == "released":
        button.toggle_state()
        update = BeoRemoteHaloUpdateButton(event.id, state=button.state)
        beoremote_halo.send(update)

        if button and button.title == "Oven Timer":
            if oven_timer["running"]:
                semaphore.acquire()
                oven_timer["running"] = not oven_timer["running"]
            else:
                if len(processes) > 0:
                    semaphore.release()
                    oven_timer["running"] = not oven_timer["running"]
                else:
                    proc = Process(
                        target=oven_timer_function,
                        args=(beoremote_halo, event.id, button.content),
                    )
                    oven_timer["running"] = True
                    processes.append(proc)
                    proc.start()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndInteract.py address")
        sys.exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        remote = BeoRemoteHalo(
            ipaddress,
            config,
            on_system_event=on_system_event,
            on_wheel_event=on_wheel_event,
            on_button_event=on_button_event,
        )

        remote.connect()
        for process in processes:
            process.terminate()

    sys.exit()
