import pygame
from worldmap import *
from game_objects import *
from pygame.locals import *
import sys

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
isLinux = sys.platform.startswith("linux")
if(isLinux):
    from gi.repository import Gtk

class SceneManager():
    def __init__(self):
        self.go_to(MenuScreen())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class Scene():
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class InteractiveScene(Scene):
    def __init__(self):
        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.width = SCREEN_WIDTH
        self.movable_characters = []
        self.map = Map(30, 15)
        self.main_player = MainPlayer(name = "P1",
                                      load_function = pygame.image.load,
                                      directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"],
                                      x = 1, 
                                      y = 1)
        self.enemy_player = EnemyPlayer(name = "Example AI",
                                        load_function = pygame.image.load,
                                        directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"], 
                                        x = 2,
                                        y = 2)

        self.main_player.change_direction(self.main_player.current_direction, override_opt = True)
        self.enemy_player.change_direction(self.enemy_player.current_direction, override_opt = True)

        self.movable_characters.append(self.main_player)
        self.movable_characters.append(self.enemy_player)

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

    def render(self, surface):
        surface.fill((0,0,0))
        self.map.render(surface, self.main_player.gridX * 50 + self.main_player.xOffset, self.main_player.gridY * 50 + self.main_player.yOffset)
        width = self.width
        height = self.height
        for character in self.movable_characters:
            surface.blit(character.sprite, ((width / 2) - 25 - (self.main_player.gridX * 50 + self.main_player.xOffset) + (character.gridX * 50 + character.xOffset), (height / 2) - 25 - (self.main_player.gridY * 50 + self.main_player.yOffset) + (character.gridY * 50 + character.yOffset)))

    def update(self):
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

        self.doKeys(self.main_player)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.width,self.height = event.size

        pass

class MenuScreen(Scene):
    def __init__(self):
        self.font_color = (200,200,200)
        self.font = pygame.font.SysFont("comicsansms", 500)
        self.label = self.font.render("Play!", 1, self.font_color)
    def render(self, surface):
        surface.fill((0,0,0))
        surface.blit(self.label, (100,100))
    def update(self):
        pass
    def handle_events(self,events):
        for event in events:
            print "event is " + str(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "this works"
                self.manager.go_to(InteractiveScene())



class GolemsGame:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
                
        # run the game loop
    def game_loop(self):
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        FPS = 30
        surface = pygame.display.get_surface()
        width, height = surface.get_size()
        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height

        manager = SceneManager()
        while True:

            if(isLinux):
                while Gtk.events_pending():
                    Gtk.main_iteration()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)

            manager.scene.handle_events(events)
            manager.scene.update()
            manager.scene.render(surface)

            pygame.display.update()
            self.clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        stub = 0

    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        stub = 0

def isUpPressed(keys):
    return keys[pygame.K_UP] or keys[pygame.K_KP8] or keys[pygame.K_k]
def isDownPressed(keys):
    return keys[pygame.K_DOWN] or keys[pygame.K_KP2] or keys[pygame.K_j]
def isLeftPressed(keys):
    return keys[pygame.K_LEFT] or keys[pygame.K_KP4] or keys[pygame.K_h]
def isRightPressed(keys):
    return keys[pygame.K_RIGHT] or keys[pygame.K_KP6] or keys[pygame.K_l]

