from typing import Optional


class Tile(object):
    def __init__(self):
        self._is_mine: Optional[bool] = False
        self._neighboring_mines: Optional[int] = 0
        self._is_swept = False
        self._is_flagged = False
        self._display_char = ' '
        self._is_cursor = False

    def sweep(self):
        self._is_swept = True
        self._is_flagged = False

    def toggle_flag(self):
        if not self._is_swept:
            self._is_flagged = not self._is_flagged

    def toggle_cursor(self):
        self._is_cursor = not self._is_cursor

    def set_mine(self):
        self._is_mine = True

    def get_mine_status(self):
        return self._is_mine

    def set_neighboring_mines(self, num_mines: int):
        self._neighboring_mines = num_mines

    def get_neighboring_mines(self) -> int:
        return self._neighboring_mines

    def display(self) -> str:
        return self._calculate_display_state()

    def _calculate_display_state(self):
        if self._is_flagged:
            return 'F'
        if self._is_swept:
            if self._is_mine:
                return '*'
            elif self._neighboring_mines == 0:
                return ' '
            else:
                return str(self._neighboring_mines)
        else:
            return '#'


