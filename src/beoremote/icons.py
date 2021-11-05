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


class Icons(Entity):
    class Icon(str, Enum):
        ALARM = "alarm"
        ALTERNATIVE = "alternative"
        ARM_STAY = "arm_stay"
        AUTO = "auto"
        BATH_TUB = "bath_tub"
        BLINDS = "blinds"
        BLISS = "bliss"
        BUTLER = "butler"
        CINEMA = "cinema"
        CLEAN = "clean"
        CLOCK = "clock"
        COFFEE = "coffee"
        COOL = "cool"
        CREATIVE = "creative"
        CURTAINS = "curtains"
        DINNER = "dinner"
        DISARM = "disarm"
        DOOR = "door"
        DOORLOCK = "doorlock"
        ENERGIZE = "energize"
        ENJOY = "enjoy"
        ENTERTAIN = "entertain"
        FAN = "fan"
        FIREPLACE = "fireplace"
        GAMING = "gaming"
        GARAGE = "garage"
        GATE = "gate"
        GOOD_MORNING = "good_morning"
        GOOD_NIGHT = "good_night"
        HEAT = "heat"
        HUMIDITY = "humidity"
        INDULGE = "indulge"
        LEAVING = "leaving"
        LIGHTS = "lights"
        LOCK = "lock"
        MEETING = "meeting"
        MOVIE = "movie"
        MUSIC = "music"
        NOTIFICATION = "notification"
        OFF = "off"
        PARTY = "party"
        POOL = "pool"
        PRIVACY = "privacy"
        PRODUCTIVE = "productive"
        READING = "reading"
        RELAX = "relax"
        REQUEST_CAR = "request_car"
        RGB_LIGHTS = "rgb_lights"
        ROMANTIC = "romantic"
        ROOF_WINDOW = "roof_window"
        ROOM_SERVICE = "room_service"
        SECURITY = "security"
        SHADES = "shades"
        SHOWER = "shower"
        SLEEP = "sleep"
        SMART_GLASS = "smart_glass"
        SPA = "spa"
        SPRINKLER = "sprinkler"
        TRAVEL = "travel"
        TURNTABLE = "turntable"
        UNLOCK = "unlock"
        VACATION = "vacation"
        WARNING = "warning"
        WATERFALL = "waterfall"
        WELCOME = "welcome"
        WINDOW = "window"
        WORK_OUT = "work_out"
        YOGA = "yoga"

    def __init__(self, icon: Icon):
        assert icon in Icons.Icon
        self.icon = icon
