"""
Author: Hashem A. Damrah
Copyright: Hashem A. Damrah, 2024
Description: This file contains the Tarneeb game model.
"""

import os
import random
import time

import numpy as np
from gymnasium import Env
from gymnasium.spaces import Box, Discrete


class Card:
    """
    This class represents a card in a deck of cards.

    Attributes:
        suit: The suit of the card (h, d, c, s).
        rank: The rank of the card (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A).
        display: The display of the card (rank + suit).
    """

    def __init__(self, suit, rank):
        """
        The constructor for the Card class.

        Args:
            suit (str): The suit of the card (h, d, c, s).
            rank (str): The rank of the card
                (2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A).
        """

        self.suit = suit
        self.rank = rank
        self.display = f"{rank}{suit.upper()}"

    def __repr__(self):
        """
        The representation of the Card class.

        Returns:
            str: The display of the card (rank + suit).
        """

        return self.display


class Deck:
    """
    This class represents a deck of cards.

    Attributes:
        cards: The cards in the deck.
    """

    def __init__(self):
        """ The constructor for the Deck class. """

        suits = ["h", "d", "c", "s"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "J", "Q", "K", "A"]

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        """ Shuffles the deck of cards. """

        random.shuffle(self.cards)

    def deal(self, numCards):
        """
        Deals a number of cards from the deck.

        Args:
            numCards (int): The number of cards to deal.

        Returns:
            list: The dealt cards.
        """

        dealtCards = self.cards[:numCards]
        self.cards = self.cards[numCards:]

        return dealtCards


class Player:
    """
    This class represents a player in the game.

    Attributes:
        name: The name of the player.
        hand: The cards in the player's hand.
        bid: The bid of the player.
    """

    def __init__(self, name):
        """
        The constructor for the Player class.

        Args:
            name (str): The name of the player.
        """

        self.name = name
        self.hand = []
        self.bid = None

    def clearHand(self):
        """ Clears the player's hand. """

        self.hand = []

    def addCard(self, card):
        """
        Adds a card to the player's hand.

        Args:
            card (Card): The card to add to the player's hand.
        """

        self.hand.append(card)

    def playCard(self, cardIndex):
        """
        Plays a card from the player's hand.

        Args:
            cardIndex (int): The index of the card to play.

        Returns:
            Card: The card played from the player's hand.
        """

        return self.hand.pop(cardIndex)

    def showHand(self):
        """
        Shows the player's hand.

        Returns:
            list: The cards in the player's hand.
        """

        return [str(card) for card in self.hand]

    def organizeHand(self):
        """ Organizes the player's hand by suit and rank. """

        suitOrder = {"h": 0, "s": 1, "d": 2, "c": 3}
        self.hand = sorted(
            self.hand,
            key=lambda card: (
                suitOrder[card.suit],
                -self._cardSortKey(card),
            ),
        )

    def _cardSortKey(self, card):
        """
        Sorts the cards in the player's hand by rank.

        Args:
            card (Card): The card to sort.

        Returns:
            int: The rank of the card.
        """

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
        """
        Sorts the cards in the player's hand by suit.

        Args:
            suit (str): The suit of the card.

        Returns:
            int: The suit of the card.
        """

        suitOrder = {
            "Hearts": 0,
            "Spades": 1,
            "Diamonds": 2,
            "Clubs": 3,
        }

        return suitOrder[suit]

    def setBid(self, bid):
        """
        Sets the bid of the player.

        Args:
            bid (int): The bid of the player.
        """

        if bid:
            self.bid = int(bid)
        else:
            self.bid = None


