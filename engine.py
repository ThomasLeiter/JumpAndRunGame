from pygame.time import Clock
from enum import Enum
from os.path import join
import pygame

from models import Wall,Powerup,Player,Monster
from models import GRID_SIZE
from models import load_sprite

class Commands(Enum):
    STAND_STILL = 0,
    MOVE_RIGHT = 1,
    MOVE_LEFT = 2,
    JUMP = 3

class Game:
    def __init__(self,level_name):
        self.level_name = level_name
        self.clock = Clock()
        self._init_entities()
        self._init_graphics()

    def _init_entities(self):
        self.grid = {}
        self.player = None
        self.monsters = []
        self._load_level()

    def _init_graphics(self):
        screen_size = (self.grid_width*GRID_SIZE,self.grid_height*GRID_SIZE)
        self.back_ground = load_sprite('background',screen_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(f'JumpAndRun level {self.level_name}')

    def _load_level(self):
        path = join('assets','levels',f'level_{self.level_name}.txt')
        self.grid_width = 0
        self.grid_height = 0
        with open(path,'r') as f:
            x,y = 0,0
            for row in f:
                for col in row:
                    if col == 'X':
                        self.grid[x,y] = Wall((x,y),self)
                    elif col == 'U':
                        self.grid[x,y] = Powerup((x,y),self)
                    elif col == 'P':
                        self.grid[x,y] = Player((x,y),self)
                        self.player = self.grid[x,y]
                    elif col == 'M':
                        self.grid[x,y] = Monster((x,y),self)
                        self.monsters.append(self.grid[x,y])
                    x += 1
                y += 1
                self.grid_width = x
                x = 0
            self.grid_height = y+1

    def _update(self):
        delta_time = self.clock.tick() / 1000
        self.player.update(delta_time)
        for monster in self.monsters:
            monster.update(delta_time)
    
    def main_loop(self):
        while True:
            self._handle_inputs()
            self._update()
            self._draw()

    def _handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_RIGHT:
                    self._handle_command(Commands.MOVE_RIGHT)
                elif event.key == pygame.K_LEFT:
                    self._handle_command(Commands.MOVE_LEFT)
                elif event.key == pygame.K_UP:
                    self._handle_command(Commands.JUMP)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self._handle_command(Commands.STAND_STILL)
                elif event.key == pygame.K_LEFT:
                    self._handle_command(Commands.STAND_STILL)

    def _draw(self):
        self.screen.blit(self.back_ground,(0,0))
        for x,y in self.grid:
            entity = self.grid[x,y]
            _x = entity.physical_x * GRID_SIZE
            _y = entity.physical_y * GRID_SIZE
            sprite = self.grid[x,y].get_current_sprite()
            self.screen.blit(sprite,(_x,_y))
        pygame.display.flip()

    def _handle_command(self,command):
        print(f'Handling {command}')
        if command == Commands.STAND_STILL:
            self.player.stand_still()
        elif command == Commands.MOVE_RIGHT:
            self.player.move_right()
        elif command == Commands.MOVE_LEFT:
            self.player.move_left()
        elif command == Commands.JUMP:
            self.player.jump()

    def get_entity(self,grid_position):
        if grid_position in self.grid:
            return self.grid[grid_position]
        return None

    def get_neighborhood(self,grid_position):
        x,y = grid_position
        for dx,dy in [
            (1,0),(1,1),(0,1),(-1,1),
            (-1,0),(-1,-1),(0,-1),(1,-1)]:
            if (x+dx,y+dy) in self.grid:
                yield self.grid[x+dx,y+dy]

    def update_grid(self,old_position,new_position):
        """
        Move entity from old_position to new_position.
        """
        self.grid[new_position] = self.grid[old_position]
        del self.grid[old_position]