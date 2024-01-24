import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

from csv import DictReader


base_url = "https://quotes.toscrape.com"


def read_quotes(filename_of_csv):
    with open(filename_of_csv, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)  # needs to be in a list to be usable


def game_logic(quotes):
    quote = choice(quotes)
    rem_guesses = 4
    print("Here's a quote: ")
    print(quote["text"])
    guess = ''
    while guess.lower() != quote["author"].lower() and rem_guesses > 0:
        guess = input(
            f"Who said this quote? Guesses remaining: {rem_guesses} \n")
        if guess.lower() == quote["author"].lower():
            print("Correct!")
            break

        rem_guesses -= 1
        if rem_guesses == 3:
            res = requests.get(f"{base_url}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birthday = soup.find(class_="author-born-date").get_text()
            birthplace = soup.find(class_="author-born-location").get_text()
            print(
                f"Here's a hint: The author was born on {birthday} {birthplace}")

        elif rem_guesses == 2:
            print(
                f"Here's a hint: The author's first name starts with: {quote['author'][0]}")

        elif rem_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(
                f"Here's a hint: The author's last name starts with: {last_initial}")

        else:
            print(
                f"Sorry, you ran out of guesses. The answer was {quote['author']}")

    again = ''  # need filler variable for while loops
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)? ")
    if again.lower() in ('yes', 'y'):
        return game_logic(quotes)
    else:
        print("BYE!")


quotes = read_quotes("quotes.csv")
game_logic(quotes)
