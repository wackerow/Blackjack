print("♠️♥️♦️♣️")

class Player():

    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

class Deck():

    def __init__(self, deck_count=6):
        self.deck_count = deck_count

class Card():

    card_values_dict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                        "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    card_colors_dict = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}

    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.value = self.card_values_dict[name]
        self.color = self.card_colors_dict[suit]


