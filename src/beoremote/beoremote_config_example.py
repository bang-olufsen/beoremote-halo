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

import uuid

from beoremote.configuration import Configuration
from beoremote.icons import Icons
from beoremote.text import Text


class BeoremoteHaloExmaple(Configuration):
    """
    Example configuration for Beoremote Halo
    """

    def __init__(self):
        kitchen_light = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Kitchen Light",
            "On",
            95,
            Configuration.Pages.Buttons.State.ACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        oven_timer = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Oven Timer",
            "Temperature 200°C",
            0,
            Configuration.Pages.Buttons.State.INACTIVE,
            Text("01:35"),
            True,
        )

        dining_table = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Dining Table",
            "Off",
            80,
            Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        fireplace = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Fire Place",
            "Ignite",
            None,
            Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.LIGHTS),
        )

        blinds = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Blinds",
            "Closed",
            100,
            Configuration.Pages.Buttons.State.ACTIVE,
            Icons(Icons.Icon.BLINDS),
        )

        tv_back_light = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "TV Backlight",
            "off",
            0,
            Configuration.Pages.Buttons.State.INACTIVE,
            Icons(Icons.Icon.RGB_LIGHTS),
        )

        living_room_thermostat = Configuration.Pages.Buttons(
            str(uuid.uuid1()),
            "Thermostat",
            "Heating",
            55,
            Configuration.Pages.Buttons.State.INACTIVE,
            Text("21°C"),
            True,
        )

        kitchen = Configuration.Pages(
            "Kitchen", str(uuid.uuid1()), [kitchen_light, oven_timer, dining_table]
        )

        living_room = Configuration.Pages(
            "living room",
            str(uuid.uuid1()),
            [fireplace, blinds, tv_back_light, living_room_thermostat],
        )

        Configuration.__init__(self, str(uuid.uuid1()), [kitchen, living_room])
