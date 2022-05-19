import pickle
from copy import deepcopy

from .prettyTables import Table
from .prettyTables.style_compositions import Compositions


class HighscoreTable(list[list]):
    def __init__(self, headers: list, max_length: int = 100):
        super().__init__()
        self.headers = headers
        self.max_length = max_length
        self.location = 'highscore.pkl'

    def get_place(self, entry0: list) -> int:
        """ Returns index for new theoretical entry. """
        if self.__len__() <= 0:
            return 0

        _, guesses0, word0, time0 = entry0

        for place, entry in enumerate(self):
            if guesses0 < entry[1]:
                return place

            elif guesses0 == entry[1]:
                if len(word0) > len(entry[2]):
                    return place

                elif len(word0) == len(entry[2]) and time0 < entry[3]:
                    return place

        return self.__len__() + 1

    def enumerate_copy(self) -> list[list]:
        enumerated = deepcopy(self)

        for place, entry in enumerate(self):
            enumerated[place].insert(0, place + 1)

        return enumerated

    def print(self, style: int, pause: bool = True, cutoff: int = None, search: str = None, bottom_entry: list = None):
        """
        Prints a prettyTable from self.

        :param style: Table styling.
        :param pause: Adds an empty input at the end.
        :param cutoff: Shortens table to this length.
        :param search: Includes only highscore entries with a name matching this parameter.
        :param bottom_entry: Adds an extra entry at the bottom that did not make it above the cutoff.
        """
        style = Compositions._fields[style]
        table = self.enumerate_copy()

        if search:
            search_results = []

            for entry in table:
                if entry[1] == search:
                    search_results.append(entry)

            table = search_results

        table = table[:cutoff] if cutoff else table
        table.append(bottom_entry) if bottom_entry else None

        if table:
            for entry in table:
                # changes all saved times to formatted strings
                entry[4] = f'{int(entry[4] / 60)}:{"0" if entry[4] % 60 < 10 else ""}{entry[4] % 60}'

            new_table = Table(style_name=style, rows=table, headers=self.headers)
            print(new_table)

        else:
            print('No results to display.')

        if pause:
            print('\nPress [Enter] to go back.')
            input()

    def cut(self):
        """ Shortens table to specified max length. """
        while self.__len__() >= self.max_length:
            self.pop(self.__len__())

    def set_file_location(self, location: str):
        self.location = location
        self.load()

    def save(self):
        """ Saves table to assigned location. """
        with open(self.location, 'wb') as file:
            pickle.dump(self, file)

    def load(self):
        """ Tries to load table from assigned location. """
        try:
            with open(self.location, 'rb') as file:
                self.__iadd__(pickle.load(file))
        except (EOFError, FileNotFoundError):  # ignores if file is empty
            pass
