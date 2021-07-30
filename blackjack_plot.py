import random
import numpy as np
import matplotlib.pyplot as plt


key = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K"
}

with open("", 'rb') as f:
    strat_matrix = np.load(f, allow_pickle=True)
print("Current Strategy Table: ")
print(strat_matrix)


def last_line(fname):
    with open(fname) as f:
        for line in f:
            pass
        last_line = line


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
        decision = strat_matrix[max(
            0, p_total - 4), (9 if d_up_card.val == 1 else min(d_up_card.val, 10) - 2)]
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
                # print(f"Total: {p.total}\n")
                if has_blackjack(p):
                    # print("Blackjack!")
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

        res = [(p, p.total) for p in players]

        # Finds max total
        max_total = max(list(zip(*res))[1])

        # Possible winners include players with total equal to max total
        poss_win = [p for p in res if p[1] == max_total]
        # print(poss_win)

        # If more than one player, reduce possible winners to only those with blackjack (if possible) - blackjack takes precedence
        # Line 173-174: If reducing poss_win does not result in an empty list, proceed with reduction
        if [p for p in poss_win if has_blackjack(p[0])]:
            poss_win = [p for p in poss_win if has_blackjack(p[0])]
        if len(poss_win) == 1:
            with open("", "a") as f:
                f.write(
                    f"{[[1 if poss_win[0][0] == p1 else 0], [1 if p1.busted else 0], player_totals, player_choice, dealer_upcard, dealer_totals, dealer_choice]}\n")
        elif len(poss_win) == 2:
            with open("", "a") as f:
                f.write(
                    f"{[[2], [1 if p1.busted else 0], player_totals, player_choice, dealer_upcard, dealer_totals, dealer_choice]}\n")

        for p in players:
            p.reset()

        player_totals = []
        player_choice = []
        dealer_upcard = []
        dealer_totals = []
        dealer_choice = []

    player_wins = 0
    dealer_wins = 0
    ties = 0
    num_sims = 0

    with open("", "r") as f:
        for line in f:
            if int(line[2]) == 1:
                player_wins += 1
            elif int(line[2]) == 0:
                dealer_wins += 1
            else:
                ties += 1
            num_sims += 1

    labels = 'MassR Wins', 'Dealer Wins', 'Ties'
    sizes = [player_wins, dealer_wins, ties]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')

    plt.show()


blackjack(1000000)
