from gettext import gettext as _

import pygame, sys
from src.game_objects import *
from src.main import *
from pygame.locals import *
isLinux = sys.platform.startswith("linux")
if(isLinux):
    try:
        from gi.repository import Gtk
    
        import sugar3.activity.activity
        from sugar3.graphics.toolbarbox import ToolbarBox
        from sugar3.activity.widgets import ActivityToolbarButton
        from sugar3.graphics.toolbutton import ToolButton
        from sugar3.activity.widgets import StopButton
        
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
                
            # Create the Sugar Toolbar.
            def buildToolbar(self):
                toolbar_box = ToolbarBox()
                self.set_toolbar_box(toolbar_box)
                toolbar_box.show()
        
                activity_button = ActivityToolbarButton(self)
                toolbar_box.toolbar.insert(activity_button, -1)
                activity_button.show()
        
                # Creating a button:
                editmode = ToolButton('edit-description')
                editmode.set_tooltip(_("Enter Edit Mode"))
                editmode.set_accelerator(_('<ctrl>e'))
                #stop_play.connect('clicked', self._stop_play_cb)
                editmode.show()
        
                toolbar_box.toolbar.insert(editmode, -1)
        
                # Blank space (separator):
                separator = Gtk.SeparatorToolItem()
                separator.props.draw = False
                separator.set_expand(True)
                toolbar_box.toolbar.insert(separator, -1)
                separator.show()
        
                # Creating the "exit activity" button:
                stop_button = StopButton(self)
                toolbar_box.toolbar.insert(stop_button, -1)
                stop_button.show()
                
                return toolbar_box
            # Loading saved state from the Journal
            def read_file(self, file_path):
                self.gameInstance.read_file(file_path)
        
            # Writing saved state to the Journal
            def write_file(self, file_path):
                self.gameInstance.write_file(file_path)

    except ImportError:
        isLinux = False;

def main():
    pygame.init()
    pygame.display.set_mode((1200,900), pygame.RESIZABLE) # 1200,900 is the XO's screen resolution.
    game = GolemsGame()
    game.game_loop()

if __name__ == '__main__':
    main()
