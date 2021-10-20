import sys
from BeoremoteHalo import BeoRemoteHalo
from BeoremoteHalo import BeoremoteHaloExmaple


def on_system_event(ws, event):
    pass


def on_wheel_event(ws, event):
    print(event.counts)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndInteract.py address")
        exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        config = BeoremoteHaloExmaple()
        remote = BeoRemoteHalo(ipaddress,
                               config,
                               on_system_event=on_system_event,
                               on_wheel_event=on_wheel_event)

        remote.connect()
