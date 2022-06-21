from pygame.time import Clock
from os.path import join
import pygame

from models import Wall,Powerup,Player,Monster,Treasure

from utility import load_sprite, load_font, text_output

from constants_and_states import GameState, Commands, GRID_SIZE

class Game:
    def __init__(self,level_name):
        self.level_name = level_name
        self.clock = Clock()
        self._init_entities()
        self._init_graphics()
        self.game_state = GameState.IN_PROGRESS

    def _init_entities(self):
        self.grid = {}
        self.entities = {}
        self.player = None
        self.monsters = []
        self._load_level()

    def _init_graphics(self):
        screen_size = (self.grid_width*GRID_SIZE,self.grid_height*GRID_SIZE)
        self.back_ground = load_sprite('background',screen_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(f'JumpAndRun level {self.level_name}')
        self.font = load_font()

    def _load_level(self):
        path = join('assets','levels',f'level_{self.level_name}.txt')
        self.grid_width = 0
        self.grid_height = 0
        with open(path,'r') as f:
            x,y = 0,0
            for row in f:
                for col in row:
                    if col == 'X':
                        entity = Wall((x,y),self)
                        self.entities[entity.get_id()] = entity
                        self.grid[x,y] = {entity.get_id()}
                    elif col == 'U':
                        entity = Powerup((x,y),self)
                        self.entities[entity.get_id()] = entity
                        self.grid[x,y] = {entity.get_id()}
                    elif col == 'T':
                        entity = Treasure((x,y),self)
                        self.entities[entity.get_id()] = entity
                        self.grid[x,y] = {entity.get_id()}
                    elif col == 'P':
                        entity = Player((x,y),self)
                        self.entities[entity.get_id()] = entity
                        self.grid[x,y] = {entity.get_id()}
                        self.player = entity
                    elif col == 'M':
                        entity = Monster((x,y),self)
                        self.entities[entity.get_id()] = entity
                        self.grid[x,y] = {entity.get_id()}
                        self.monsters.append(entity)
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
            if self.game_state == GameState.IN_PROGRESS:
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
        for id in self.entities:
            entity = self.entities[id]
            _x = entity.physical_x * GRID_SIZE
            _y = entity.physical_y * GRID_SIZE
            sprite = entity.get_current_sprite()
            self.screen.blit(sprite,(_x,_y))
        if self.game_state == GameState.IS_WON:
            text_output('YOU WIN',self.font,self.screen,(0,255,0))
        elif self.game_state == GameState.IS_LOST:
            text_output('YOU LOSE',self.font,self.screen,(255,0,0))
        pygame.display.flip()

    def _handle_command(self,command):
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
            for id in self.grid[grid_position]:
                yield id 
        return None

    def get_neighborhood(self,grid_position):
        x,y = grid_position
        for dx,dy in [
            (1,0),(1,1),(0,1),(-1,1),
            (-1,0),(-1,-1),(0,-1),(1,-1)]:
            if (x+dx,y+dy) in self.grid:
                for id in self.grid[x+dx,y+dy]:
                    yield self.entities[id]

    def update_grid(self,entity,old_position,new_position):
        """
        Move entity from old_position to new_position.
        """
        if not new_position in self.grid:
            self.grid[new_position] = set()
        self.grid[new_position].add(entity.get_id())
        self.grid[old_position] -= {entity.get_id()}
        if not self.grid[old_position]:
            del self.grid[old_position]
    
    def set_game_state(self,game_state):
        self.game_state = game_state