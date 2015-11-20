import pygame
from gi.repository import Gtk
from game_objects import *

class GolemsGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.movable_characters = []
        self.main_player = MovableCharacter("P1",pygame.image.load, ["res/main_player/up.png", "res/main_player/right.png", "res/main_player/down.png", "res/main_player/left.png"])
        self.main_player.change_direction(main_player.current_direction, override_opt = True)
        movable_characters.append(main_player)

    def keypress_event(event,main_player):
        if self.main_player.moving: # Player's currently moving, ignore keypresses
            return;
        # Use change_direction instead of just changing the
        # variable since it also changes the sprite image
        self.main_player.moving = True
        if event.key == K_UP or event.key == K_KP8:
            self.main_player.change_direction(Direction.UP)
        elif event.key == K_RIGHT or event.key == K_KP6:
            self.main_player.change_direction(Direction.RIGHT)
        elif event.key == K_DOWN or event.key == K_KP2:
            self.main_player.change_direction(Direction.DOWN)
        elif event.key == K_LEFT or event.key == K_KP4:
            self.main_player.change_direction(Direction.LEFT)
        else:
            self.main_player.moving = False # If the player pushed an invalid key, don't move character.
    # run the game loop
    def game_loop():
        FPS = 30
        surface = pygame.display.get_surface()

        while True:
            surface.fill((10,10,10))
            
            # Just some placeholder background / debugging grid show
            for x in range(0, 1250, 50):
                for y in range(0, 950, 50):
                    pygame.draw.circle(surface, (128, 128, 128), (x, y), 4, 0)

            for character in self.movable_characters:
                if character.moving:
                    character.move()
                    
                surface.blit(character.sprite, (character.x, character.y))

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    keypress_event(event, main_player)

            pygame.display.update()
            clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        #stub
        
    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        #stub

