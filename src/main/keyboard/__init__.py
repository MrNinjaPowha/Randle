from typing import Callable

from .keystate import get_key_state_value, KeyState
from .key import Key


class Keyboard:
    def __init__(self, color_letter: Callable[[str, str], str]):
        self.color_letter = color_letter
        self.layout = [
            [Key(key, "unknown") for key in "qwertyuiop"],
            [Key(key, "unknown") for key in "asdfghjkl"],
            [Key(key, "unknown") for key in "zxcvbnm"],
        ]
        self.indent = ["", " ", "  "]

    def get_key(self, key: str) -> Key | None:
        for row in self.layout:
            for key_obj in row:
                if key_obj.name == key:
                    return key_obj

    def get_key_state(self, key: str) -> KeyState:
        if self.get_key(key):
            return self.get_key(key).state

        return "unknown"

    def set_key_state(self, key: str, state: KeyState):
        if self.get_key(key):
            self.get_key(key).state = state

    def increase_key_state(self, key: str, state: KeyState):
        key_obj = self.get_key(key)

        if not key_obj:
            return

        if get_key_state_value(key_obj.state) < get_key_state_value(state):
            key_obj.state = state

    def color_key(self, key: Key):
        if key.state == "correct":
            return self.color_letter(key.name, "green")
        elif key.state == "present":
            return self.color_letter(key.name, "yellow")
        elif key.state == "absent":
            return self.color_letter(key.name, "gray")
        else:
            return f" {key.name} "

    def __str__(self):
        output = ""

        for i, row in enumerate(self.layout):
            output += self.indent[i]

            for key in row:
                output += self.color_key(key)

            if i < len(self.layout) - 1:
                output += "\n"

        return output
