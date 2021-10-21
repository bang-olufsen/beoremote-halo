import sys
import time
from multiprocessing import Process, Semaphore

from BeoremoteHalo import BeoRemoteHalo
from BeoremoteHalo import BeoRemoteHaloConfig
from BeoremoteHalo import BeoRemoteHaloUpdateButton
from BeoremoteHalo import BeoremoteHaloExmaple

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


def on_system_event(ws, event):
    """

    :param ws:
    :param event:
    """


def on_wheel_event(ws, event):
    """

    :param ws:
    :param event:
    """
    button = config[event.id]
    if button and button.value is not None:
        button.value = clamp(button.value + event.counts * 5, 0, 100)
        update = BeoRemoteHaloUpdateButton(event.id, value=button.value)
        ws.send(update)


def oven_timer_function(ws, button_id, content):
    """

    :param ws:
    :param button_id:
    :param content:
    """
    try:
        minutes, seconds = content.text.split(":")
        for m in range(int(minutes), -1, -1):
            for s in range(int(seconds), -1, -1):
                semaphore.acquire()
                semaphore.release()
                content = BeoRemoteHaloConfig.ContentText("{:02d}:{:02d}".format(m, s))
                update = BeoRemoteHaloUpdateButton(button_id, content=content)
                ws.send(update)
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
                """pause"""
                semaphore.acquire()
                oven_timer["running"] = not oven_timer["running"]
            else:
                if len(processes) > 0:
                    print("resume timer")
                    oven_timer["running"] = not oven_timer["running"]
                else:
                    """start"""
                    p = Process(target=oven_timer_function, args=(beoremote_halo, event.id, button.content))
                    oven_timer["running"] = True
                    processes.append(p)
                    p.start()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndInteract.py address")
        sys.exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        remote = BeoRemoteHalo(ipaddress,
                               config,
                               on_system_event=on_system_event,
                               on_wheel_event=on_wheel_event,
                               on_button_event=on_button_event)

        remote.connect()
        for process in processes:
            process.terminate()

    sys.exit()
