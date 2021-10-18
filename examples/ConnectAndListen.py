import sys
import websocket


def on_message(ws, message):
    print(message)


def on_close(ws, close_status_code, close_msg):
    print("### Connection Closed ###")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndListen.py address")
        exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        ws = websocket.WebSocketApp("ws://{0}:8080".format(ipaddress),
                                    on_message=on_message,
                                    on_close=on_close)
        ws.run_forever()
