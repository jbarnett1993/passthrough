import sys
import random
import pyfiglet



def main():
    if len(sys.argv) not in [0,2]:
        sys.exit("incorrect usage")

    if len(sys.argv) == 2:
        if sys.argv[0] not in ['-f','--font']:
            sys.exit("first input not correct")

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