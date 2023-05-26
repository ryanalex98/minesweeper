from src.board import Board
from src.player import Player


class Game(object):
    def __init__(self, height: int, width: int, n_mines: int):
        self._height = height
        self._width = width
        self._board = Board(height=height, width=width, n_mines=n_mines)
        self._player = Player()
        self._is_not_game_over = False
        self._n_mines = n_mines
        self._valid_move_commands = ['w', 'a', 's', 'd', 'e', 'f']

    def play(self):
        self._display()
        while not self._is_game_over():
            self._move()
            self._display()
        self._display_game_over_message()

    def _is_game_over(self):
        if self._game_won() or self._game_lost():
            return True
        else:
            return False

    def _display_game_over_message(self):
        if self._game_lost():
            print("Game over :(")
        elif self._game_won():
            print("Congratulations!")


    def _move(self):
        while True:
            move_command = self._player.request_move_command()
            if self._valid_move_command(move_command):
                break
            print("Invalid move. Try again.")
        self._board.receive_move_command(move_command)

    def _valid_move_command(self, move_command):
        if move_command in self._valid_move_commands:
            return True
        else:
            return False

    def _display(self):
        self._board.display()

    def _game_won(self) -> bool:
        if self._board.get_undiscovered_count() == self._n_mines:
            return True
        else:
            return False

    def _game_lost(self) -> bool:
        if self._board.has_swept_mine():
            return True
        else:
            return False

