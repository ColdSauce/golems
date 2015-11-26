import pygame
from src.game_objects import *
from src.main import *

def main():
    pygame.init()
    pygame.display.set_mode((0,0), pygame.RESIZABLE)
    game = GolemsGame()
    game.game_loop()

if __name__ == '__main__':
    main()