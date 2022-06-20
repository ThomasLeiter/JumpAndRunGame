import pygame
from os.path import join

def load_sprite(sprite_name,size):
    path = join('assets','sprites',f'{sprite_name}.png')
    sprite = pygame.image.load(path)
    sprite = pygame.transform.scale(sprite,size)
    sprite.set_colorkey((255,255,255))
    return sprite

class GraphicObject:
    def get_current_sprite(self):
        raise NotImplementedError('Graphic objects should return a sprite.')

class Wall(GraphicObject):
    def __init__(self):
        self.sprite = load_sprite('wall',(40,40))
    def get_current_sprite(self):
        return self.sprite

class Powerup(GraphicObject):
    def __init__(self):
        self.sprite = load_sprite('powerup_green',(40,40))
    def get_current_sprite(self):
        return self.sprite
