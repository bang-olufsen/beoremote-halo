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

import json


def remove_nones(dictionary):
    """

    :param dictionary:
    :return:
    """
    return {k: v for k, v in dictionary.__dict__.items() if v is not None}


class Entity:
    """This is the base class for the model classes. It provides json serialization methods."""

    @classmethod
    def from_json(cls, data):
        json_obj = json.loads(data)
        return cls(**json_obj)

    def to_json(self, sort_keys: bool = False, indent: int = None):
        # pylint: disable=unnecessary-lambda
        return json.dumps(
            self,
            default=lambda o: remove_nones(o),
            sort_keys=sort_keys,
            indent=indent,
            separators=(",", ":"),
        )

    def __str__(self):
        return self.to_json()
