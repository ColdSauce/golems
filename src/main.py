import pygame
from game_objects import *

class GolemsGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.movable_characters = []
        self.main_player = MovableCharacter("P1",pygame.image.load, ["res/main_player/up.png", "res/main_player/right.png", "res/main_player/down.png", "res/main_player/left.png"])
        self.main_player.change_direction(self.main_player.current_direction, override_opt = True)
        self.movable_characters.append(self.main_player)

    def keypress_event(self,event,main_player):
        if self.main_player.moving: # Player's currently moving, ignore keypresses
            return;
        # Use change_direction instead of just changing the
        # variable since it also changes the sprite image
        self.main_player.moving = True
        if event.key == pygame.K_UP or event.key == pygame.K_KP8:
            self.main_player.change_direction(Direction.UP)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
            self.main_player.change_direction(Direction.RIGHT)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
            self.main_player.change_direction(Direction.DOWN)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
            self.main_player.change_direction(Direction.LEFT)
        else:
            self.main_player.moving = False # If the player pushed an invalid key, don't move character.
    # run the game loop
    def game_loop(self):
        FPS = 30
        surface = pygame.display.get_surface()

        while True:
            surface.fill((10,10,10))
            width, height = surface.get_size()
            
            # Just some placeholder background / debugging grid show
            for x in range(-1250, 1250, 50):
                for y in range(-950, 950, 50):
                    pygame.draw.circle(surface, (128, 128, 128), ((width / 2) - self.main_player.x + x, (height / 2) - self.main_player.y + y), 4, 0)

            for character in self.movable_characters:
                if character.moving:
                    if character == self.main_player:
                        character.move(5)
                        if not character.moving:
                            keys = pygame.key.get_pressed()
                            if (keys[pygame.K_UP]) or (keys[pygame.K_KP8]):
                                character.change_direction(Direction.UP)
                                character.moving = True
                            elif (keys[pygame.K_DOWN]) or (keys[pygame.K_KP2]):
                                character.change_direction(Direction.DOWN)
                                character.moving = True
                            elif (keys[pygame.K_LEFT]) or (keys[pygame.K_KP4]):
                                character.change_direction(Direction.LEFT)
                                character.moving = True
                            elif (keys[pygame.K_RIGHT]) or (keys[pygame.K_KP6]):
                                character.change_direction(Direction.RIGHT)
                                character.moving = True
                    else:
                        character.move()
                surface.blit(character.sprite, ((width / 2) - self.main_player.x + character.x, (height / 2) - self.main_player.y + character.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    self.keypress_event(event, self.main_player)

            pygame.display.update()
            self.clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        stub = 0

    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        stub = 0

