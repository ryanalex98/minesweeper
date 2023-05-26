from enum import Enum


class MoveType(Enum):
    FLAG = 0
    SWEEP = 1


class DisplayType(Enum):
    UNDISCOVERED = 0
    FLAGGED = 1
    NUMBERED = 2
    MINE = 3
    EMPTY = 4
