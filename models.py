from enum import Enum
import pygame
from os.path import join

def load_sprite(sprite_name,size):
    path = join('assets','sprites',f'{sprite_name}.png')
    sprite = pygame.image.load(path)
    sprite = pygame.transform.scale(sprite,size)
    sprite.set_colorkey((255,255,255))
    return sprite

GRID_SIZE = 40

class GraphicObject:
    def get_current_sprite(self):
        raise NotImplementedError('Graphic objects should return a sprite.')


class EntityType(Enum):
    WALL = 'X'
    POWERUP = 'U'
    MONSTER = 'M'
    PLAYER = 'P'

class MovingState(Enum):
    ACTIVE = 0
    MOVING_RIGHT = 1
    MOVING_LEFT = 2
    SLEEPING = 3
    
GRAVITY = 10
PLAYER_VERTICAL_SPEED = -10
PLAYER_SPEED = 3
MONSTER_SPEED = 3

class Entity:
    def __init__(self,grid_position,game):
        self.grid_x,self.grid_y = grid_position
        self.physical_x = self.grid_x + .5
        self.physical_y = self.grid_y + .5
        self.game = game
    def get_type(self):
        raise NotImplementedError('Entities should implement get_type method')

class Wall(Entity,GraphicObject):
    def __init__(self,grid_position,game):
        Entity.__init__(self,grid_position,game)
        self.sprite = load_sprite('wall',(GRID_SIZE,GRID_SIZE))
    def get_current_sprite(self):
        return self.sprite        
    def get_type(self):
        return EntityType.WALL

class Powerup(Entity,GraphicObject):
    def __init__(self,grid_position,game):
        Entity.__init__(self,grid_position,game)
        self.sprite = load_sprite('powerup_green',(GRID_SIZE,GRID_SIZE))
    def get_current_sprite(self):
        return self.sprite        
    def get_type(self):
        return EntityType.POWERUP

class Movable(Entity,GraphicObject):
    def __init__(self,grid_position,game):
        Entity.__init__(self,grid_position,game)
        self.vx = 0
        self.vy = 0
        self.state = MovingState.ACTIVE
    def _snap_to_grid(self,vertical):
        if vertical:
            self.physical_y = self.grid_y
        else:
            self.physical_x = self.grid_x
    def update(self,delta_time):
        self._update_position(delta_time)
        self._update_speed(delta_time)
        self._update_grid()
    def _update_position(self,delta_time):
        self.physical_x += self.vx * delta_time
        self.physical_y += self.vy * delta_time
    def _update_speed(self,delta_time):
        pass
    def _update_grid(self):
        new_x,new_y = int(self.physical_x),int(self.physical_y)
        if (
            new_x != self.grid_x or 
            new_y != self.grid_y
            ):
            self.game.update_grid(
                (self.grid_x,self.grid_y),
                (new_x,new_y))
            self.grid_x = new_x
            self.grid_y = new_y
    def move_right(self):
        raise NotImplementedError('Movable should implement move_right')
    def move_left(self):
        raise NotImplementedError('Movable should implement move_left')
    def stand_still(self):
        self.vx = 0

class Monster(Movable):
    def __init__(self,grid_position,game):
        Movable.__init__(self,grid_position,game)
        self.sprites = {
            MovingState.ACTIVE : load_sprite('monster',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_RIGHT : load_sprite('monster',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_LEFT : load_sprite('monster',(GRID_SIZE,GRID_SIZE)),
            MovingState.SLEEPING : load_sprite('monster_sleeping',(GRID_SIZE,GRID_SIZE)),
        }
    def get_current_sprite(self):
        return self.sprites[self.state]
    def move_right(self):
        self.vx = MONSTER_SPEED
    def move_left(self):
        self.vx = -MONSTER_SPEED

class Player(Movable):
    def __init__(self,grid_position,game):
        Movable.__init__(self,grid_position,game)
        self.sprites = {
            MovingState.ACTIVE : load_sprite('player_standing',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_RIGHT : load_sprite('player_moving_right',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_LEFT : load_sprite('player_moving_left',(GRID_SIZE,GRID_SIZE)),
        }
    def get_current_sprite(self):
        return self.sprites[self.state]
    
    def _update_speed(self, delta_time):
        if self._on_solid_ground():
            return
        self.vy += GRAVITY * delta_time
    
    def _on_solid_ground(self):
        x,y = self.grid_x,self.grid_y
        lower_neighbor = self.game.get_entity((x,y+1))
        if lower_neighbor and lower_neighbor.physical_y - self.physical_y < 1:
            self.physical_y = self.grid_y + .5
            return True
        return False

    def move_right(self):
        self.vx = PLAYER_SPEED
        self.state = MovingState.MOVING_RIGHT
    
    def move_left(self):
        self.vx = -PLAYER_SPEED
        self.state = MovingState.MOVING_LEFT
    def jump(self):
        self.vy = PLAYER_VERTICAL_SPEED