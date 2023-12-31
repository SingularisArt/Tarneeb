import os
import random
import time


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.display = f"{rank}{suit.upper()}"
        self.dictHand = {
            "rank": rank,
            "suit": suit[0].lower(),
        }

    def __repr__(self):
        return self.display


class Deck:
    def __init__(self):
        suits = ["h", "d", "c", "s"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "J", "Q", "K", "A"]

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
        suitOrder = {"h": 0, "s": 1, "d": 2, "c": 3}
        self.hand = sorted(
            self.hand,
            key=lambda card: (
                suitOrder[card.suit],
                -self._cardSortKey(card),
            ),
        )

    def _cardSortKey(self, card):
        rankOrder = {
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            "10": 9,
            "J": 10,
            "Q": 11,
            "K": 12,
            "A": 13,
        }

        return rankOrder[card.rank]

    def _suitSortKey(self, suit):
        suitOrder = {
            "Hearts": 0,
            "Spades": 1,
            "Diamonds": 2,
            "Clubs": 3,
        }

        return suitOrder[suit]

    def setBid(self, bid):
        if bid:
            self.bid = int(bid)
        else:
            self.bid = None


class TarneebGame:
    def __init__(self, playerNames):
        self.playerNames = playerNames
        self.scores = [0, 0]
        self.isOver = False
        self._resetValues()

    def _getCardValue(self, card):
        suit = card.suit

        value = self._cardSortKey(card)

        if suit == self.trump:
            return 2 * value
        elif suit == self.firstPlayedSuit:
            return value
        else:
            return 0

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

        curScoresSplit = ' - '.join(map(str, self.curScores))
        totalScoresSplit = ' - '.join(map(str, self.scores))

        print(
            f"Round {self.round} started",
            f"(trump suit: {self.trump})",
            f"(current round scores: {curScoresSplit})",
            f"(total game scores: {totalScoresSplit}).\n"
        )

        self.getCards()

    def getCardsFromPlayer(self, i, player):
        cardIndex = None
        allSuitsInPlayersHand = set([card.suit for card in player.hand])

        while True:
            string = (
                f"{player.name}, enter the index",
                "of the card you want to play: "
            )
            cardIndex = input(string)

            try:
                cardIndex = int(cardIndex)
                card = player.hand[cardIndex]
                self._getCardValue(card)
                if i == 0:
                    self.firstPlayedSuit = card.suit
                    break

                if self.firstPlayedSuit in allSuitsInPlayersHand:
                    if card.suit == self.firstPlayedSuit:
                        break
                    else:
                        print(
                            "Invalid input: You must play the same suit as",
                            f"the first card played ({self.firstPlayedSuit})."
                        )
                else:
                    break
            except ValueError:
                print("Invalid input: Please enter a valid number.")

        return cardIndex, card

    def getCards(self):
        for i, player in enumerate(self.players):
            name = player.name
            print(f"{name}'s hand: {', '.join(player.showHand())}")

            cardIndex, card = self.getCardsFromPlayer(i, player)

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
            "J": 10, "Q": 11, "K": 12, "A": 13,
        }

        return rankOrder[card.rank]

    def determineWinner(self):
        cardValues = [
            int(self._getCardValue(card["card"])) for card in self.playedCards
        ]

        winningCard = max(cardValues)
        winningCardIndex = cardValues.index(winningCard)
        winningCardDisplay = self.playedCards[winningCardIndex]["card"]
        winningPlayer = self.playedCards[winningCardIndex]["player"]

        print(
            f"{winningPlayer.name} wins",
            f"the round with {winningCardDisplay}!"
        )

        if winningPlayer.name in ["Player 1", "Player 3"]:
            self.curScores[0] += 1
        else:
            self.curScores[1] += 1

        self.playedCards = []

        return winningPlayer

    def playGame(self):
        while max(self.scores) < 60:
            self._resetValues()
            self.dealDeck()

            for _ in range(13):
                self.round += 1
                self.playRound()

                time.sleep(2)
                os.system("clear")

            n = 0
            N = 1
            if self.highestBid["player"] not in ["Player 1", "Player 3"]:
                n = 1
                N = 0

            if self.curScores[n] >= self.highestBid["bid"]:
                self.scores[n] += self.curScores[n]
            else:
                self.scores[n] -= self.highestBid["bid"]
                self.scores[N] += self.curScores[N]

        self.printWinners()
        self.isOver = True

    def _resetValues(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.round = 0
        self.firstPlayedSuit = None
        self.trump = None
        self.prevWinner = None

        self.curScores = [0, 0]
        self.playedCards = []

        self.highestBid = {"bid": None, "player": ""}
        self.players = [Player(name) for name in self.playerNames]

    def printWinners(self):
        if self.scores[0] > self.scores[1]:
            print(
                f"Team 1 won with a score of {self.scores[0]}",
                f"and Team 2 had a score of {self.scores[1]}!"
            )
        elif self.scores[1] > self.scores[0]:
            print(
                f"Team 2 won with a score of {self.scores[1]}",
                f"and Team 1 had a score of {self.scores[0]}!"
            )


if __name__ == "__main__":
    playerNames = ["Player 1", "Player 2", "Player 3", "Player 4"]
    game = TarneebGame(playerNames)
    game.playGame()
