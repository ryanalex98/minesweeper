from typing import List


class Player(object):
    def __init__(self):
        self._valid_moves: List = ["e", "f"]

    @staticmethod
    def request_move_command() -> str:
        print("Commmand List: w-a-s-d to move cursor, e to sweep, f to flag.")
        move_command = input("Move Command: ")
        return move_command

    def invalid_move(self):
        pass


