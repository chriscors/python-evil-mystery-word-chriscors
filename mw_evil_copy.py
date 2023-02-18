import numpy as np


def subset_list_randomly(dictionary) -> list:
    import random
    length = random.choice(range(4, 8))

    filtered = list(filter(lambda w: len(w) == length, dictionary))
    return filtered


def get_list(guess_letter: str, current_word: list, dictionary) -> list:

    current_word_iterations = [
        list("".join(current_word)) for _ in range(len(current_word))]
    counter = 0
    pop = []
    for letter_list in current_word_iterations:

        if letter_list[counter] == "_":
            letter_list[counter] = guess_letter
        else:
            pop.append(counter)
        counter += 1

    counter = 0
    for ind in pop:
        ind -= counter
        current_word_iterations.pop(ind)
        counter += 1

    # pair down the list further to only those that actually include the word
    dictionary = list(filter(lambda word: guess_letter in word, dictionary))

    # make buckets
    words_buckets = [[] for _ in range(len(letter_list))]
    # make buckets

    for word in dictionary:
        split_word = list(word)
        counter = 0

        for test_word in current_word_iterations:
            word_fits = True
            index = 0
            for test_letter in test_word:
                if (test_letter != split_word[index] and
                        test_letter != "_"):
                    word_fits = False
                index += 1
            if word_fits:
                words_buckets[counter].append(word)
            counter += 1

    dictionary = max(words_buckets, key=len)
    index = words_buckets.index(dictionary)
    return dictionary, current_word_iterations[index]


def play_game():
    from pathlib import Path
    file = Path("dictionary.txt")
    with open(file) as opened_file:
        dictionary = opened_file.read()
    dictionary = dictionary.upper()
    dictionary = dictionary.split('\n')
    dictionary = subset_list_randomly(dictionary)
    # Declare vars
    # Empty list the ength of the random words
    current_guess = ["_"] * len(dictionary[0])
    guesses = []

    # Track state
    guesses_remaining = 15

    # First tell user how many letters:
    print(f'''
Welcome to ~EvIl~ Hangman!
You secret word has {len(current_guess)} letters.

Current guess:
{" ".join(current_guess)}''')

    while guesses_remaining > 0:
        guess = input("Take a guess! ").upper()

        print()
        if guess in guesses:
            print(f'You already guessed {guess}! Try again?')
            print(f'You have {guesses_remaining} guesses left.')
            print()
            print('Current guess:')
            print(" ".join(current_guess))
            print()
        elif guess not in "".join(dictionary):
            guesses_remaining -= 1
            print(f'Sorry! {guess} was not in the word.')
            print(f'You have {guesses_remaining} guesses left.')
            print()
            print('Current guess:')
            print(" ".join(current_guess))
            print()
        else:
            dictionary, current_guess = get_list(
                guess, current_guess, dictionary)
            if "_" not in current_guess:
                print(f"YES! The word was {current_guess}")
                print()
                if input("You win! Play again? (y/n):") == "y":
                    print()
                    play_game()
                else:
                    break
            else:
                print(f'Yes! {guess} was in the word.')
                print(f'You have {guesses_remaining} guesses left.')
                print()
                print('Current guess:')
                print(" ".join(current_guess))
                print()
        guesses.append(guess)
        # If loss
    print(f"Good try! The word was {word}.")
    if input("Play again? (y/n):") == y:
        print()
        play_game()
    else:
        pass


if __name__ == "__main__":

    play_game()
