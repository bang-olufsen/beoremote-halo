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

from beoremote.beoremotehalo import BeoremoteHalo, BeoremoteHaloExmaple
from beoremote.buttonEvent import ButtonEvent
from beoremote.systemEvent import SystemEvent
from beoremote.text import Text
from beoremote.update import Update
from beoremote.updateButton import UpdateButton
from beoremote.wheelEvent import WheelEvent

config = BeoremoteHaloExmaple()
semaphore = Semaphore(1)
processes = []
oven_timer = {"running": False}


def clamp(value: int, min_value: int, max_value: int):
    """

    :param value: value to clap between min_value and max_value
    :param min_value: lower limit used to clamp value
    :param max_value: upper limit used to clamp value
    :return:
    """
    return max(min(value, max_value), min_value)


def on_system_event(client: BeoremoteHalo, event: SystemEvent):
    """

    :param client: Client handle to communicate with Beoremote Halo
    :param event: System Event from Beoremote Halo
    """
    del client, event  # unused


def on_wheel_event(client: BeoremoteHalo, event: WheelEvent):
    """

    :param client: Client handle to communicate with Beoremote Halo
    :param event: Wheel Event from Beoremote Halo
    """
    button = config[event.id]
    if button and button.value is not None:
        button.value = clamp(button.value + event.counts * 5, 0, 100)
        update = Update(
            UpdateButton(
                id=button.id,
                value=button.value,
                title=None,
                subtitle=None,
                state=None,
                content=None,
            )
        )
        client.send(update)


def oven_timer_function(client: BeoremoteHalo, button_id: str, content: Text):
    """

    :param client: Client handle to communicate with Beoremote Halo
    :param button_id: Uuid of button to update
    :param content: Text content of the button to update
    """
    try:
        minutes, seconds = content.text.split(":")
        for minute in range(int(minutes), -1, -1):
            for second in range(int(seconds), -1, -1):
                semaphore.acquire()
                semaphore.release()
                content = Text("{:02d}:{:02d}".format(minute, second))
                update = Update(
                    UpdateButton(
                        id=button_id,
                        value=None,
                        title=None,
                        subtitle=None,
                        state=None,
                        content=content,
                    )
                )
                client.send(update)
                time.sleep(1)
            seconds = 59
    except KeyboardInterrupt:
        pass


def on_button_event(client: BeoremoteHalo, event: ButtonEvent):
    """

    :param client: Client handle to communicate with Beoremote Halo
    :param event: Button Event from Beoremote Halo
    """
    button = config[event.id]
    if event.state == "released":
        button.toggle_state()
        update = Update(
            UpdateButton(
                id=event.id,
                value=None,
                title=None,
                subtitle=None,
                state=button.state,
                content=None,
            )
        )
        client.send(update)

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
                        args=(client, event.id, button.content),
                    )
                    oven_timer["running"] = True
                    processes.append(proc)
                    proc.start()


def backend(hostname: str):
    remote = BeoremoteHalo(
        host=hostname,
        configuration=config,
        on_system_event=on_system_event,
        on_wheel_event=on_wheel_event,
        on_button_event=on_button_event,
    )
    remote.set_verbosity(True)
    remote.connect()
    for process in processes:
        process.terminate()

    sys.exit()
