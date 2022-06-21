import pygame
from os.path import join

def load_sprite(sprite_name,size):
    path = join('assets','sprites',f'{sprite_name}.png')
    sprite = pygame.image.load(path)
    sprite = pygame.transform.scale(sprite,size)
    sprite.set_colorkey((255,255,255))
    return sprite

def load_font(font_name='freesansbold.ttf',size=64):
    return pygame.font.Font(font_name, size)

def text_output(message,font,surface,color):
    msg = font.render(message,True,color,(255,255,255))
    msg.set_colorkey((255,255,255))
    sx,sy = surface.get_size()
    mx,my = msg.get_size()
    x,y = (sx-mx)/2,(sy-my)/2
    surface.blit(msg,(x,y))
