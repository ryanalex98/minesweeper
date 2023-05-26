from src.tile import Tile
from src.data_model.enums import MoveType
from src.utils import clear_screen
from typing import Tuple, List, Set
import random


class Board(object):
    def __init__(self, height: int, width: int, n_mines: int):
        self._height = height  # num_rows, length_col
        self._width = width  # num_cols, length_row
        self._n_mines = n_mines
        self._cursor_pos: Tuple[int, int] = (0, 0)
        self._board_of_tiles = [[Tile() for i in range(self._width)] for j in range(self._height)]
        self._is_unseeded = True

    def receive_move_command(self, move_command: str):
        if move_command == "w":
            self._attempt_cursor_move((-1, 0))
        elif move_command == "s":
            self._attempt_cursor_move((1, 0))
        elif move_command == "a":
            self._attempt_cursor_move((0, -1))
        elif move_command == "d":
            self._attempt_cursor_move((0, 1))
        elif move_command == "e":
            self._apply_move(MoveType.SWEEP)
        elif move_command == "f":
            self._apply_move(MoveType.FLAG)

    def _get_tile_from_ordered_pair(self, coord: Tuple[int, int]) -> Tile:
        return self._board_of_tiles[coord[0]][coord[1]]

    def _apply_move(self, move_type: MoveType):
        if move_type == MoveType.FLAG:
            self._board_of_tiles[self._cursor_pos[0]][self._cursor_pos[1]].toggle_flag()
        if move_type == MoveType.SWEEP:
            if self._is_unseeded:
                self._seed_board()
                self._is_unseeded = False
            self._auto_sweep()

    def _auto_sweep(self):
        set_to_sweep = self._collect_tiles_connected_to_guess()
        self._sweep_coordinates(coords_to_sweep=list(set_to_sweep))

    def _collect_tiles_connected_to_guess(self) -> Set:
        set_of_zeros = set()
        set_to_sweep = set()
        set_to_sweep.add(self._cursor_pos)


        queue = []
        visited = set()
        cursor_neighbors = self._get_neighboring_coordinates(self._cursor_pos)
        for cursor_neighbor_coord in cursor_neighbors:
            cursor_neighbor_tile = self._get_tile_from_ordered_pair(cursor_neighbor_coord)
            if cursor_neighbor_tile.get_neighboring_mines() == 0 and not cursor_neighbor_tile.get_mine_status():
                queue.append(cursor_neighbor_coord)

        while queue:
            coords = queue.pop(0)
            visited.add(coords)
            if self._board_of_tiles[coords[0]][coords[1]].get_neighboring_mines() == 0 and not self._board_of_tiles[coords[0]][coords[1]].get_mine_status():
                set_of_zeros.add(coords)
            neighboring_coords = self._get_neighboring_coordinates(coords)
            for neighboring_coord in neighboring_coords:
                if neighboring_coord not in visited:
                    queue.append(neighboring_coord)

        neighbor_sweep_set = self._add_neighbors_to_sweep(set_of_zeros)
        set_to_sweep.update(neighbor_sweep_set)
        return set_to_sweep


    def _add_neighbors_to_sweep(self, set_of_zeros_and_cursor: Set):
        iterable_set_of_zeros = list(set_of_zeros_and_cursor.copy())
        sweep_set = set_of_zeros_and_cursor
        for coord in iterable_set_of_zeros:
            if self._board_of_tiles[coord[0]][coord[1]].get_neighboring_mines() == 0:
                neighboring_coords = self._get_neighboring_coordinates(coord)
                sweep_set.update(set(neighboring_coords))
        return sweep_set

    def _sweep_coordinates(self, coords_to_sweep: List[Tuple[int, int]]):
        for coord in coords_to_sweep:
            self._board_of_tiles[coord[0]][coord[1]].sweep()

    def _attempt_cursor_move(self, attempted_position_change: Tuple[int, int]):
        cursor_row_num = self._cursor_pos[0]
        cursor_col_num = self._cursor_pos[1]
        new_cursor_row_num = cursor_row_num
        new_cursor_col_num = cursor_col_num
        if 0 <= cursor_row_num + attempted_position_change[0] < self._height:
            new_cursor_row_num = cursor_row_num + attempted_position_change[0]
        if 0 <= cursor_col_num + attempted_position_change[1] < self._width:
            new_cursor_col_num = cursor_col_num + attempted_position_change[1]
        self._cursor_pos = (new_cursor_row_num, new_cursor_col_num)

    def display(self):
        display_chars = self._generate_display_chars()
        user_friendly_display = self._make_display_user_friendly(display_chars=display_chars)
        self._print_user_friendly_display(user_friendly_display=user_friendly_display)

    def _generate_display_chars(self):
        display_chars = []
        for row_num in range(self._height):
            new_row = []
            for col_num in range(self._width):
                new_row.append(self._board_of_tiles[row_num][col_num].display())
            display_chars.append(new_row)
        return display_chars

    def _make_display_user_friendly(self, display_chars: List[List[str]]) -> List[List[str]]:

        user_friendly_display = []

        # row_num_prefix_length = 4
        # header_column_nums = [' ' for i in range(row_num_prefix_length)]
        # underline_column_nums = [' ' for i in range(row_num_prefix_length)]
        # for i in range(self._width):
        #     char_to_show = str(i)
        #     if self._cursor_pos[1] == i:
        #         char_to_show = 'X'
        #     header_column_nums += [char_to_show, ' ']
        #     underline_column_nums += ['_', ' ']
        # user_friendly_display.append(header_column_nums)
        # user_friendly_display.append(underline_column_nums)

        for row_num in range(len(display_chars)):
            # char_to_show = str(row_num)
            # if self._cursor_pos[0] == row_num:
            #     char_to_show = 'X'
            # row_num_prefix = [char_to_show, ' ', '|', ' ']
            # entire_row = row_num_prefix

            entire_row = [' ']
            for col_num in range(len(display_chars[row_num])):
                entire_row += [display_chars[row_num][col_num], ' ']
                if row_num == self._cursor_pos[0] and col_num == self._cursor_pos[1]:
                    entire_row[-3] = '<'
                    entire_row[-1] = '>'
            user_friendly_display.append(entire_row)
        return user_friendly_display

    @staticmethod
    def _print_user_friendly_display(user_friendly_display: List[List[str]]):
        clear_screen()
        for row in user_friendly_display:
            row_output = ''.join(row)
            print(row_output)

    def has_swept_mine(self) -> bool:
        for row in self._board_of_tiles:
            for tile in row:
                if tile.display() == '*':
                    return True
        return False

    def get_undiscovered_count(self) -> int:
        counter = 0
        for row in self._board_of_tiles:
            for tile in row:
                if tile.display() == 'F' or tile.display() == '#':
                    counter += 1
        return counter

    def _seed_board(self):
        self._place_mines()
        self._update_neighboring_mine_counts()

    def _place_mines(self):
        coords = self._get_list_of_coords_minus_cursor()
        for i in range(self._n_mines):
            coord = coords.pop(random.randrange(len(coords)))
            self._board_of_tiles[coord[0]][coord[1]].set_mine()

    # def _place_mines(self):
    #     self._board_of_tiles[0][0].set_mine()
    #     self._board_of_tiles[0][2].set_mine()
    #     self._board_of_tiles[0][3].set_mine()

    def _update_neighboring_mine_counts(self):
        for row_num in range(self._height):
            for col_num in range(self._width):
                neighbors = self._get_neighboring_coordinates(coord=(row_num, col_num))
                mine_count = 0
                for neighbor in neighbors:
                    mine_count += int(self._board_of_tiles[neighbor[0]][neighbor[1]].get_mine_status())
                self._board_of_tiles[row_num][col_num].set_neighboring_mines(mine_count)

    def _get_list_of_coords_minus_cursor(self) -> List[Tuple[int, int]]:
        coords = []
        for row_num in range(self._height):
            for col_num in range(self._width):
                if row_num != self._cursor_pos[0] and col_num != self._cursor_pos[1]:
                    coords.append((row_num, col_num))
        return coords

    def _get_neighboring_coordinates(self, coord: Tuple[int, int]):
        coord_diffs_to_check = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        neighboring_coords = []
        for coord_diff in coord_diffs_to_check:
            if self._is_valid_row_num(coord[0] + coord_diff[0]) and self._is_valid_col_num(coord[1] + coord_diff[1]):
                neighboring_coords.append((coord[0] + coord_diff[0], coord[1] + coord_diff[1]))
        return neighboring_coords

    def _is_valid_row_num(self, row_num):
        if 0 <= row_num < self._height:
            return True
        else:
            return False

    def _is_valid_col_num(self, col_num):
        if 0 <= col_num < self._width:
            return True
        else:
            return False
