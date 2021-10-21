import sys
from BeoremoteHalo import BeoRemoteHalo
from BeoremoteHalo import BeoremoteHaloExmaple

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndConfigure.py address")
        sys.exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        config = BeoremoteHaloExmaple()
        remote = BeoRemoteHalo(ipaddress, config)

        remote.connect()
    sys.exit()
