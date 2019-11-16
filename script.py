"""
Blackjack Game
"""
import random
from math import ceil
import time

card_values_dict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                    "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
card_colors_dict = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}
max_players = 4
max_decks = 8


class Deck:
    """"""
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
    """"""
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.value = card_values_dict[name]
        self.color = card_colors_dict[suit]

    def __repr__(self):
        return self.name + self.suit


class Dealer:
    """"""
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
    """"""
    def __init__(self, name):
        self.name = name
        self.balance = 100
        self.current_bet = 0
        self.active_hands = []
        # NOTE: bet_per_hand = self.current_bet / len(self.active_hands)
        self.insurance_bet = 0  # May be up to half self.current_bet

    def __repr__(self):
        return self.name

    def place_bet(self, bet):
        if bet > self.balance:
            print(f"Insufficient funds to bet {bet}.\nCurrent Balance: {self.balance}")
            return False
        elif bet <= 0 or bet % 2 != 0:
            print("Must be a positive even wager.")
        else:
            self.current_bet += bet
            return True

    def credit(self, amount):  # NOTE: bet_per_hand = self.current_bet / len(self.active_hands)
        """
        :param amount: (self.current_bet / len(self.active_hands)) * Odds
        :return: None
        """
        self.balance += amount

    def debit(self, amount):  # NOTE: bet_per_hand = self.current_bet / len(self.active_hands)
        """
        :param amount: self.current_bet / len(self.active_hands
        :return: None
        """
        self.balance -= amount

    def reset_hand(self):
        self.current_bet = 0
        self.insurance_bet = 0

        # Delete active Hand(s) object(s)
        for hand in self.active_hands:
            del hand

        # Clear active_hand array
        self.active_hands.clear()


class Hand:
    """"""
    def __init__(self):
        self.cards = []
        self.busted = False

    def __repr__(self):
        out_string = ""
        for card in self.cards:
            out_string += f"[{card.name}{card.suit}]"
        return out_string

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

    def soft_17(self):
        value_sum = 0
        aces = 0
        for card in self.cards:
            value_sum += card.value
            if card.value == 11:
                aces += 1
        while value_sum > 17 and aces > 1:
            value_sum -= 10
            aces -= 1
        return value_sum == 17 and aces == 1

    def deal_card(self, card):
        self.cards.append(card)


def welcome():
    """"""
    welcome_string = "WELCOME TO BLACKJACK!! (CASINO RULE EDITION)"
    print("\n" + "#" * len(welcome_string))
    print(f"{welcome_string}")
    print("#" * len(welcome_string) + "\n")
    print(" - Get 21 points on the player's first two cards (called a 'blackjack', without a dealer blackjack")
    print(" - Reach a final score higher than the dealer without exceeding 21")
    print(" - Let the dealer draw additional cards until their hand exceeds 21 ('busted')\n")


def deal_new_round(players, dealer, deck):
    """"""
    # Initiate new hand for each player and dealer
    for player in players:
        player.active_hands.append(Hand())
    dealer.active_hand.append(Hand())

    # Deal 2 cards to each player and dealer
    for _ in range(2):
        for player in players:
            player.active_hands[0].deal_card(deck.cards.pop())
        dealer.active_hand[0].deal_card(deck.cards.pop())


def end_round(players, dealer):
    """"""
    dealer.reset_hand()
    for player in players:
        player.reset_hand()


def available_plays(hand, player):  # !! hand parameter part of player object
    """
    :param hand: Current hand
    :param player: Current player
    :return: Boolean tuple: (can_double_down, can_split)
    """

    # Able to double bet?
    bet_per_hand = player.current_bet / len(player.active_hands)
    if bet_per_hand * 2 <= player.balance and len(hand) == 2:
        # Able to split?
        if hand.cards[0].value == hand.cards[1].value:
            return True, True, " / [D]ouble-down / Sp[l]it"
        return True, False, " / [D]ouble-down"
    return False, False, ""


def hit(deck, current_hand):
    """"""
    current_hand.deal_card(deck.cards.pop())
    return current_hand


def split(deck, hand_to_split, hands_to_play, player):
    """"""
    idx_active = player.active_hands.index(hand_to_split)
    idx_to_play = hands_to_play.index(hand_to_split)
    card_to_split_off = hand_to_split.cards.pop(1)
    player.active_hands.insert(idx_active + 1, Hand())
    player.active_hands[idx_active + 1].deal_card(card_to_split_off)
    player.active_hands[idx_active].deal_card(deck.cards.pop())
    player.active_hands[idx_active + 1].deal_card(deck.cards.pop())
    hands_to_play.insert(idx_to_play + 1, Hand())
    hands_to_play[idx_to_play:idx_to_play + 2] = player.active_hands[idx_active:idx_active + 2]
    print(f"{player.name}: {player.active_hands[idx_active]}  {player.active_hands[idx_active + 1]}")
    return hands_to_play


