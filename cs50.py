import sys
import random
import pyfiglet

print("testing")


def main():
    if len(sys.argv) not in [1,3]:
        sys.exit("incorrect usage")

    if len(sys.argv) == 3:
        if sys.argv[1] not in ['-f','--font']:
            sys.exit("first input not correct")
        print(sys.argv[2])
        font = sys.argv[2]
        if font not in pyfiglet.FigletFont.getFonts():
            sys.exit(f"Font {font} is not supported")

        else:
            font = random.choice(pyfiglet.FigletFont.getFonts())

        text = input("Enter text:")

        result = pyfiglet.figlet_format(text, font=font)
        print(result)

if __name__ == "__main__":
    main()