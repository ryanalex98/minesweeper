from src.game import Game


if __name__ == "__main__":
    game = Game(height=10, width=10, n_mines=10)
    game.play()
