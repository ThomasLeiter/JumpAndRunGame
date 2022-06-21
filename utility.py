import pygame
from os.path import join

def load_sprite(sprite_name,size):
    path = join('assets','sprites',f'{sprite_name}.png')
    sprite = pygame.image.load(path)
    sprite = pygame.transform.scale(sprite,size)
    sprite.set_colorkey((255,255,255))
    return sprite