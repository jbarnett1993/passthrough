import inflect
import sys

def get_names():
    """Prompt the user for names until they input Ctrl-D or Ctrl-Z."""
    names = []
    while True:
        try:
            name = input("Enter a name (Ctrl-D or Ctrl-Z to stop, or just press Enter): ")
            if not name:  # exit loop if name is empty
                break
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