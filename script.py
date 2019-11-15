"""
Blackjack Game
"""
import random

card_values_dict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                    "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
card_colors_dict = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}
max_players = 4
max_decks = 10


class Deck:

    def __init__(self, deck_count=6):
        self.deck_count = deck_count  # Must be ≥1
        self.cards = []
        for _ in range(self.deck_count):
            for suit in card_colors_dict.keys():
                for name in card_values_dict.keys():
                    self.cards.append(Card(name, suit))
        for _ in range(6):
            random.shuffle(self.cards)

    def __repr__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)


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
        self.active_hands = []

    def __repr__(self):
        return self.name

    def place_bet(self, bet):
        if bet > self.balance:
            print(f"Insufficient funds.\nCurrent Balance: {self.balance}")
            return False
        elif bet <= 0:
            print("Must be a positive wager.")
        else:
            self.current_bet = bet
            self.balance -= bet
            return True

    def win(self, amount):
        self.balance += amount

    def reset_hand(self):
        # Delete active Hand(s) object(s)
        for hand in self.active_hands:
            del hand

        # Clear active_hand array
        self.active_hands.clear()


class Hand:

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def total(self):
        value_sum = 0
        aces = 0
        for card in self.cards:
            value_sum += card.value
            if card.value == 11:
                aces += 1
        while value_sum > 21 and aces > 0:
            value_sum -= 10
            aces -= 1
        return value_sum

    def deal_card(self, card):
        self.cards.append(card)


def deal_new_round(players, dealer, deck):
    # Initiate new hand for each player and dealer
    for player in players:
        player.active_hands.append(Hand())
    dealer.active_hand.append(Hand())

    # Deal 2 cards to each player and dealer
    for _ in range(2):
        for player in players:
            player.active_hands[0].deal_card(deck.cards.pop())
        dealer.active_hand[0].deal_card(deck.cards.pop())


def end_round(players):
    for player in players:
        player.current_bet = 0
        for hand in player.active_hands:
            del hand
        player.active_hands.clear()



def bust_or_21(hand, player):

    return did_bust, did_win


def available_plays(hand, player):  # !! hand parameter part of player object
    """
    :param hand:
    :param player:
    :return: Boolean tuple: (can_double_down, can_split)
    """

    # Able to double bet?
    if player.current_bet <= player.balance and len(hand) == 2:
        # Able to split?
        if hand.cards[0].value == hand.cards[1].value:
            return True, True
        return True, False
    return False, False


def hit():
    pass


def split():
    pass


def double_down():
    pass


def stay():
    pass


def display_game_state(players, dealer, players_done=False):
    dealer_string = "Dealer: "
    if players_done:
        for card in dealer.active_hand[0].cards:
            dealer_string += f"[{card.name}{card.suit}]"
    else:
        dealer_string += f"[{dealer.active_hand[0].cards[1].name}{dealer.active_hand[0].cards[1].suit}]"
    print(f"\n{dealer_string}\n")

    for player in players:
        player_string = f"{player.name}\n"
        for hand in player.active_hands:
            for card in hand.cards:
                player_string += f"[{card.name}{card.suit}]"
            player_string += "\n"
        print(f"\n{player_string}\n")


def play_round(players, deck):
    # Initiate dealer object
    dealer = Dealer()

    # Input: Place your bets!
    for player in players:
        print(f"{player.name}'s balance:   {player.balance}")
        while True:
            try:
                player_bet = int(input("What is your bet? "))
                if player.place_bet(player_bet):
                    break
            except:
                print(f"Must be an integer between 1 - {player.balance}.")

    # All bets are placed, time to deal!
    deal_new_round(players, dealer, deck)
    display_game_state(players, dealer)

    # Delete dealer object
    del dealer


def balance_status(players):
    print("\n")
    for player in players:
        print(f"{player.name:17.15}{player.balance:6d}")
    print("\n")


def deck_check(deck, num_decks):
    if len(deck) < (num_decks * 10):
        # If low, delete old deck and initiate new deck
        del deck
        return Deck(num_decks)
    else:
        return deck


def play_game():

    # Input: How many decks?
    while True:
        try:
            num_decks = int(input("How many decks would you like to play with? "))
            if num_decks not in range(1, max_decks + 1):
                print(f"Must be between 1 and {max_decks} decks.")
                continue
            else:
                break
        except TypeError:
            print(f"Must be a number between 1 - {max_decks}.")

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

    # Initiate new Deck object
    deck = Deck(num_decks)

    # Create Player object for each
    players = []
    for player in range(num_players):
        # Input: Player name?
        player_name = input(f"Enter name for Player {player + 1}: ")
        # Append go players list
        players.append(Player(player_name))

    # Stall before starting gameplay
    input("\nLet's play some Blackjack!! Press enter when ready... \n")
    balance_status(players)

    game_on = True
    while game_on:
        # Execute a round of Blackjack
        play_round(players, deck)

        # Check if deck low and in need of shuffling
        deck = deck_check(deck, num_decks)

        # Play another round?
        game_on = input("Press enter to play again, or type 'end' to finish: ").lower() != 'end'

    balance_status(players)


play_game()