def display_game_state(players, dealer, players_done=False):
    """"""
    # Print Dealer
    dealer_string = "Dealer: "
    if players_done:
        for card in dealer.active_hand[0].cards:
            dealer_string += f"[{card.name}{card.suit}]"
    else:
        dealer_string += f"[{dealer.active_hand[0].cards[1].name}{dealer.active_hand[0].cards[1].suit}]"
    print(f"\n{dealer_string}\n")

    # Print Players
    for player in players:
        player_string = f"{player.name}\n"
        for hand in player.active_hands:
            for card in hand.cards:
                player_string += f"[{card.name}{card.suit}]"
            player_string += "\n"
        print(f"{player_string}")


def balance_status(players):
    print("")
    for player in players:
        print(f"{player.name:17.15}{int(player.balance):6d}")
    print("")


def deck_check(deck, num_decks):
    if len(deck) < (num_decks * 10):
        # If low, delete old deck and initiate new deck
        del deck
        return Deck(num_decks)
    else:
        return deck


def game_over(players):
    print("GAME OVER!\nThe final balances are:\n")
    balance_status(players)


def play_round(players, deck, all_players):
    # Initiate dealer object
    dealer = Dealer()

    # Input: Place your bets!
    for player in players:
        print(f"{player.name:17.15}{int(player.balance):6d}")
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

    # Check if dealer showing Ace:
    if dealer.active_hand[0].cards[1].value == 11:
        # Offer insurance bet:
        print("Insurance? Type [y]es or press enter to pass...")
        for player in players:
            if input(f"{player.name}: ").lower() in ("y", "yes"):
                if player.current_bet * 1.5 <= player.balance:
                    player.insurance_bet = player.current_bet // 2
                    print("Insurance bet placed.")
                else:
                    print("Sorry, not enough funds.")

    # Now, check if Dealer hit Blackjack
    if dealer.active_hand[0].total() == 21:
        print(f"Dealer has Blackjack!  {dealer.active_hand[0]}")
        # Payout insurance and end round
        while len(players) > 0:
            players[0].credit(players[0].insurance_bet * 2)
            players[0].insurance_bet = 0
            if players[0].active_hands[0].total() == 21:
                # Player pushes
                print(f"{players[0].name} pushes!")
            else:
                # Player loses
                print(f"{players[0].name} loses {players[0].current_bet}")
                players[0].debit(players[0].current_bet)
            players[0].current_bet = 0
            players.pop(0)
    else:
        if dealer.active_hand[0].cards[1].value == 11:
            print("Dealer does not have Blackjack, insurance bets collected.")
        # Collect insurance
        for player in players:
            player.debit(player.insurance_bet)
            player.insurance_bet = 0

    # Now check if any player hit Blackjack!
    player_idx = 0
    while player_idx < len(players):
        if players[player_idx].active_hands[0].total() == 21:
            print(f"{players[player_idx].name} hit Blackjack!")
            reward = int(ceil(players[player_idx].current_bet * 1.5))
            print(f"Rewarded {reward}\n")
            players[player_idx].credit(reward)
            # If Blackjack off of deal, remove player from round
            players.pop(player_idx)
            del reward
        else:
            player_idx += 1

    # Time for Players to hit/stay/double/split/bust
    while len(players) > 0:
        current_player = players[0]
        # Create array of player hands that still need to be played through
        # Does not affect Player.active_hands, so they can be popped off: hands_to_play.pop(0)
        hands_to_play = current_player.active_hands[:]
        while len(hands_to_play) > 0:
            # Focused on a single hand:
            current_hand = hands_to_play[0]
            stay = False
            # while not (busted, 21 or stay)
            while current_hand.total() < 21 and not stay:
                can_double_down, can_split, str_append = available_plays(current_hand, current_player)
                # Display active user / hand:
                print(f"{current_player.name}: {current_hand}")
                # Prompt user for action
                while True:
                    move_selection = input(f"[H]it / [S]tay{str_append}: ").lower()
                    if move_selection in ("h", "hit"):  # HIT!
                        hit(deck, current_hand)
                        print(f"{current_player.name}: {current_hand}")
                        break
                    elif move_selection in ("s", "stay"):  # STAY!
                        stay = True
                        break
                    elif move_selection in ("d", "double", "double-down") and can_double_down:  # DOUBLE-DOWN!
                        # Adjust current bet (double the bet on given hand)
                        current_player.current_bet += (current_player.current_bet / len(current_player.active_hands))
                        hit(deck, current_hand)
                        print(f"{current_player.name}: {current_hand}")
                        stay = True
                        break
                    elif move_selection in ("l", "split") and can_split:  # SPLIT!
                        # Adjust current bet (double the bet on given hand)
                        current_player.current_bet += (current_player.current_bet / len(current_player.active_hands))
                        hands_to_play = split(deck, current_hand, hands_to_play, current_player)
                        break
                    else:
                        continue
                # Calculate ask_again/21/bust?
                if current_hand.total() == 21:
                    stay = True
                elif current_hand.total() > 21:
                    # Bust!
                    print("Bust!")
                    current_player.current_bet -= current_player.current_bet / len(current_player.active_hands)
                    current_player.debit(current_player.current_bet / len(current_player.active_hands))
                    bust_index = current_player.active_hands.index(current_hand)
                    current_player.active_hands.pop(bust_index)
                    pass
                else:
                    # 21!
                    print("21!")
                    # Don't ask again, but must compare to dealer for win vs push
                    pass
            hands_to_play.pop(0)
        players.pop(0)

    # Dealer's turn (automated)
    print(f"Dealer: {dealer.active_hand[0]}")
    dealer_bust = False
    while True:
        if dealer.active_hand[0].total() > 21:
            # Dealer Busts!
            dealer_bust = True
            break
        if dealer.active_hand[0].total() < 17 or dealer.active_hand[0].soft_17():
            # Dealer Hits
            hit(deck, dealer.active_hand[0])
            time.sleep(2)
            print(f"Dealer: {dealer.active_hand[0]}")
        else:
            # Dealer Stays
            break

    # If dealer busted, reward all active hands
    if dealer_bust:
        for player in players:
            player.credit(player.current_bet)
    else:
        # Compare dealer hand to active player hands
        for player in all_players:
            for hand in player.active_hands:
                if hand.total() > dealer.active_hand[0].total():
                    # Player hand wins
                    player.credit(player.current_bet / len(player.active_hands))
                elif hand.total() < dealer.active_hand[0].total():
                    # Player hand loses
                    player.debit(player.current_bet / len(player.active_hands))

    # End of round clean-up
    end_round(all_players, dealer)
    del dealer


