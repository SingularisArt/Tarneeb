"""
Tarneeb is a trick-taking card game for four players. The game is played
with a standard 52-card deck. The goal of the game is to win the most
tricks.
"""

import argparse
import pprint
import random


class Hand:
    """
    Hand class that represents a player's hand of cards.

    Attributes:
        cards (list): List of cards in the player's hand.
    """

    def __init__(self, cards, bid=None):
        """
        Hand class that represents a player's hand of cards.

        Args:
            cards (list): List of cards in the player's hand.
            bid (int): Bid of the player.
        """

        self.cards = cards
        self.cardValues = [self.calculateCardValue(card) for card in cards]
        self.handValue = self.calculateHandValue()
        self.playerBid = bid if bid is not None else self.bid()
        self.suitCounts = self.getSuitCounts()

    def __repr__(self):
        """
        Returns a string representation of the Hand class.

        Returns:
            string: String representation of the Hand class.
        """

        return pprint.pformat(
            {
                "cards": self.cards,
                "bid": self.playerBid,
            }
        )

    def calculateCardValue(self, card):
        """
        Calculates the value of a card based on the rest of the hand. The value
        of the card is calculated by multiplying the rank (2-10, J=11, Q=12,
        K=13, A=15) by the number of cards with the same suit.

        Args:
            card (dict): Card to calculate the value of.

        Returns:
            int: Value of the card.
        """

        rankValue = card["rank"]
        if rankValue == "J":
            rankValue = 11
        elif rankValue == "Q":
            rankValue = 12
        elif rankValue == "K":
            rankValue = 13
        elif rankValue == "A":
            rankValue = 15
        else:
            rankValue = int(rankValue)

        numCardsWithSameSuit = len(
            [card for card in self.cards if card["suit"] == card["suit"]]
        )

        return rankValue * numCardsWithSameSuit

    def calculateHandValue(self):
        """
        Calculates the value of the player's hand.

        Returns:
            int: Value of the player's hand.
        """

        # The hand value is calculated by adding the value of each card in the
        # hand.
        return sum(self.cardValues)

    def getSuitCounts(self):
        """
        Gets the value of each suit in the player's hand based on the
        cards in the hand.

        Returns:
            dict: Dictionary of the suit counts.
        """

        suitCounts = {"h": 0, "s": 0, "d": 0, "c": 0}
        suitCountsTemp = {"h": 0, "s": 0, "d": 0, "c": 0}

        for card in self.cards:
            suitCounts[card["suit"]] += 1

        # Iterate over the cards
        for x, card in enumerate(self.cards):
            suitCountsTemp[card["suit"]] += self.cardValues[x]

        # Multiply the suit counts by the card values
        for suit in suitCountsTemp:
            suitCounts[suit] *= suitCountsTemp[suit]

        return suitCounts

    def bid(self):
        """
        Calculates the bid of the player based on the cards in the hand.

        The bid calculated as follows:
        1. If the hand value is less than 1000, pass
        2. If the hand value is between 1000 and 1200, bid 7
        3. If the hand value is between 1200 and 1400, bid 8
        4. If the hand value is between 1400 and 1600, bid 9
        5. If the hand value is between 1600 and 1800, bid 10
        6. If the hand value is between 1800 and 2000, bid 11
        7. If the hand value is between 2000 and 2200, bid 12
        8. If the hand value is greater than 2200, bid 13

        Returns:
            int: Bid of the player.
        """

        if self.handValue < 1000:
            return "p"
        elif 1000 <= self.handValue < 1200:
            return 7
        elif 1200 <= self.handValue < 1400:
            return 8
        elif 1400 <= self.handValue < 1600:
            return 9
        elif 1600 <= self.handValue < 1800:
            return 10
        elif 1800 <= self.handValue < 2000:
            return 11
        elif 2000 <= self.handValue < 2200:
            return 12
        elif 2200 <= self.handValue:
            return 13


