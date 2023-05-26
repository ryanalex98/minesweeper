import unittest
from src.board import Board


class TestBoard(unittest.TestCase):

    def create_board(self):
        board = Board(height=3, width=4, n_mines=3)
        board._board_of_tiles[0][3].set_mine()
        board._board_of_tiles[2][1].set_mine()
        board._board_of_tiles[2][3].set_mine()
        board._update_neighboring_mine_counts()
        board._is_seeded = True

        board.receive_move_command("s")
        board.receive_move_command("d")
        board.receive_move_command("e")
        board.display()



    def test_set_zeros(self):

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