def play_game():

    # Introduction
    welcome()

    # Input: How many decks?
    while True:
        try:
            num_decks = int(input("How many decks would you like to play with? "))
            if num_decks not in range(1, max_decks + 1):
                print(f"Must be between 1 and {max_decks} decks.")
                continue
            else:
                break
        except:  # TypeError:
            print(f"Must be a number between 1 - {max_decks}.")

    # Input: How many players?
    while True:
        try:
            num_players = int(input("How many players? "))
        except:  # TypeError:
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
    all_players = []
    for player in range(num_players):
        # Input: Player name?
        player_name = input(f"Enter name for Player {player + 1}: ")
        # Append go players list
        all_players.append(Player(player_name))

    # Stall before starting game play
    input("\nLet's play some Blackjack!! Press enter when ready...")
    balance_status(all_players)

    game_on = True
    while game_on:
        # Determine participating players (Must have positive balance)
        players_for_round = [player for player in all_players if player.balance >= 2]

        # End game if no players remain
        if len(players_for_round) == 0:
            break

        # Execute a round of Blackjack
        play_round(players_for_round, deck, all_players)

        # Display updated balance status
        balance_status(all_players)

        # Check if deck low and in need of shuffling
        deck = deck_check(deck, num_decks)

        # Play another round?
        game_on = input("Press enter to play again, or type 'end' to finish: ").lower() != 'end'

    # Display end-of-game balances
    game_over(all_players)


play_game()

# TODO: During game play, edit how/when cards are displayed

# TODO: Double-down bet DIFFERENT than others... if that hand won, must reward double
#   i.e.    [9][9]              -- current_bet = 10, len() = 1, bet/hand = 10
#   Split:  [9][2]      [9][K]  -- current_bet = 20, len() = 2, bet/hand = 10
#   Double: [9][2][Q]   [9][K]  -- current_bet = 30, len() = 2, bet/hand = 15 !!!!
#   _
#   Dealer: [J][10]             -- Payout would be:     15
#                               -- Payout SHOULD be:    20
