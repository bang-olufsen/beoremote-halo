import _thread
import json
import sys
import time
import uuid

import websocket


def remove_nulls(d):
    return {k: v for k, v in d.__dict__.items() if v is not None}


class BeoRemoteHaloConfig:
    version = '1.0.1'

    def __init__(self, pages):
        if type(pages) != list:
            pages = [pages]
        self.configuration = {'version': BeoRemoteHaloConfig.version, 'id': str(uuid.uuid1()), 'pages': pages}

    def to_json(self, indent=None):
        return json.dumps(self, default=lambda o: remove_nulls(o), indent=indent)

    class Page:
        def __init__(self, title, buttons=None):
            self.title = title
            self.id = str(uuid.uuid1())
            if type(buttons) != list:
                buttons = [buttons]
            self.buttons = buttons

    class Button:
        def __init__(self, title, content, subtitle=None, value=None, state=None, default=None):
            self.id = str(uuid.uuid1())
            self.title = title
            self.subtitle = subtitle
            self.value = value
            self.state = state
            self.content = content
            self.default = default

        def set_subtitle(self, subtitle=str()):
            self.subtitle = subtitle

        def set_value(self, value=int()):
            self.value = value

        def set_state(self, state=bool()):
            self.state = "active" if state else "inactive"

        def set_default(self, default=bool()):
            self.default = default

    class ContentIcon:
        def __init__(self, icon):
            self.icon = icon

    class ContentText:
        def __init__(self, text):
            self.text = text


class BeoRemoteHalo:

    def __init__(self, host, configuration=BeoRemoteHaloConfig):
        self.ws = websocket.WebSocketApp("ws://{0}:8080".format(host),
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_close=self.on_close)
        self.configuration = configuration

    def run_forever(self):
        def run(*args):
            self.ws.run_forever()

        _thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        print(message)

    def on_close(self, ws, close_status_code, close_msg):
        print("### Connection Closed ###")

    def on_open(self, ws):
        time.sleep(1)
        ws.send(self.configuration.to_json())
        print(self.configuration.to_json(2))

    def run(self):
        self.ws.run_forever()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ConnectAndConfigure.py address")
        exit(1)

    if len(sys.argv) >= 2:
        ipaddress = sys.argv[1]

        kitchenLight = BeoRemoteHaloConfig.Button("Kitchen Light", BeoRemoteHaloConfig.ContentIcon("lights"))
        kitchenLight.set_value(95)
        kitchenLight.set_state(True)
        kitchenLight.set_subtitle("On")

        ovenTimer = BeoRemoteHaloConfig.Button("Oven Timer", BeoRemoteHaloConfig.ContentText("15:45"))
        ovenTimer.set_subtitle("Temperature 200°C")
        ovenTimer.set_default(True)
        ovenTimer.set_value(0)

        diningTable = BeoRemoteHaloConfig.Button("Dining Table", BeoRemoteHaloConfig.ContentIcon("lights"))
        diningTable.set_value(80)
        diningTable.set_state(False)
        diningTable.set_subtitle("Off")

        fireplace = BeoRemoteHaloConfig.Button("Fire Place", BeoRemoteHaloConfig.ContentIcon("fireplace"))
        fireplace.set_subtitle("Ignite")
        fireplace.set_state(False)

        blinds = BeoRemoteHaloConfig.Button("Blinds", BeoRemoteHaloConfig.ContentIcon("blinds"))
        blinds.set_subtitle("Closed")
        blinds.set_value(100)
        blinds.set_state(True)

        tvBackLight = BeoRemoteHaloConfig.Button("TV Backlight", BeoRemoteHaloConfig.ContentIcon("rgb_lights"))
        tvBackLight.set_subtitle("Off")
        tvBackLight.set_value(0)
        tvBackLight.set_state(False)

        livingRoomThermostat = BeoRemoteHaloConfig.Button("Thermostat", BeoRemoteHaloConfig.ContentText("21°C"))
        livingRoomThermostat.set_subtitle("Heating")
        livingRoomThermostat.set_value(55)
        livingRoomThermostat.set_default(True)
        livingRoomThermostat.set_state(False)

        kitchen = BeoRemoteHaloConfig.Page("Kitchen", [kitchenLight, ovenTimer, diningTable])
        livingRoom = BeoRemoteHaloConfig.Page("Kitchen", [fireplace, blinds, tvBackLight, livingRoomThermostat])

        config = BeoRemoteHaloConfig([kitchen, livingRoom])
        remote = BeoRemoteHalo(ipaddress, config)

        remote.run()
