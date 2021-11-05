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

from enum import Enum
from typing import Sequence

from beoremote.entity import Entity


class Configuration(Entity):
    class Configuration(Entity):
        class Pages(Entity):
            class Buttons(Entity):
                class State(str, Enum):
                    ACTIVE = "active"
                    INACTIVE = "inactive"

                def __init__(
                    self,
                    button_id: str,
                    title: str,
                    subtitle: str,
                    value: int,
                    state: State,
                    content,
                    default: bool = False,
                ):  # pylint: disable=too-many-arguments
                    self.id = button_id
                    self.title = title
                    self.subtitle = subtitle
                    self.value = value
                    self.state = state
                    self.content = content
                    self.default = default

                def toggle_state(self):
                    if self.state == self.State.ACTIVE:
                        self.state = self.State.INACTIVE
                    else:
                        self.state = self.State.ACTIVE

            def __init__(self, title: str, page_id: str, buttons: Sequence[Buttons]):
                self.title = title
                self.id = page_id
                self.buttons = buttons

        def __init__(self, configuration_id: str, pages: Sequence[Pages]):
            self.version = "1.0.1"
            self.id = configuration_id
            self.pages = pages

    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def __getitem__(self, item):
        for page in self.configuration.pages:
            for button in page.buttons:
                if button.id == item:
                    return button
        return None
