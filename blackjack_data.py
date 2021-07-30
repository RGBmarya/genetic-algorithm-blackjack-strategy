import random
import numpy as np
import matplotlib.pyplot as plt


key = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K"
}


class Card:

    # Constructor
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
        self.face_up = True

    # Show value and suit of card
    def show(self):
        if self.face_up:
            if self.val == 1 or self.val > 10:
                # print(f"{key[self.val]} of {self.suit}")
                pass
            else:
                # print(f"{self.val} of {self.suit}")
                pass
        else:
            # print("? of ? (Card is face down)")
            pass


class Deck:

    # Constructor
    def __init__(self):
        self.cards = []

    # Fill deck with cards
    def fill(self):
        # Number of decks
        for i in range(4):
            for i in range(1, 14):
                for j in ["Clubs", "Diamonds", "Hearts", "Spades"]:
                    self.cards.append(Card(i, j))

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Print all cards remaining in deck
    def show(self):
        for card in self.cards:
            card.show()

    # Remove card from deck given value and suit
    def remove(self, val, suit):
        for index, card in enumerate(self.cards):
            if card.val == val and card.suit == suit:
                del self.cards[index]
                break

    # Deal card to player
    def deal(self):
        player_card = random.choice(self.cards)
        self.remove(player_card.val, player_card.suit)
        return player_card


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.total = 0
        self.busted = False

    # Player hits
    # Card is added to hand
    # Card value is added to total
    def hit(self, deck, totals_list, choice_list):
        p_card = deck.deal()
        self.hand.append(p_card)
        if p_card.val == 1:
            if self.total > 10:
                self.total += 1
            else:
                self.total += 11
        else:
            self.total += min(p_card.val, 10)
        totals_list.append(self.total)
        choice_list.append(1)

    # Player stands
    def stand(self, choice_list):
        choice_list.append(0)

    # Show player hand if not
    def show_hand(self):
        for card in self.hand:
            card.show()

    def choice(self, p_total, d_up_card):
        decision = random.randint(0, 1)
        if decision == 1:
            return "hit"
        return "stand"

    def reset(self):
        self.hand = []
        self.total = 0
        self.busted = False


def has_blackjack(player):
    return len(player.hand) == 2 and player.total == 21


def blackjack(n):
    match_info_table = []

    for i in range(n):
        p1 = Player("Player")
        dealer = Player("Dealer")
        players = [p1, dealer]

        player_totals = []
        player_choice = []
        dealer_upcard = []
        dealer_totals = []
        dealer_choice = []

        deck = Deck()
        deck.fill()
        deck.shuffle()

        for p in players:
            for i in range(2):
                if p != dealer:
                    p.hit(deck, player_totals, player_choice)
                else:
                    p.hit(deck, dealer_totals, dealer_choice)
            if p != dealer:
                player_totals.pop(0)
            else:
                dealer_upcard_val = dealer_totals.pop(0)
                dealer_upcard.append(dealer_upcard_val)
            (player_choice if p != dealer else dealer_choice).clear()
        dealer.hand[1].face_up = False
        dealer.show_hand()

        for p in players:
            if p == dealer:
                dealer.hand[1].face_up = True
                if p1.busted:
                    break
            while p.busted == False:
                p.show_hand()
                if has_blackjack(p):
                    break
                ans = p.choice(p.total, dealer.hand[0]) if p != dealer else (
                    "hit" if p.total < 17 else "stand")
                if ans.lower() == "hit":
                    p.hit(
                        deck, player_totals if p != dealer else dealer_totals,
                        player_choice if p != dealer else dealer_choice
                    )
                    if p.total == 21:
                        break
                    elif p.total > 21:
                        p.show_hand()
                        p.busted = True
                        p.total = -1
                        break
                elif ans.lower() == "stand":
                    p.stand(player_choice if p != dealer else dealer_choice)
                    break
                else:
                    continue

        # list of (player, total) tuples for each player
        res = [(p, p.total) for p in players]

        # Finds max total
        max_total = max(list(zip(*res))[1])

        # Possible winners include players with total equal to max total
        poss_win = [p for p in res if p[1] == max_total]

        # If more than one player, reduce possible winners to only those with blackjack (if possible) - blackjack takes precedence
        # Line 173-174: If reducing poss_win does not result in an empty list, proceed with reduction
        if [p for p in poss_win if has_blackjack(p[0])]:
            poss_win = [p for p in poss_win if has_blackjack(p[0])]
        if len(poss_win) == 1:
            for i in range(len(player_choice)):
                match_info = [
                    1 if poss_win[0][0] == p1 else 0,
                    1 if p1.busted else 0,
                    player_totals[i],
                    player_choice[i],
                    dealer_upcard[0]
                ]

                # Sometimes appending empty list
                match_info_table.append(match_info)

        for p in players:
            p.reset()

        player_totals = []
        player_choice = []
        dealer_upcard = []
        dealer_totals = []
        dealer_choice = []

    return match_info_table


path = r"G:\Users\Mihir Gaming PC\Documents\programming\python\blackjack\bj_results.npy"

np.save(path, blackjack(10000000))
print("done")
