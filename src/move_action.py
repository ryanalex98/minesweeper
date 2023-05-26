from dataclasses import dataclass
from data_model.enums import MoveType


@dataclass
class MoveAction:
    row: int
    col: int
    move_type: MoveType