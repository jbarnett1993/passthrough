 '''implement a program that prompts the user for a str in English and then outputs the “emojized” version of that str, converting any codes (or aliases) therein to their corresponding emoji.

 carpedm20.github.io/emoji/all.html?enableList=enable_list_alias '''

implement a program that prompts the user for a str in English and then outputs the “emojized” version of that str, converting any codes (or aliases) therein to their corresponding emoji.

 carpedm20.github.io/emoji/all.html?enableList=enable_list_alias

import requests
from bs4 import BeautifulSoup

def fetch_emoji_dict():
    URL = "https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    emoji_dict = {}
    
    # Extracting emoji and its aliases from the website
    for item in soup.find_all("li", class_="emoji"):
        emoji = item.find("span", class_="icon").text.strip()
        aliases = item.find("span", class_="aliases").text.strip().split(" ")
        for alias in aliases:
            emoji_dict[alias[1:-1]] = emoji  # Remove the colons from the alias
    
    return emoji_dict

def emojize_string(s, emoji_dict):
    for alias, emoji in emoji_dict.items():
        s = s.replace(f":{alias}:", emoji)
    return s

if __name__ == "__main__":
    emoji_dict = fetch_emoji_dict()
    user_input = input("Enter a string with emoji codes: ")
    emojized_output = emojize_string(user_input, emoji_dict)
    print("Emojized string:", emojized_output)