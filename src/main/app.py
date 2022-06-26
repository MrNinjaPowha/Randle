import os.path

from .prettyTables import Table
from .prettyTables.style_compositions import Compositions

from .consolefunctions import clear_console as cc
from .game import Game


class App:
    def __init__(self):
        self.game = Game()

    def start(self):
        """ Opens start menu and is always returned to until the user quits. """
        while True:
            cc()
            print(
                'Welcome to Randle, Wordle but with an unknown length of the word.\n'
                '[1] Start\n'
                '[2] Leaderboard\n'
                '[3] Settings\n'
                '[4] Help\n'
                '[Q] Quit'
            )

            command = input()

            if command == '1':
                self.game.run()

            elif command == '2':
                self.highscore_menu()

            elif command == '3':
                self.settings_menu()

            elif command == '4':
                self.help_menu()

            elif command.casefold() == 'q':
                break

    def settings_menu(self):
        old_settings = self.game.settings.copy()
        menu_open = True

        while menu_open:
            cc()

            print(
                f'[1] Turn {"off" if self.game.settings["colorblind"] else "on"} colorblind mode\n'
                f'[2] Leaderboard style: {self.game.settings["table_style"]}\n'
                f'[3] Turn {"off" if self.game.settings["animations"] else "on"} animations\n'

                '\n[S] Save settings\n'
                '[C] Cancel'
            )

            command = input()

            if command == '1':
                self.game.settings['colorblind'] = not self.game.settings['colorblind']

            if command == '2':
                self.table_style_menu()

            if command == '3':
                self.game.settings['animations'] = not self.game.settings['animations']

            elif command.casefold() in ('s', 'c'):
                if old_settings != self.game.settings:  # if settings were changed then confirmation is required
                    while True:
                        cc()
                        if command.casefold() == 's':
                            print('Are you sure you want to save your settings?')
                        else:
                            print('Are you sure you want to discard any changes you have made?')

                        print('[Y] Yes  [N] No')

                        yes_or_no = input()

                        if yes_or_no.casefold() == 'y':
                            if command.casefold() == 'c':
                                self.game.settings = old_settings  # restores previous settings

                            self.game.save_settings()

                            menu_open = False
                            break

                        if yes_or_no.casefold() == 'n':
                            break

                else:
                    menu_open = False

    def table_style_menu(self):
        example_headers = ['#', 'Name', 'Guesses', 'Word', 'Time']
        example_table = [
            [1, 'First', 5, 'example', 135],
            [2, 'Second', 12, 'test', 218],
            [3, 'Third', 15, 'table', 254]
        ]

        cc()

        while True:
            table = Table(
                style_name=Compositions._fields[self.game.settings["table_style"]],
                rows=example_table,
                headers=example_headers
            )

            print(
                f'Leaderboard style: {self.game.settings["table_style"]}\n\n'
                
                f'{table}\n\n'
                
                f'Enter a number between 0 and {len(Compositions._fields)} to select a style or press [Enter] to '
                f'cycle through all options.\n'
                f'[S] Save and go back'
            )

            command = input()

            if command.casefold() == 's':
                break

            elif command.isnumeric():
                if int(command) > len(Compositions._fields):
                    cc()
                    print(f'{command} is too large.')

                else:
                    self.game.settings['table_style'] = int(command)
                    cc()

            else:
                if self.game.settings['table_style'] + 1 >= len(Compositions._fields):
                    self.game.settings['table_style'] = 0

                else:
                    self.game.settings['table_style'] += 1

                cc()

    def highscore_menu(self):
        while True:
            cc()
            print(
                '[1] Display top 10\n'
                '[2] Display the full leaderboard\n'
                '[3] Search for entries\n'
                '[C] Cancel'
            )

            command = input()
            cc()

            if command == '1':
                self.game.highscore_list.print(self.game.settings['table_style'], cutoff=10)

            elif command == '2':
                self.game.highscore_list.print(self.game.settings['table_style'])

            elif command == '3':
                print('Enter a name to search for all of their entries:')
                self.game.highscore_list.print(self.game.settings['table_style'], search=input())

            elif command.casefold() == 'c':
                break

    def help_menu(self):
        examples = [self.game.check_guess('table', 'lobby'), self.game.check_guess('heal', 'healthy')]
        if self.game.settings["animations"]:
            for i in range(2):
                examples[i] = ''.join(examples[i])

        cc()
        print(
            'In Randle the goal is to guess a randomized word.\n'
            'Each guess must be a valid word that is longer than 2 letters.\n\n'

            'After you have guessed, the word you just guessed will appear again but each letter will get a\n'
            'background color that shows how close your guess is to the correct word.\n\n'

            'Example (the correct word is LOBBY):\n'
            f'{examples[0]}\n\n\n'

            'Since the word can be any length longer than 2 letters, you might not know how long the word is.\n'
            'However, if you make a guess where all the letters were correct, but the correct word is longer,\n'
            'then you will get an indication that there are still more letters to find.\n\n'

            'Example (the correct word is HEALTHY):\n'
            f'{examples[1]}\n\n'

            'Press [Enter] to go back.'
        )
        input()

    def set_file_locations(self, **kwargs: str):
        for arg in kwargs.values():
            # creates any missing folders
            path = '/'.join(arg.split('/')[:-1])
            if not os.path.exists(path):
                os.mkdir(path)

        self.game.set_wordlist(kwargs.get('wordlist'))
        self.game.highscore_list.set_file_location(kwargs.get('highscore'))
        self.game.set_settings_location(kwargs.get('settings'))
