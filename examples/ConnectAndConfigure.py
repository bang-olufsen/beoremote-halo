import sys
from BeoremoteHalo import BeoRemoteHalo
from BeoremoteHalo import BeoRemoteHaloConfig

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
