from enum import Enum

GRID_SIZE = 40

GRAVITY = 10
PLAYER_VERTICAL_SPEED = -10
PLAYER_SPEED = 3
MONSTER_SPEED = 3
class EntityType(Enum):
    WALL = 'X'
    POWERUP = 'U'
    MONSTER = 'M'
    PLAYER = 'P'
    TREASURE = 'T'

class MovingState(Enum):
    ACTIVE = 0
    MOVING_RIGHT = 1
    MOVING_LEFT = 2
    SLEEPING = 3
class GameState(Enum):
    IN_PROGRESS = 0
    IS_WON = 1
    IS_LOST = 2

class Commands(Enum):
    STAND_STILL = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    JUMP = 3