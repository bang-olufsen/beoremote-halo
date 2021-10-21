import sys
from BeoremoteHalo import BeoRemoteHalo

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndListen.py address")
        sys.exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        remote = BeoRemoteHalo(ipaddress)
        remote.connect()

    sys.exit()