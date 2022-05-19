import os

CLEAR = '\033[0m'
ATTRIBUTES = {
    'bold': '\033[1m',
    'faint': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'invert': '\033[7m'
}
COLORS = [
    'black',
    'red',
    'lime',
    'yellow',
    'blue',
    'purple',
    'cyan',
    'white'
]


def clear_console():
    """ Clears Windows or Linux console. """
    command = 'cls' if os.name in ('nt', 'dos') else 'clear'
    os.system(command)


def rgb(red: int, green: int, blue: int) -> str:
    """ Returns a string that gives the correct color for the color_text function. """
    return f'8;2;{red};{green};{blue}'


def color_text(text: str, color=None, background=None, **kwargs) -> str:
    """
    Colors a string in a console. Be aware that it does not work in every console.
    :param text: The string to be colored.
    :param color: Can be a named color string or a rgb-value.
    :param background: Colors the background to the text, takes same values as color.
    :param kwargs: Add any extra styling such as bold or italic. Formatting: bold=True.
    :return: A string combined with ANSI Escape Codes.
    """
    for arg in (color, background):
        if arg is not None:
            # makes sure that both color and background are valid
            if not isinstance(arg, str):
                raise ValueError(f'{[i for i, a in locals().items() if a == arg][0]} can not be of type {type(arg)}, '
                                 f'only a color name or rgb() is accepted')
            elif not (arg in COLORS or arg[:4] == '8;2;'):
                raise ValueError(f'{arg} is not a valid color')

    # formats color and background into ANSI Escaped Codes
    color = f'\033[3{COLORS.index(background) if color in COLORS else color}m' \
        if color is not None else ''
    background = f'\033[4{COLORS.index(background) if background in COLORS else background}m' \
        if background is not None else ''

    style = []
    for arg in kwargs:
        # adds all kwargs that exists in attributes dict
        if kwargs[arg]:
            style.append(ATTRIBUTES[arg])

    return f'{color}{background}{"".join(style)}{text}{CLEAR}'
