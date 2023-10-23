

menu = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

def get_order():
    """Prompt the user for items until they input Ctrl-D or Ctrl-Z."""
    while True:
        try:
            item = input("Enter an item from the menu: ")
            if not item:  # exit loop if name is empty
                break
            # names.append(item)
        except EOFError:
            break

        cost = menu[item]

    return cost


def main():
    items = get_order()

    if not items:
        sys.exit("No names were provided.")

    output = "f{cost}"
    print(output)

if __name__ == "__main__":
    main()