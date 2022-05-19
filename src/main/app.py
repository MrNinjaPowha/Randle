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
                '[2] Highscores\n'
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
        example_headers = ['#', 'Name', 'Guesses', 'Word', 'Time']
        example_table = [
            [1, 'The Best', 5, 'introduction', 135],
            [2, 'I Tried', 12, 'remedy', 218]
        ]
        menu_open = True

        while menu_open:
            cc()
            table = Table(
                style_name=Compositions._fields[self.game.settings["table_style"]],
                rows=example_table,
                headers=example_headers
            )

            print(
                f'[1] Turn {"off" if self.game.settings["colorblind"] else "on"} colorblind mode\n'
                f'[2] Leaderboard style: {self.game.settings["table_style"]}\n'
                f'{table}\n'

                '\n[S] Save settings\n'
                '[C] Cancel'
            )

            command = input()

            if command == '1':
                self.game.settings['colorblind'] = not self.game.settings['colorblind']

            if command == '2':
                if self.game.settings['table_style'] + 1 >= len(Compositions._fields):
                    self.game.settings['table_style'] = 0

                else:
                    self.game.settings['table_style'] += 1

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
        cc()
        print(
            'In Randle the goal is to guess a randomized word.\n'
            'Each guess must be a valid word that is longer than 2 letters.\n\n'

            'After you have guessed, the word you just guessed will appear again but each letter will get a\n'
            'background color that shows how close your guess is to the correct word\n\n'

            'Example (the correct word is LOBBY):\n'
            f'{self.game.check_guess("table", "lobby")}\n\n\n'

            'Since the word can be any length longer than 2 letters, you might not know how long the word is.\n'
            'However, if you make a guess where all the letters were correct, but the correct word is longer,\n'
            'then you will get an indication that there are still more letters to find.\n\n'

            'Example (the correct word is HEALTHY):\n'
            f'{self.game.check_guess("heal", "healthy")}\n\n'

            'Press [Enter] to go back.'
        )
        input()

    def set_file_locations(self, wordlist: str, highscore: str, settings: str):
        self.game.set_wordlist(wordlist)
        self.game.highscore_list.set_file_location(highscore)
        self.game.set_settings_location(settings)