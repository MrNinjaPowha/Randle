import pickle
from time import time
from random import randrange
from .consolefunctions import clear_console as cc, color_text, rgb
from .highscoretable import HighscoreTable


class Game:
    def __init__(self):
        self.settings = {
            'colorblind': False,
            'table_style': 0
        }

        self.wordlist_location = 'wordlist.pkl'
        self.highscore_location = 'highscore.pkl'
        self.settings_location = 'settings.pkl'

        self.wordlist = None
        self.highscore_list = HighscoreTable(['#', 'Name', 'Guesses', 'Word', 'Time'])

        self.answer = ''
        self.guesses = []

    def run(self):
        """Main function of a game class. It resets values and runs the game."""
        self.answer = self.wordlist[randrange(len(self.wordlist))]
        self.guesses.clear()
        start_time = time()

        cc()

        guessing = True

        while guessing:
            while True:
                for guess in self.guesses:
                    # prints previous guesses
                    print(guess)

                if self.guesses:
                    print('')
                print('Enter a valid word to make a guess or give up by entering /Q')

                guess = input().casefold()

                if guess == '/q':
                    # command to give up
                    self.end()
                    guessing = False
                    break

                elif guess in self.wordlist:
                    break  # continues if guess was valid

                else:
                    cc()
                    if len(guess) < 3:
                        print('Your guess has to be 3 letters or longer.\n')
                    else:
                        print(f'{guess.capitalize()} is not a valid word.\n')

            if guess == self.answer:
                self.guesses.append(self.answer)
                self.win(time() - start_time)
                guessing = False

            else:
                self.guesses.append(self.check_guess(guess))

            cc()

    def win(self, guess_time: float):
        """Finishes game and possibly adds player to leaderboard"""
        final_time = round(guess_time)

        cc()
        print(
            'Congratulations! You guessed the correct word:\n'
            f'{self.check_guess(self.answer)}'
        )

        highscore_place = self.highscore_list.get_place(['', len(self.guesses), self.answer, final_time])

        if highscore_place < 100:  # achieved top 100
            print('\nPlease enter your name and you will be placed on the leaderboard.')

            while True:
                name = input()

                if 2 < len(name) < 21:
                    break

                else:  # failed to provide valid name
                    cc()
                    print('Name has to be between 3 and 20 characters')

            self.highscore_list.insert(highscore_place, [name, len(self.guesses), self.answer, final_time])

        cc()
        print('Leaderboard Top 10:\n')

        if highscore_place < 10:  # prints top 10
            self.highscore_list.print(self.settings['table_style'], cutoff=10)

        else:  # prints top 10 and this entry at bottom
            self.highscore_list.print(self.settings['table_style'], cutoff=10, bottom_entry=[
                highscore_place if highscore_place < 100 else '?',
                'You', len(self.guesses), self.answer, final_time
            ])

            self.highscore_list.print(self.settings['table_style'])

    def end(self):
        """Reveals correct word if player gives up"""
        cc()
        print(
            f'The correct word was {self.answer}\n\n'
            'Press [Enter] to go back to the main menu.'
        )
        input()

    def check_guess(self, guess: str, answer: str = None) -> str:
        """
        Returns the guess formatted for a Wordle-like game with colored backgrounds.
        If answer is left empty, then this function will use the answer for the current game.
        """
        output = []
        answer = self.answer if answer is None else answer

        if len(guess) < len(answer) and answer[:len(guess)] == guess:
            # if all letters in guess were correct but the answer is longer
            for letter in guess:
                output.append(self.color_letter(letter, 'green'))

            output.append(self.color_letter('...', 'red'))

        else:
            for i, letter in enumerate(guess):
                if i < len(answer):  # makes sure that answer does not go out of range
                    if letter == answer[i]:
                        output.append(self.color_letter(letter, 'green'))

                    elif letter in answer:
                        output.append(self.color_letter(letter, 'yellow'))

                    else:
                        output.append(self.color_letter(letter, 'gray'))

                elif letter in answer:
                    output.append(self.color_letter(letter, 'yellow'))

                else:
                    output.append(self.color_letter(letter, 'gray'))

        return ''.join(output)

    def color_letter(self, letter: str, color: str) -> str:
        """ Colors a string based on color parameter. Also considers the colorblind option. """
        if color == 'green':
            return color_text(f' {letter} ', background='lime') if not self.settings['colorblind'] else \
                color_text(f' {letter} ', invert=True)

        elif color == 'yellow':
            return color_text(f' {letter} ', background='yellow') if not self.settings['colorblind'] else \
                color_text(f' {letter} ', underline=True, bold=True)

        elif color == 'gray':
            return color_text(f' {letter} ', background=rgb(40, 40, 40)) if not self.settings['colorblind'] else \
                color_text(f' {letter} ', italic=True, faint=True)

        elif color == 'red':
            return color_text(f'{letter}', background='red') if not self.settings['colorblind'] else f'{letter}'

    def set_wordlist(self, location: str):
        """ Sets this games wordlist. File has to exist! """
        self.wordlist_location = location
        with open(location, 'rb') as file:
            self.wordlist = pickle.load(file)

    def set_settings_location(self, location: str = 'settings.pkl'):
        """ Sets settings location and tries to open file. """
        self.settings_location = location

        try:
            with open(location, 'rb') as file:
                settings = pickle.load(file)
                for setting in settings:
                    self.settings[setting] = settings[setting]

        except (FileNotFoundError, EOFError):  # if no file exists or if empty
            self.settings = self.settings

    def save_settings(self):
        """ Saves self.settings. """
        with open(self.settings_location, 'wb') as file:
            pickle.dump(self.settings, file)