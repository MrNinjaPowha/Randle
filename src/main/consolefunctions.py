from dataclasses import dataclass
import os
from typing import Literal

CLEAR = "\033[0m"
ATTRIBUTES = {
    "bold": "\033[1m",
    "faint": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "invert": "\033[7m",
}
COLORS = ["black", "red", "lime", "yellow", "blue", "purple", "cyan", "white"]

type Color = Literal[
    "black", "red", "lime", "yellow", "blue", "purple", "cyan", "white"
]


@dataclass
class RGB:
    red: int
    green: int
    blue: int


def clear_console():
    """Clears Windows or Linux console."""
    command = "cls" if os.name in ("nt", "dos") else "clear"
    os.system(command)


def get_ANSI_color(color: Color | RGB, background: bool = False) -> str:
    """Returns the ANSI escape code for a color or RGB value."""
    if color in COLORS:
        return f"\033[{'4' if background else '3'}{COLORS.index(color)}m"
    elif isinstance(color, RGB):
        return f"\033[{'4' if background else '3'}8;2;{color.red};{color.green};{color.blue}m"
    else:
        raise ValueError(f"{color} is not a valid color")


def color_text(
    text: str, color: Color | RGB = None, background: Color | RGB = None, **kwargs
) -> str:
    """
    Colors a string in a console. Be aware that it does not work in every console.
    :param text: The string to be colored.
    :param color: Can be a named color string or a rgb-value.
    :param background: Colors the background to the text, takes same values as color.
    :param kwargs: Add any extra styling such as bold or italic. Formatting: bold=True.
    :return: A string combined with ANSI Escape Codes.
    """
    # formats color and background into ANSI Escaped Codes
    color = get_ANSI_color(color) if color else ""
    background = get_ANSI_color(background, background=True) if background else ""

    style = []
    for arg in kwargs:
        # adds all kwargs that exists in attributes dict
        if arg in ATTRIBUTES:
            style.append(ATTRIBUTES[arg])

    return f'{color}{background}{"".join(style)}{text}{CLEAR}'
