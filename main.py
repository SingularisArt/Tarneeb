from game import TarneebGame
import model


def main():
    playerNames = ["Player 1", "Player 2", "Player 3", "Player 4"]
    game = TarneebGame(playerNames)
    game.playGame()


if __name__ == "__main__":
    main()
