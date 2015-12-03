import pygame
from src.game_objects import *
from src.main import *

def main():
    pygame.init()
    pygame.display.set_mode((1200,900), pygame.RESIZABLE) # 1200,900 is the XO's screen resolution.
    game = GolemsGame()
    game.game_loop()

if __name__ == '__main__':
    main()
