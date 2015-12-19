import pygame
import sys
import scenemanager

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
isLinux = sys.platform.startswith("linux")
if(isLinux):
    try:
        from gi.repository import Gtk
    except ImportError:
        isLinux = False

   
class GolemsGame:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.activity = None
                
        # run the game loop
    def game_loop(self, editmodeButton = None):
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        FPS = 30
        surface = pygame.display.get_surface()
        width, height = surface.get_size()
        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height

        manager = scenemanager.SceneManager()
        
        if(self.activity != None):
            manager.activity = self.activity
            
        keysLastFrame = pygame.key.get_pressed();
        
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

            keys = pygame.key.get_pressed()
            
            manager.scene.handle_events(events)
            manager.scene.update(keys, keysLastFrame)
            manager.scene.render(surface)
            
            keysLastFrame = keys[:]

            pygame.display.update()
            self.clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        stub = 0

    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        stub = 0


