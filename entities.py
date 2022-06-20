from enum import Enum

class EntityType(Enum):
    WALL = 0
    POWERUP = 1
    MONSTER = 2
    PLAYER = 3

class Entity:
    def __init__(self,grid_position,game):
        self.grid_x,self.grid_y = grid_position
        self.physical_x,self.physical_y = grid_position
        self.game = game
    def get_type(self):
        raise NotImplementedError('Entities should implement get_type method')

class Wall(Entity):
    def get_type(self):
        return EntityType.WALL

class Powerup(Entity):
    def get_type(self):
        return EntityType.POWERUP

class Movable(Entity):
    def __init__(self,grid_position,game):
        super().__init__(grid_position,game)
        self.vx = 0
        self.vy = 0
    def _snap_to_grid(self,vertical):
        if vertical:
            self.physical_y = self.grid_y
        else:
            self.physical_x = self.grid_x
    # TODO Implement collision detection