import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game(2)
    game.main_loop()