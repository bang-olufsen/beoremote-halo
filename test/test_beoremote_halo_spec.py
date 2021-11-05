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

import unittest

from src.beoremote.configuration import Configuration
from src.beoremote.event import Event
from src.beoremote.icons import Icons
from src.beoremote.text import Text
from src.beoremote.update import Update
from src.beoremote.updateButton import UpdateButton
from src.beoremote.updateDisplayPage import UpdateDisplayPage
from src.beoremote.updateNotification import UpdateNotification


class MyTestCase(unittest.TestCase):
    def test_button_update_text(self):
        update_string = (
            r'{"update":{"type":"button","id":'
            r'"497f6eca-6276-4993-bfeb-53cbbbba6f08","title":"string","subtitle":'
            r'"string","value":100,"state":"active","content":{'
            r'"text":"string"}}}'
        )

        button = Update(
            UpdateButton(
                "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "string",
                "string",
                100,
                UpdateButton.State.active,
                Text("string"),
            )
        )

        self.assertEqual(update_string, button.to_json())

    def test_button_update_icon(self):
        update_string = (
            r'{"update":{"type":"button","id":'
            r'"497f6eca-6276-4993-bfeb-53cbbbba6f08","title":"string","subtitle":'
            r'"string","value":100,"state":"active","content":{'
            r'"icon":"lights"}}}'
        )

        button = Update(
            UpdateButton(
                "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "string",
                "string",
                100,
                UpdateButton.State.active,
                Icons(Icons.Icon.LIGHTS),
            )
        )

        self.assertEqual(update_string, button.to_json())

    def test_config(self):
        config_string = (
            r'{"configuration":{"version":"1.0.1","id":'
            r'"497f6eca-6276-4993-bfeb-53cbbbba6f08","pages":[{"title":"string",'
            r'"id":"3d042361-b046-423a-a9f4-8ec4a5952476","buttons":[{"id":'
            r'"470710e1-8ea1-412a-827d-48ff406cb482","title":"string","subtitle":'
            r'"string","value":100,"state":"active","content":{"text":"string"},'
            r'"default":true}]}]}}'
        )

        button = Configuration.Configuration.Pages.Buttons(
            "470710e1-8ea1-412a-827d-48ff406cb482",
            "string",
            "string",
            100,
            Configuration.Configuration.Pages.Buttons.State.ACTIVE,
            Text("string"),
            True,
        )

        page = Configuration.Configuration.Pages(
            "string", "3d042361-b046-423a-a9f4-8ec4a5952476", [button]
        )

        configuration = Configuration(
            Configuration.Configuration("497f6eca-6276-4993-bfeb-53cbbbba6f08", [page])
        )

        self.assertEqual(config_string, configuration.to_json())

    def test_power_event(self):
        power_event = Event.from_json(
            r'{"event":{"type":"power","capacity":80,"state":"discharging"}}'
        ).event

        self.assertEqual(power_event.type, "power")
        self.assertEqual(power_event.state, "discharging")
        self.assertEqual(power_event.capacity, 80)

    def test_system_event(self):
        system_event = Event.from_json(
            r'{"event":{"type":"system","state":"active"}}'
        ).event

        self.assertEqual(system_event.type, "system")
        self.assertEqual(system_event.state, "active")

    def test_wheel_event(self):
        wheel_event = Event.from_json(
            r'{"event":{"type":"wheel","id":"470710e1-8ea1-412a-827d-48ff406cb482", "counts": -5}}'
        ).event

        self.assertEqual(wheel_event.type, "wheel")
        self.assertEqual(wheel_event.id, "470710e1-8ea1-412a-827d-48ff406cb482")
        self.assertEqual(wheel_event.counts, -5)

    def test_status_event(self):
        system_event = Event.from_json(
            r'{"event":{"type":"status", "state": "ok"}}'
        ).event

        self.assertEqual(system_event.type, "status")
        self.assertEqual(system_event.state, "ok")
        self.assertEqual(system_event.message, None)

        system_event = Event.from_json(
            r'{"event":{"type":"status", "state": "error", "message": "Some Error Message"}}'
        ).event

        self.assertEqual(system_event.type, "status")
        self.assertEqual(system_event.state, "error")
        self.assertEqual(system_event.message, "Some Error Message")

    def test_button_event(self):
        button_event = Event.from_json(
            r'{"event":{"type":"button", "id": "470710e1-8ea1-412a-827d-48ff406cb482", "state": '
            r'"pressed"}}'
        ).event

        self.assertEqual(button_event.type, "button")
        self.assertEqual(button_event.id, "470710e1-8ea1-412a-827d-48ff406cb482")
        self.assertEqual(button_event.state, "pressed")

        button_event = Event.from_json(
            r'{"event":{"type":"button", "id": "470710e1-8ea1-412a-827d-48ff406cb482", "state": '
            r'"released"}}'
        ).event

        self.assertEqual(button_event.type, "button")
        self.assertEqual(button_event.id, "470710e1-8ea1-412a-827d-48ff406cb482")
        self.assertEqual(button_event.state, "released")

    def test_unknown_event(self):
        unknown_event = Event.from_json(r'{"event":{"type":"unknown"}}').event

        self.assertEqual(unknown_event, None)

    def test_update_notification(self):
        update_string = (
            r'{"update":{"type":"notification",'
            r'"id":"7f703610-5133-4b94-aab6-f3d59acb6537",'
            r'"title":"Kitchen","subtitle":"Long description..."}}'
        )
        notification = UpdateNotification(
            "7f703610-5133-4b94-aab6-f3d59acb6537", "Kitchen", "Long description..."
        )
        update = Update(notification)
        self.assertEqual(update_string, update.to_json())

    def test_update_displaypage(self):
        update_string = (
            r'{"update":{"type":"displaypage",'
            r'"pageid":"c3f5c128-7373-4a09-ae75-c7adfa990211"}}'
        )
        display_page = UpdateDisplayPage("c3f5c128-7373-4a09-ae75-c7adfa990211")
        update = Update(display_page)
        self.assertEqual(update_string, update.to_json())
