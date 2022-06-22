from constants_and_states import GameState, EntityType, MovingState
from constants_and_states import GRID_SIZE, GRAVITY
from constants_and_states import PLAYER_SPEED, PLAYER_VERTICAL_SPEED, MONSTER_SPEED

from utility import load_sprite

class GraphicObject:
    """
    Abstract class to represent a GraphicObject

    Methods:
    ---------
    get_current_sprite : Surface
        Return the active sprite of the graphic object
    """
    def get_current_sprite(self):
        raise NotImplementedError('Graphic objects should return a sprite.')

class Entity:
    """
    Abstract class to represent a logical game entity.

    Methods:
    ---------
    get_id : int
        Return the unique ID of the entity
    get_type : EntityType
        Return the type of the entity
    """
    ID = 0
    def __init__(self,grid_position,game):
        self._id = Entity.ID
        Entity.ID += 1
        self.grid_x,self.grid_y = grid_position
        self.physical_x = self.grid_x + .5
        self.physical_y = self.grid_y + .5
        self.game = game

    def get_id(self):
        return self._id

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
        self.sprites = {
            False: load_sprite('powerup_green',(GRID_SIZE,GRID_SIZE)),
            True: load_sprite('invisible',(GRID_SIZE,GRID_SIZE))}
        self.is_used = False

    def get_current_sprite(self):
        return self.sprites[self.is_used]       

    def get_type(self):
        return EntityType.POWERUP

    def apply(self,player):
        raise NotImplementedError('Powerups should implement apply method')

class SpeedPowerup(Powerup):
    def apply(self,player):
        player.speed = 2*PLAYER_SPEED

class Treasure(Entity,GraphicObject):
    def __init__(self,grid_position,game):
        Entity.__init__(self,grid_position,game)
        self.sprite = load_sprite('treasure',(GRID_SIZE,GRID_SIZE))
    def get_current_sprite(self):
        return self.sprite        
    def get_type(self):
        return EntityType.TREASURE

