import os
import random
import time


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.display = f"{rank} of {suit}"
        self.dictHand = {
            "rank": rank,
            "suit": suit[0].lower(),
        }

    def __repr__(self):
        return self.display


class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "Jack", "Queen", "King", "Ace"]

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, numCards):
        dealtCards = self.cards[:numCards]
        self.cards = self.cards[numCards:]
        return dealtCards


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bid = None

    def clearHand(self):
        self.hand = []

    def addCard(self, card):
        self.hand.append(card)

    def playCard(self, cardIndex):
        return self.hand.pop(cardIndex)

    def showHand(self):
        return [str(card) for card in self.hand]

    def organizeHand(self):
        suitOrder = {"Hearts": 0, "Spades": 1, "Diamonds": 2, "Clubs": 3}
        self.hand = sorted(
            self.hand,
            key=lambda card: (
                suitOrder[card.suit],
                -self._cardSortKey(card),
            ),
        )

    def _cardSortKey(self, card):
        rankOrder = {
            "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
            "7": 6, "8": 7, "9": 8, "10": 9,
            "Jack": 10, "Queen": 11, "King": 12, "Ace": 13,
        }

        return rankOrder[card.rank]

    def setBid(self, bid):
        if bid:
            self.bid = int(bid)
        else:
            self.bid = None


class TarneebGame:
    def __init__(self, playerNames):
        self.deck = Deck()
        self.deck.shuffle()

        self.round = 0
        self.firstPlayedSuit = None
        self.trump = None
        self.prevWinner = None

        self.scores = [0, 0]
        self.curScores = [0, 0]
        self.playedCards = []

        self.highestBid = {"bid": None, "player": ""}
        self.players = [Player(name) for name in playerNames]

    def cleanHands(self):
        for player in self.players:
            player.clearHand()

    def dealDeck(self):
        self.cleanHands()
        for _ in range(13):
            for player in self.players:
                if not self.deck.cards:
                    self.deck = Deck()
                    self.deck.shuffle()

                player.addCard(self.deck.deal(1)[0])

        for player in self.players:
            player.organizeHand()

    def displayHands(self):
        for player in self.players:
            print(f"{player.name}'s hand: {', '.join(player.showHand())}\n")

    def getBid(self, player):
        highestBid = self.highestBid["bid"] or 7
        name = player.name

        while True:
            try:
                bid = input(f"{name}, enter your bid ({highestBid}-13): ")
                if bid == "":
                    return None
                elif 7 <= int(bid) <= 13:
                    return bid
                else:
                    print("Invalid bid. Please enter between 7 and 13.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def getBids(self):
        for player in self.players:
            while True:
                bid = self.getBid(player)
                highestBid = self.highestBid["bid"]
                if bid:
                    bid = int(bid)
                else:
                    bid = None

                if highestBid and bid and highestBid >= bid:
                    print("Invalid bid. Please enter a higher bid.")
                else:
                    if bid and (not highestBid or bid > highestBid):
                        self.highestBid["bid"] = bid
                        self.highestBid["player"] = player.name
                    break

            player.setBid(bid)
            if not bid:
                print(f"{player.name} passes")
            else:
                print(f"{player.name} bids {bid}")

        if not self.highestBid["bid"]:
            os.system("clear")
            print("No one bid; restarting round.\n")

            self.dealDeck()
            self.playRound()

        print(f"\n{self.highestBid['player']} won the bid.\n")
        self.trump = input("Enter trump suit (h, s, d, c): ")
        print()

        while self.trump not in ["h", "s", "d", "c"]:
            print(
                "Invalid suit. Please enter",
                "h (hearts), s (spades), d (diamonds), or c (clubs).",
            )
            self.trump = input("Enter trump suit (h, s, d, c): ")
            print()

    def playRound(self):
        print(f"Round {self.round} started.\n")
        self.displayHands()

        if self.round == 1:
            self.getBids()

        # Determine the order of players based on the bid winner
        if self.round == 1:
            startIndex = self.players.index(
                next(
                    player
                    for player in self.players
                    if player.name == self.highestBid["player"]
                )
            )
        else:
            startIndex = 0
            if self.prevWinner:
                winner = self.prevWinner
                startIndex = self.players.index(winner)

        self.players = self.players[startIndex:] + self.players[:startIndex]

        os.system("clear")
        print(
            f"Round {self.round} started",
            f"(trump: {self.trump}) ({'-'.join(map(str, self.curScores))}).\n"
        )
        self.getCards()

    def getCards(self):
        for i, player in enumerate(self.players):
            name = player.name
            print(f"{name}'s hand: {', '.join(player.showHand())}")

            while True:
                cardIndex = input(
                    f"{name}, enter the index of the card you want to play: "
                )

                try:
                    cardIndex = int(cardIndex)
                    if 0 <= cardIndex < len(player.hand):
                        card = player.hand[cardIndex]
                        if i == 0:
                            if card.suit == self.trump:
                                self.firstPlayedSuit = self.trump
                            else:
                                self.firstPlayedSuit = card.suit
                        break
                    else:
                        print("Invalid index. Please enter a valid index.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            player.playCard(cardIndex)
            self.playedCards.append({
                "card": card,
                "player": player,
            })
            print(f"{player.name} played {card}")
            print()

        self.prevWinner = self.determineWinner()

        self.playedCards = []

    def _cardSortKey(self, card):
        rankOrder = {
            "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
            "7": 6, "8": 7, "9": 8, "10": 9,
            "Jack": 10, "Queen": 11, "King": 12, "Ace": 13,
        }

        return rankOrder[card.rank]

    def _suitSortKey(self, suit):
        suitOrder = {"Hearts": 0, "Spades": 1, "Diamonds": 2, "Clubs": 3}
        return suitOrder[suit]

    def determineWinner(self):
        trumpCards = [
            card for card in self.playedCards if card["card"].suit[0].lower() == self.trump
        ]

        if trumpCards:
            winningTrump = max(
                trumpCards, key=lambda card: self._cardSortKey(card["card"])
            )
            winningPlayer = winningTrump["player"]
            winningCard = winningTrump["card"]
        else:
            sortedCards = sorted(
                self.playedCards,
                key=lambda card: (
                    -self._cardSortKey(card["card"]),
                    self._suitSortKey(card["card"].suit),
                ),
            )
            winningPlayer = sortedCards[0]["player"]
            winningCard = sortedCards[0]["card"]

        print(f"{winningPlayer.name} wins the round with {winningCard}!")

        if winningPlayer.name in ["Player 1", "Player 3"]:
            self.curScores[0] += 1
        else:
            self.curScores[1] += 1

        self.playedCards = []

        return winningPlayer

    def playGame(self):
        while max(self.scores) < 60:
            self.dealDeck()

            for _ in range(13):
                self.round += 1
                self.playRound()

                time.sleep(3)
                os.system("clear")

                self.highestBid = {"bid": None, "player": ""}

            n = 0
            N = 1
            if self.highestBid["player"] in ["Player 1", "Player 3"]:
                n = 0
                N = 1
            else:
                n = 1
                N = 0

            if self.curScores[n] >= self.highestBid["bid"]:
                self.scores[n] += self.curScores[n]
            else:
                self.scores[n] -= self.highestBid["bid"]
                self.scores[N] += self.curScores[N]

            self.round = 0
            self.curScores = [0, 0]


if __name__ == "__main__":
    playerNames = ["Player 1", "Player 2", "Player 3", "Player 4"]
    game = TarneebGame(playerNames)
    game.playGame()
