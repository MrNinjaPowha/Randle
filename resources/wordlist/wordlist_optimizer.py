import pickle

# Run this script if you wish to add your own wordlist
# This will remove any words shorter than the minimum length and
# that are not alphabetical letters only.
# This script will also remove any words containing any uppercase letters

RAW_WORDLIST_PATH = 'wordlist_raw.txt'
OUTPUT_PATH = 'wordlist.pkl'  # If you change this, make sure to also change the wordlist's location in main.py
MIN_LENGTH = 3


def main():
    with open(RAW_WORDLIST_PATH) as wordlist:
        words = wordlist.read().rsplit()

    output = []

    for word in words:
        if len(word) >= MIN_LENGTH and word.isalpha() and word.islower():
            output.append(word)
        else:
            print(f'Removed {word}')

    with open(OUTPUT_PATH, 'wb') as pickled:
        pickle.dump(output, pickled)


if __name__ == '__main__':
    main()
