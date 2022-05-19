from src.main import App


def main():
    app = App()
    app.set_file_locations(
        wordlist='resources/wordlist/wordlist.pkl',
        highscore='resources/highscore/highscore.pkl',
        settings='resources/settings.pkl'
    )
    app.start()


if __name__ == '__main__':
    main()
