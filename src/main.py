import pygame
from worldmap import *
from game_objects import *
from pygame.locals import *
import sys

isLinux = sys.platform.startswith("linux")
if(isLinux):
    from gi.repository import Gtk

class GolemsGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.movable_characters = []
        self.main_player = MovableCharacter("P1",pygame.image.load, ["res/main_player/up.png", "res/main_player/right.png", "res/main_player/down.png", "res/main_player/left.png"], 1, 1)
        self.main_player.change_direction(self.main_player.current_direction, override_opt = True)
        self.movable_characters.append(self.main_player)

    def doKeys(self,char):
        if char.moving: # Player's currently moving, ignore keypresses
            return;
        keys = pygame.key.get_pressed()
        # Use change_direction instead of just changing the
        # variable since it also changes the sprite image
        if isUpPressed(keys):
            char.change_direction(Direction.UP)
            if(not self.map.isSolid(char.gridX, char.gridY - 1)):
                char.moving = True
        elif isRightPressed(keys):
            char.change_direction(Direction.RIGHT)
            if(not self.map.isSolid(char.gridX + 1, char.gridY)):
                char.moving = True
        elif isDownPressed(keys):
            char.change_direction(Direction.DOWN)
            if(not self.map.isSolid(char.gridX, char.gridY + 1)):
                char.moving = True
        elif isLeftPressed(keys):
            char.change_direction(Direction.LEFT)
            if(not self.map.isSolid(char.gridX - 1, char.gridY)):
                char.moving = True
    # run the game loop
    def game_loop(self):
        FPS = 30
        surface = pygame.display.get_surface()
        self.map = Map(30, 15)

        while True:
            surface.fill((0,0,0))
            width, height = surface.get_size()
            self.map.render(surface, self.main_player.gridX * 50 + self.main_player.xOffset, self.main_player.gridY * 50 + self.main_player.yOffset)
            
            for character in self.movable_characters:
                if character.moving:
                    if character == self.main_player:
                        character.move(10)
                        if not character.moving:
                            keys = pygame.key.get_pressed()
                            if isUpPressed(keys):
                                character.change_direction(Direction.UP)
                                if(not self.map.isSolid(character.gridX, character.gridY - 1)):
                                    character.moving = True
                            elif isDownPressed(keys):
                                character.change_direction(Direction.DOWN)
                                if(not self.map.isSolid(character.gridX, character.gridY + 1)):
                                    character.moving = True
                            elif isLeftPressed(keys):
                                character.change_direction(Direction.LEFT)
                                if(not self.map.isSolid(character.gridX - 1, character.gridY)):
                                    character.moving = True
                            elif isRightPressed(keys):
                                character.change_direction(Direction.RIGHT)
                                if(not self.map.isSolid(character.gridX + 1, character.gridY)):
                                    character.moving = True
                    else:
                        character.move()
                surface.blit(character.sprite, ((width / 2) - 25 - (self.main_player.gridX * 50 + self.main_player.xOffset) + (character.gridX * 50 + character.xOffset), (height / 2) - 25 - (self.main_player.gridY * 50 + self.main_player.yOffset) + (character.gridY * 50 + character.yOffset)))

            if(isLinux):
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
            
            self.doKeys(self.main_player)

            pygame.display.update()
            self.clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        stub = 0

    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        stub = 0

def isUpPressed(keys):
    return keys[pygame.K_UP] or keys[pygame.K_KP8]
def isDownPressed(keys):
    return keys[pygame.K_DOWN] or keys[pygame.K_KP2]
def isLeftPressed(keys):
    return keys[pygame.K_LEFT] or keys[pygame.K_KP4]
def isRightPressed(keys):
    return keys[pygame.K_RIGHT] or keys[pygame.K_KP6]

