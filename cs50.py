In The Sound of Music, there’s a song sung largely in English, So Long, Farewell, with these lyrics, wherein “adieu” means “goodbye” in French:

Adieu, adieu, to yieu and yieu and yieu

Of course, the line isn’t grammatically correct, since it would typically be written (with an Oxford comma) as:

Adieu, adieu, to yieu, yieu, and yieu

To be fair, “yieu” isn’t even a word; it just rhymes with “you”!

In a file called adieu.py, implement a program that prompts the user for names, one per line, until the user inputs control-d. Assume that the user will input at least one name. Then bid adieu to those names, separating two names with one and, three names with two commas and one and, and 
 names with 
 commas and one and, as in the below:

use the inflect module

import inflect
import sys

def get_names():
    """Prompt the user for names until they input Ctrl-D."""
    names = []
    while True:
        try:
            name = input("Enter a name (Ctrl-D to stop): ")
            names.append(name)
        except EOFError:
            break
    return names

def main():
    p = inflect.engine()
    names = get_names()

    if not names:
        sys.exit("No names were provided.")

    farewell_message = f"Adieu, adieu, to {p.join(names)}"
    print(farewell_message)

if __name__ == "__main__":
    main()