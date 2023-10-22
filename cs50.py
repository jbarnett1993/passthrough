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