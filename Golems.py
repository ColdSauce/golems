from gettext import gettext as _

import pygame, sys
from src.game_objects import *
from src.main import *
from pygame.locals import *
try:
    import sugar3.activity.activity
    
    import sugargame.canvas

    class GolemsActivity(sugar3.activity.activity.Activity):
        def __init__(self, actHandle):
            super(GolemsActivity, self).__init__(actHandle)
    
            # Build the Pygame canvas.
            self._pycanvas = sugargame.canvas.PygameCanvas(self)
    
            # Create the game instance.
            self.gameInstance = GolemsGame()
    
            # Allow for creation of Sugar Toolbars.
            self.gameInstance.activity = self
            
        # Loading saved state from the Journal
        def read_file(self, file_path):
            self.gameInstance.read_file(file_path)
    
        # Writing saved state to the Journal
        def write_file(self, file_path):
            self.gameInstance.write_file(file_path)

except ImportError:
    print("We had issue importing Sugar Stuff.  We might not be on Sugar?")

def main():
    pygame.init()
    pygame.display.set_mode((1200,900), pygame.RESIZABLE) # 1200,900 is the XO's screen resolution.
    game = GolemsGame()
    game.game_loop()

if __name__ == '__main__':
    main()
