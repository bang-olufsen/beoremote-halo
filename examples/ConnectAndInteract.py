import math
import sys
import threading
import time

from BeoremoteHalo import BeoRemoteHalo
from BeoremoteHalo import BeoRemoteHaloConfig
from BeoremoteHalo import BeoRemoteHaloUpdateButton
from BeoremoteHalo import BeoremoteHaloExmaple

config = BeoremoteHaloExmaple()


def clamp(value, minv, maxv):
    return max(min(value, maxv), minv)


def on_system_event(ws, event):
    pass


def on_wheel_event(ws, event):
    button = config[event.id]
    if button and button.value is not None:
        button.value = clamp(button.value + event.counts * 5, 0, 100)
        update = BeoRemoteHaloUpdateButton(event.id, value=button.value)
        print(update.to_json())
        ws.send(update.to_json())


oventimer_started = False
threads = []


def oventimer_function(ws, id, countdown):
    minutes, seconds = countdown.split(":")
    for m in range(int(minutes), -1, -1):
        for s in range(int(seconds), -1, -1):
            content = BeoRemoteHaloConfig.ContentText("{:02d}:{:02d}".format(m, s))
            update = BeoRemoteHaloUpdateButton(id, content=content)
            ws.send(update.to_json())
            time.sleep(1)
        seconds = 59


def on_button_event(ws, event):
    button = config[event.id]
    if event.state == "released":
        button.toggle_state()
        update = BeoRemoteHaloUpdateButton(event.id, state=button.state)

        if button and button.title == "Oven Timer":
            if oventimer_started:
                """pause"""
            else:
                """start"""
                t = threading.Thread(target=oventimer_function, args=(ws, event.id, button.content.text))
                threads.append(t)
                t.start()

        ws.send(update.to_json())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndInteract.py address")
        exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        remote = BeoRemoteHalo(ipaddress,
                               config,
                               on_system_event=on_system_event,
                               on_wheel_event=on_wheel_event,
                               on_button_event=on_button_event)

        remote.connect()
        while threading.active_count() > 1:
            for t in threads:
                t.join()
                print(t, 'is done.')
        print('all done.')
