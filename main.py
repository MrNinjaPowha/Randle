from src.main import App


def main():
    app = App()
    app.set_file_locations(
        'resources/wordlist/wordlist.pkl',
        'resources/highscore/highscore.pkl',
        'resources/settings.pkl'
    )
    app.start()


if __name__ == '__main__':
    main()
