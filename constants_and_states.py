from enum import Enum

GRID_SIZE = 40


class GameState(Enum):
    IN_PROGRESS = 0
    IS_WON = 1
    IS_LOST = 2

class Commands(Enum):
    STAND_STILL = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    JUMP = 3