class Game:
    """
    Game class that represents a game of Tarneeb.

    Attributes:
        deck (list): A list of cards in the deck.
        players (dict): A dictionary of players in the game.
        trump_suit (str): The trump suit of the game.
        teamBids (dict): A dictionary of the bids of each team.
        highestBid (dict): A dictionary of the highest bid of each team.
    """

    def __init__(self, player1Bid, player2Bid, player3Bid) -> None:
        """
        Game class that represents a game of Tarneeb.

        Args:
            player1Bid (int): Bid of player 1.
            player2Bid (int): Bid of player 2.
            player3Bid (int): Bid of player 3.
        """

        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                      "J", "Q", "K", "A"]
        self.suits = ["h", "s", "d", "c"]

        self.deck = self.generateDeck()
        self.players = {
            "team1": {
                "score": 0,
                "player1": Hand(self.deck[0:13], player1Bid),
                "player2": Hand(self.deck[13:26], player2Bid),
            },
            "team2": {
                "score": 0,
                "player3": Hand(self.deck[26:39], player3Bid),
                "player4": Hand(self.deck[39:52]),
            },
        }

        self.tricks = {player: [] for player in self.players}

        self.trumpSuit = self.determineTrumpSuit(
            self.players["team1"]["player1"],
        )

        self.teamBids = {
            "team1": {
                "player1": player1Bid,
                "player2": player2Bid,
            },
            "team2": {
                "player3": player3Bid,
                "player4": self.players["team2"]["player4"].bid(),
            },
        }

        self.highestBid = self.findHighestBidder()

    def __repr__(self):
        """
        Returns a string representation of the Game class.

        Returns:
            string: String representation of the Game class.
        """

        return pprint.pformat(self.players)

    def generateDeck(self):
        """
        Generates a deck of cards.

        Returns:
            list: List of cards in the deck.
        """

        suits = ["h", "s", "d", "c"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "J", "Q", "K", "A"]

        deck = [
            {"rank": rank, "suit": suit}
            for suit in suits
            for rank in ranks
        ]

        random.shuffle(deck)

        return deck

    def determineTrumpSuit(self, player):
        """
        Determines the trump suit of the game.

        Args:
            player (Hand): Player to determine the trump suit of.

        Returns:
            str: Trump suit of the game.
        """

        # Get the suit counts from the Hand class
        suits = player.getSuitCounts()

        # Get the suit that has the highest value from the Hand function
        highestSuit = max(suits.items(), key=lambda x: (x[1], random.random()))

        # Detuple the result
        return highestSuit[0]

    def findHighestBidder(self):
        """
        Finds the highest bidder of the game.

        Returns:
            dict: Dictionary of the highest bidder and their bid.
        """

        # Get the highest bidder from the teamBids dictionary
        highestBidder = max(
            (
                (player, int(bid) if bid != "p" else 0)
                for team in self.teamBids.values()
                for player, bid in team.items()
            ),
            key=lambda x: (x[1], random.random()),
        )

        # Detuple the result
        return {highestBidder[0]: highestBidder[1]}

    def checkBids(self):
        """
        Checks the bids of each player to make sure they are valid.

        Raises:
            ValueError: If the bid is not between 7 and 13.
            ValueError: If the bid is not greater than the previous bid.
            ValueError: If the bid is not an integer.
            ValueError: If the bid is not a valid bid.
            ValueError: If the bid is not a valid bid.
            ValueError: If the bid is not a valid bid.
        """

        player1Bid = self.teamBids["team1"]["player1"]
        player2Bid = self.teamBids["team1"]["player2"]
        player3Bid = self.teamBids["team2"]["player3"]

        # If the bid is "p", then the player passes and set it to None
        player1Bid = None if player1Bid == "p" else int(player1Bid)
        player2Bid = None if player2Bid == "p" else int(player2Bid)
        player3Bid = None if player3Bid == "p" else int(player3Bid)

        # If the bids are not between 7 and 13, then raise an error
        if player1Bid is not None and not (7 <= player1Bid <= 13):
            raise ValueError("Player 1 bid must be between 7 and 13.")
        elif player2Bid is not None and not (7 <= player2Bid <= 13):
            raise ValueError("Player 2 bid must be between 7 and 13.")
        elif player3Bid is not None and not (7 <= player3Bid <= 13):
            raise ValueError("Player 3 bid must be between 7 and 13.")

        # Each bid must be greater than the previous bid
        if (
            player1Bid is not None
            and player2Bid is not None
            and not player1Bid < player2Bid
        ):
            raise ValueError("Player 1 bid must be greater than player 2 bid.")
        elif (
            player2Bid is not None
            and player3Bid is not None
            and not player2Bid < player3Bid
        ):
            raise ValueError("Player 2 bid must be greater than player 3 bid.")
        elif (
            player1Bid is not None
            and player3Bid is not None
            and not player1Bid < player3Bid
        ):
            raise ValueError("Player 1 bid must be greater than player 3 bid.")

    def determineHighestCard(self, cards):
        """
        Determines the highest card in a round.

        Args:
            cards (list): List of cards in the round.

        Returns:
            dict: The highest card in the round.
        """

        # First, find all the trump cards
        trumpCards = [card for card in cards if card["suit"] == self.trumpSuit]
        if len(trumpCards) > 0:
            # If there are trump cards, then find the highest trump card
            return max(
                trumpCards,
                key=lambda x: (self.ranks.index(x["rank"]), random.random()),
            )

        # If there are no trump cards, then find the highest card
        return max(
            cards,
            key=lambda x: (self.ranks.index(x["rank"]), random.random()),
        )

    def playRound(self):
        """ Plays a round of Tarneeb. """

        # Get the highest bidder
        highestBidder = list(self.highestBid.keys())[0]

        # Play the highest card from the highest bidder
        team = None
        if highestBidder == "player1" or highestBidder == "player2":
            team = "team1"
        else:
            team = "team2"

        cards = self.players[team][highestBidder].cards
        highestCard = self.determineHighestCard(cards)

        print(f"The trump suit is {self.trumpSuit.upper()}.")
        print(f"Player 4: {self.displayCard(highestCard)}")

        player1Card = self.displayCardToDict(input("Player 1: "))
        player2Card = self.displayCardToDict(input("Player 2: "))
        player3Card = self.displayCardToDict(input("Player 3: "))

        playedCards = [
            player1Card,
            player2Card,
            player3Card,
            highestCard,
        ]

        highestPlayedCard = self.determineHighestCard(playedCards)
        wonPlayer = playedCards.index(highestPlayedCard) + 1
        print(f"Player {wonPlayer} won the round.")

    def displayCard(self, card):
        """
        Displays a card in a human-readable format.
        EXM: {"rank": "2", "suit": "h"} -> 2H

        Args:
            card (dict): Card to display.

        Returns:
            string: String representation of the card.
        """

        return f"{card['rank']}{card['suit'].upper()}"

    def displayCardToDict(self, card):
        """
        Converts a human-readable card to a dictionary.
        EXM: 2H -> {"rank": "2", "suit": "h"}

        Args:
            card (string): Card to convert.

        Returns:
            dict: Dictionary representation of the card.
        """

        return {
            "rank": card[0],
            "suit": card[1].lower(),
        }


def main():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument(
        "-pb",
        "--player-bids",
        type=str,
        required=True,
        help="A list of the player bids.",
    )

    # Parse arguments
    args = parser.parse_args()

    player1Bid, player2Bid, player3Bid = args.player_bids.split(",")
    game = Game(player1Bid, player2Bid, player3Bid)

    game.playRound()


if __name__ == "__main__":
    main()
