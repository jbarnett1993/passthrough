'''Prompts the user for a level, 
. If the user does not input a positive integer, the program should prompt again.
Randomly generates an integer between 1 and 
, inclusive, using the random module.
Prompts the user to guess that integer. If the guess is not a positive integer, the program should prompt the user again.
If the guess is smaller than that integer, the program should output Too small! and prompt the user again.
If the guess is larger than that integer, the program should output Too large! and prompt the user again.
If the guess is the same as that integer, the program should output Just right! and exit.'''

import random

def get_positive_integer(prompt):
    """Prompts the user for a positive integer and returns it."""
    while True:
        try:
            num = int(input(prompt))
            if num > 0:
                return num
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid positive integer.")

def main():
    # Prompt the user for a level
    level = get_positive_integer("Enter a level (positive integer): ")

    # Randomly generate an integer between 1 and level, inclusive
    secret_number = random.randint(1, level)

    while True:
        # Prompt the user to guess the integer
        guess = get_positive_integer("Guess the integer between 1 and {}: ".format(level))

        # Check the guess
        if guess < secret_number:
            print("Too small!")
        elif guess > secret_number:
            print("Too large!")
        else:
            print("Just right!")
            break

if __name__ == "__main__":
    main()