class TarneebGame(Env):
    """
    This class represents the Tarneeb game.
    It inherits from the Env class in the gymnasium package.

    Attributes:
        action_space: The action space of the game. (Relate to GYM)
        observation_space: The observation space of the game. (Relate to GYM)
        playerNames: The names of the players in the game.
        scores: The scores of the players in the game.
        curScores: The scores of the current round.
        isOver: Whether the game is over.
        trump: The trump suit of the game.
        players: The players in the game.
        prevWinner: The previous winner of the game.
        playedCards: The cards played in the trick.
        deck: The deck of cards in the game.
        round: The current round.
        firstPlayedSuit: The suit of the first card played in the trick.
        highestBid: The highest bid of the current round.
    """

    def __init__(self, playerNames):
        """
        The constructor for the TarneebGame class.

        Args:
            playerNames (list): The names of the players in the game.
        """

        self.playerNames = playerNames
        self.scores = [0, 0]
        self.isOver = False
        self.action_space = Discrete(13 + 8)  # 13 cards + 8 bids
        self.observation_space = Box(
            low=np.array([0]),
            high=np.array([100]),
        )

        self._resetValues()

    def step(self, action):
        """
        Steps through the game for the gymnasium package.

        Args:
            action (int): The action to take.
        """

        pass

    def reset(self):
        """ Reset the game for a new episode. """

        pass

    def render(self):
        """ Render the game. """

        pass

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

    def _cardSortKey(self, card):
        """
        Sorts the cards in the player's hand by rank.

        Args:
            card (Card): The card to sort.

        Returns:
            int: The rank of the card.
        """

        rankOrder = {
            "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
            "7": 6, "8": 7, "9": 8, "10": 9,
            "J": 10, "Q": 11, "K": 12, "A": 13,
        }

        return rankOrder[card.rank]

    def _getCardValue(self, card):
        """
        Gets the value of a card. The value is calculated based on two things:
            1. If the suit is a trump card, the rank is doubled.
                i.e., Ace of trumps suit = 2 * 14 = 28.
            2. If the suit is the same as the first card played,
                the rank is not doubled.
                i.e., Ace of first suit = 14.
            3. If the suit is not the same as the first card played,
                the value is always 0.

        Args:
            card (Card): The card to get the value of.

        Returns:
            int: The value of the card.
        """

        suit = card.suit

        value = self._cardSortKey(card)

        if suit == self.trump:
            return 2 * value
        elif suit == self.firstPlayedSuit:
            return value
        else:
            return 0

    def cleanHands(self):
        """ Cleans the players' hands. """

        for player in self.players:
            player.clearHand()

    def dealDeck(self):
        """ Deals the deck of cards to the players. """

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
        """ Displays the players' hands. """

        for player in self.players:
            print(f"{player.name}'s hand: {', '.join(player.showHand())}\n")

    def getBid(self, player):
        """
        Gets the bid of a player. This function is called recursively in the
        getBids function in case of an invalid bid, i.e., a bid lower than the
        previous bid, a bid lower than 7, or a bid higher than 13.

        Args:
            player (Player): The player to get the bid of.

        Returns:
            int: The bid of the player.
        """

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
        """ Gets the bids of the players. """

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
        """ Plays a round of the game. """

        print(f"Round {self.round} started.\n")
        self.displayHands()

        if self.round == 1:
            self.getBids()

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
        """
        Gets the cards from a player. This function is called recursively in
        case of an invalid card, i.e., a card that is not the same suit as the
        first card played in the trick and the player has a card of the same
        suit in their hand.

        Args:
            i (int): The index of the player.
            player (Player): The player to get the cards from.

        Returns:
            int: The index of the card played.
            Card: The card played.
        """

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
        """ Gets the cards from the players. """

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

    def determineWinner(self):
        """
        Determines the winner of the trick.

        Returns:
            Player: The winner of the trick.
        """

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

    def printWinners(self):
        """ Prints the winners of the game. """

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

    def playGame(self):
        """
        Plays the game. The game is played until one of the teams reaches a
        cumulative score of 60 or more.

        At the end of each round, the scores of the players are updated. If the
        team with the highest bid gets a greater score or equal to their bid,
        their total score of the game gets updated by adding their points for
        the round. Otherwise, their total score of the game gets updated by
        subtracting their bid from their total score of the game and the other
        team's score gets updated by adding their points for the round.
        """

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


if __name__ == "__main__":
    playerNames = ["Player 1", "Player 2", "Player 3", "Player 4"]
    game = TarneebGame(playerNames)
    game.playGame()