class Movable(Entity,GraphicObject):
    """
    Abstract class to represent a movable entity

    Methods:
    ---------
    update(delta_time) : int -> None
        Update position and state based on elapsed time in seconds
    """
    def __init__(self,grid_position,game):
        Entity.__init__(self,grid_position,game)
        self.vx = 0
        self.vy = 0
        self.state = MovingState.ACTIVE

    def _handle_collisions(self):
        for neighbor in self.game.get_neighborhood((self.grid_x,self.grid_y)):
            if neighbor.grid_x == self.grid_x:
                if (
                    self.physical_y - neighbor.physical_y < 1 and 
                    self.physical_y - neighbor.physical_y >= 0):
                    self._handle_upward_collision(neighbor)
                elif (
                    self.physical_y - neighbor.physical_y > -1 and 
                    self.physical_y - neighbor.physical_y <= 0):
                    self._handle_downward_collision(neighbor)
            elif neighbor.grid_y == self.grid_y:
                if (
                    self.physical_x - neighbor.physical_x < 1 and 
                    self.physical_x - neighbor.physical_x >= 0):
                    self._handle_right_collision(neighbor)
                elif (
                    self.physical_x - neighbor.physical_x > -1 and 
                    self.physical_x - neighbor.physical_x <= 0):
                    self._handle_left_collision(neighbor)

    def _handle_downward_collision(self,neighbor):
        if neighbor.get_type() == EntityType.WALL:
            self.vy = 0
            self._snap_to_grid(True)

    def _handle_upward_collision(self,neighbor):
        if neighbor.get_type() == EntityType.WALL:
            self.vy = 0
            self._snap_to_grid(True)

    def _handle_right_collision(self,neighbor):
        if neighbor.get_type() == EntityType.WALL:
            self.vx = 0
            self._snap_to_grid(False)

    def _handle_left_collision(self,neighbor):
        if neighbor.get_type() == EntityType.WALL:
            self.vx = 0
            self._snap_to_grid(False)

    def _snap_to_grid(self,vertical):
        if vertical:
            self.physical_y = self.grid_y + 0.5
        else:
            self.physical_x = self.grid_x + 0.5

    def update(self,delta_time):
        self._update_position(delta_time)
        self._update_speed(delta_time)
        self._update_grid()
        self._handle_collisions()

    def _update_position(self,delta_time):
        self.physical_x += self.vx * delta_time
        self.physical_y += self.vy * delta_time

    def _update_speed(self, delta_time):
        self.vy += GRAVITY * delta_time

    def _update_grid(self):
        new_x,new_y = int(self.physical_x),int(self.physical_y)
        if (
            new_x != self.grid_x or 
            new_y != self.grid_y
            ):
            self.game.update_grid(
                self,
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
        self.state = MovingState.ACTIVE
        self.move_right()

    def put_asleep(self):
        self.stand_still()
        self.state = MovingState.SLEEPING

    def update(self,delta_time):
        Movable.update(self,delta_time)
        has_free_path = self._check_free_path()
        if self.state == MovingState.MOVING_RIGHT and not has_free_path:
            self.move_left()
        elif self.state == MovingState.MOVING_LEFT and not has_free_path:
            self.move_right()

    def _check_free_path(self):
        x,y = self.grid_x,self.grid_y
        if self.state == MovingState.MOVING_RIGHT:
            x += 1
        elif self.state == MovingState.MOVING_LEFT:
            x -= 1
        for neighbor in self.game.get_entity((x,y)):
            if neighbor.get_type() == EntityType.WALL:
                return False
        for neighbor in self.game.get_entity((x,y+1)):
            if neighbor.get_type() == EntityType.WALL:
                return True
        return False        

    def get_current_sprite(self):
        return self.sprites[self.state]

    def move_right(self):
        self.vx = MONSTER_SPEED
        self.state = MovingState.MOVING_RIGHT

    def move_left(self):
        self.vx = -MONSTER_SPEED
        self.state = MovingState.MOVING_LEFT

    def get_type(self):
        return EntityType.MONSTER

class Player(Movable):

    def __init__(self,grid_position,game):
        Movable.__init__(self,grid_position,game)
        self.sprites = {
            MovingState.ACTIVE : load_sprite('player_standing',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_RIGHT : load_sprite('player_moving_right',(GRID_SIZE,GRID_SIZE)),
            MovingState.MOVING_LEFT : load_sprite('player_moving_left',(GRID_SIZE,GRID_SIZE)),
        }
        self.powerups = []
        self.speed = PLAYER_SPEED

    def get_current_sprite(self):
        return self.sprites[self.state]
    
    def move_right(self):
        self.vx = self.speed
        self.state = MovingState.MOVING_RIGHT
    
    def move_left(self):
        self.vx = -self.speed
        self.state = MovingState.MOVING_LEFT
    
    def stand_still(self):
        self.state = MovingState.ACTIVE
        return super().stand_still()

    def jump(self):
        for entity in self.game.get_entity(
            (self.grid_x,self.grid_y+1)):
            if entity.get_type() == EntityType.WALL:
                self.vy = PLAYER_VERTICAL_SPEED

    def get_type(self):
        return EntityType.PLAYER

    def update(self,delta_time):
        for powerup in self.powerups:
            powerup.apply(self)
        Movable.update(self,delta_time)

    def _handle_right_collision(self,neighbor):
        Movable._handle_right_collision(self,neighbor)
        if (
            neighbor.get_type() == EntityType.MONSTER and 
            neighbor.state != MovingState.SLEEPING):
            self.game.set_game_state(GameState.IS_LOST)
        else:
            self._handle_normal_collision(neighbor)

    def _handle_left_collision(self,neighbor):
        Movable._handle_left_collision(self,neighbor)
        if (
            neighbor.get_type() == EntityType.MONSTER and 
            neighbor.state != MovingState.SLEEPING):
            self.game.set_game_state(GameState.IS_LOST)
        else:
            self._handle_normal_collision(neighbor)

    def _handle_downward_collision(self,neighbor):
        Movable._handle_downward_collision(self,neighbor)
        if neighbor.get_type() == EntityType.MONSTER:
            neighbor.put_asleep()
        else:
            self._handle_normal_collision(neighbor)

    def _handle_upward_collision(self,neighbor):
        Movable._handle_upward_collision(self,neighbor)
        if (
            neighbor.get_type() == EntityType.MONSTER and 
            neighbor.state != MovingState.SLEEPING):
            self.game.set_game_state(GameState.IS_LOST)
        else:
            self._handle_normal_collision(neighbor)

    def _handle_normal_collision(self,neighbor):
        if neighbor.get_type() == EntityType.TREASURE:
            self.game.set_game_state(GameState.IS_WON)
        elif (
            neighbor.get_type() == EntityType.POWERUP and 
            not neighbor.is_used):
            self.powerups.append(neighbor)
            neighbor.is_used = True