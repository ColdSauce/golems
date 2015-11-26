import pygame
from game_objects import *
from pygame.locals import *

class Map:
    def __init__(self):
        self.wall = Tile(pygame.image.load("res/map/wall.png"), True)
        self.floor = Tile(pygame.image.load("res/map/floor.png"))
        self.map = []
        for y in range(0, 25):
            row = []
            if(y == 0 or y == 24):
                for x in range(0, 25):
                    row.append(self.wall)
            else:
                row.append(self.wall)
                for x in range(0, 23):
                    row.append(self.floor)
                row.append(self.wall)
            self.map.append(row)
    
    def isSolid(self, x, y):
        return self.map[y][x].solid
    
    def render(self, surface, xOffset, yOffset):
        width, height = surface.get_size()
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[y])):
                surface.blit(self.map[y][x].sprite, ((width / 2) - 25 - xOffset + (x * 50), (height / 2) - 25 - yOffset + (y * 50)))