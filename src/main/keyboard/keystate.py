from typing import Literal


type KeyState = Literal["correct", "present", "absent", "unknown"]


def get_key_state_value(key_state: KeyState) -> int:
    if key_state == "unknown":
        return 0
    if key_state == "absent":
        return 1
    if key_state == "present":
        return 2
    if key_state == "correct":
        return 3
