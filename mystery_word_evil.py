import numpy as np


def process_file() -> list:
    """Processes the dictionary file from file to a useable list

    Returns:
        list: Processed list from file
    """
    from pathlib import Path
    file = Path("dictionary.txt")
    with open(file) as opened_file:
        dictionary = opened_file.read()
    dictionary = dictionary.upper()
    return dictionary.split('\n')


def subset_list_randomly(dictionary: list) -> list:
    """Receives a dictionary of words and subsets it based on a random number

    Args:
        dictionary (list): List of words

    Returns:
        list: Subsetted list of words
    """
    import random
    length = random.choice(range(4, 8))

    filtered = list(filter(lambda w: len(w) == length, dictionary))
    return filtered


def get_list(guess_letter: str, current_word: list, dictionary) -> list:
    """Updates the list of possible words to the largest possibility of english words based on current guess

    Args:
        guess_letter (str): Letter guessed by user
        current_word (list): List of past guesses / "_"
        dictionary (List): All current possible words

    Returns:
        list: Returns dictionary, new current word
    """

    #current_word_iterations = [current_word]*len(current_word)
    # FOUND BEHAVIOR
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
    # get dictionary from file
    dictionary = process_file()

    # get a random length and partiion dictionary
    dictionary = subset_list_randomly(dictionary)

    # Declare vars
    # Empty list of underscores the length of the random words
    current_guess = ["_"] * len(dictionary[0])
    # Empty user guesses
    guesses = []

    # Track state
    guesses_remaining = 8

    # First tell user how many letters:
    print(f'''
Welcome to ~EvIl~ Hangman!
Your secret word has {len(current_guess)} letters.

Current guess:
{" ".join(current_guess)}''')

    while guesses_remaining > 0:
        guess = input("Take a guess! ").upper()

        print()
        # Ensure validity
        if len(guess) > 1 or not guess.isalpha():
            print(f'That guess is invalid.')
            print(f'You have {guesses_remaining} guesses left.')
            print()
            print('Current guess:')
            print(" ".join(current_guess))
            print()
        # Ensure not already guessed
        elif guess in guesses:
            print(f'You already guessed {guess}! Try again?')
            print(f'You have {guesses_remaining} guesses left.')
            print()
            print('Current guess:')
            print(" ".join(current_guess))
            print()
        # Ensure guess in possible words
        elif guess not in "".join(dictionary):
            guesses_remaining -= 1
            print(f'Sorry! {guess} was not in the word.')
            print(f'You have {guesses_remaining} guesses left.')
            print()
            print('Current guess:')
            print(" ".join(current_guess))
            print()
        else:
            # Get list of possible words, update current guess
            dictionary, current_guess = get_list(
                guess, current_guess, dictionary)
            # If all guesses correct
            if "_" not in current_guess:
                print(f"YES! The word was {current_guess}")
                print()
                if input("You win! Play again? (y/n):") == "y":
                    print()
                    play_game()
                else:
                    return
            # If guess correct but not complete
            else:
                print(f'Yes! {guess} was in the word.')
                print(f'You have {guesses_remaining} guesses left.')
                print()
                print('Current guess:')
                print(" ".join(current_guess))
                print()
        # Track past guesses
        guesses.append(guess)
    # If loss
    print(f"Good try! The word was {dictionary[0]}.")
    if input("Play again? (y/n):") == "y":
        print()
        play_game()
    else:
        return


if __name__ == "__main__":

    play_game()
