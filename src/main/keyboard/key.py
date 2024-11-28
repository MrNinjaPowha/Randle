from dataclasses import dataclass

from . import KeyState


@dataclass
class Key:
    name: str
    state: KeyState
