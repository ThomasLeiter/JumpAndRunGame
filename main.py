import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game(1)
    game.main_loop()