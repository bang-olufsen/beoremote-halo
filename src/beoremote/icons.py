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

from entity import Entity


class Icons(Entity):  # pylint: disable=invalid-name
    class Icon(str, Enum):
        alarm = "alarm"
        alternative = "alternative"
        arm_stay = "arm_stay"
        auto = "auto"
        bath_tub = "bath_tub"
        blinds = "blinds"
        bliss = "bliss"
        butler = "butler"
        cinema = "cinema"
        clean = "clean"
        clock = "clock"
        coffee = "coffee"
        cool = "cool"
        creative = "creative"
        curtains = "curtains"
        dinner = "dinner"
        disarm = "disarm"
        door = "door"
        doorlock = "doorlock"
        energize = "energize"
        enjoy = "enjoy"
        entertain = "entertain"
        fan = "fan"
        fireplace = "fireplace"
        gaming = "gaming"
        garage = "garage"
        gate = "gate"
        good_morning = "good_morning"
        good_night = "good_night"
        heat = "heat"
        humidity = "humidity"
        indulge = "indulge"
        leaving = "leaving"
        lights = "lights"
        lock = "lock"
        meeting = "meeting"
        movie = "movie"
        music = "music"
        notification = "notification"
        off = "off"
        party = "party"
        pool = "pool"
        privacy = "privacy"
        productive = "productive"
        reading = "reading"
        relax = "relax"
        request_car = "request_car"
        rgb_lights = "rgb_lights"
        romantic = "romantic"
        roof_window = "roof_window"
        room_service = "room_service"
        security = "security"
        shades = "shades"
        shower = "shower"
        sleep = "sleep"
        smart_glass = "smart_glass"
        spa = "spa"
        sprinkler = "sprinkler"
        travel = "travel"
        turntable = "turntable"
        unlock = "unlock"
        vacation = "vacation"
        warning = "warning"
        waterfall = "waterfall"
        welcome = "welcome"
        window = "window"
        work_out = "work_out"
        yoga = "yoga"

    def __init__(self, icon: Icon):
        assert icon in Icons.Icon
        self.icon = icon
