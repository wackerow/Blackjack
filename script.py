"""
Blackjack Game
"""
import random

card_values_dict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                    "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
card_colors_dict = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}

max_players = 4

class Deck:

    def __init__(self, deck_count=6):
        self.deck_count = deck_count  # Must be ≥1
        self.cards = []
        for _ in range(self.deck_count):
            for suit in card_colors_dict.keys():
                for name in card_values_dict.keys():
                    self.cards.append(Card(name, suit))
        self.shuffle_deck()

    def __repr__(self):
        return str(self.cards)

    def shuffle_deck(self):
        random.shuffle(self.cards)


class Card:

    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.value = card_values_dict[name]
        self.color = card_colors_dict[suit]

    def __repr__(self):
        return self.name + self.suit


class Dealer:

    active_hand = []

    def __init__(self):
        pass

    def __repr__(self):
        return "Dealer"

    def deal_new(self, hand):
        self.active_hand.append(hand)

    def reset_hand(self):
        # Delete active "hand" object
        del self.active_hand[0]

        # Clear active_hand array
        self.active_hand.clear()


class Player:

    def __init__(self, name):
        self.name = name
        self.balance = 100
        self.current_bet = 0
        self.hands = []

    def __repr__(self):
        return self.name

    def place_bet(self, bet):
        if bet > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.current_bet = bet
            self.balance -= bet
            return True

    def win(self, amount):
        self.balance += amount


class Hand:

    def __init__(self):
        self.cards = []

    def deal_card(self, card):
        self.cards.append(card)


def deal_new_round():
    # pop off cards, starting with first player, ending with dealer, one card to each x2 rounds
    pass


def available_moves():
    # If current_bet ≥ balance:
        # If immediately after deal
            can_double_down = True

        # If immediately after deal AND cards have equal values
            can_split = True


def hit():
    pass


def split():
    pass


def double_down():
    pass


def stay():
    pass


def play_round():

    deal_new_round()


def play_game():
    # Initiate new deck

    # Input: How many players?
    while True:
        try:
            num_players = int(input("How many players? "))
        except TypeError:
            print(f"Must be a number between 1 - {max_players}.")
        else:
            if num_players not in range(1, max_players + 1):
                print(f"Must be between 1 and {max_players} players.")
                continue
            else:
                break

    # Create Player object for each with Name, add to an array
    players = []
    for player in range(num_players):
        player_name = input(f"Enter name for Player {player + 1}: ")
        players.append(Player(player_name))

    # Create dealer object
    dealer = Dealer()

    # While Loop:
        # Play round ()
        # Check number of cards left in deck


deck = Deck()
print(deck)