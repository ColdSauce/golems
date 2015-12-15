import sys
isLinux = sys.platform.startswith("linux")
if(isLinux):
    from gi.repository import Gtk
    import sugar3.activity.activity
    from sugar3.graphics.toolbarbox import ToolbarBox
    from sugar3.activity.widgets import ActivityToolbarButton
    from sugar3.graphics.toolbutton import ToolButton
    from sugar3.activity.widgets import StopButton

class Scene():  
    def __init__(self):
        pass

    def render(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
        
    def makeToolbar(self, activity):
        " Creates the Toolbar for the Sugar Activity "
        toolbar = ToolbarBox()
        
        activity_button = ActivityToolbarButton(activity)
        toolbar.toolbar.insert(activity_button, -1)
        activity_button.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.toolbar.insert(separator, -1)
        separator.show()
        
        stop_button = StopButton(self)
        toolbar.toolbar.insert(stop_button, -1)
        stop_button.show()
        
        return toolbar

class Scenes:
    MENU = 0
    INTERACTIVE = 1
    BATTLE = 2
    CODING = 3

    #update this with addition of new scenes!
    NUMSCENES = 4
