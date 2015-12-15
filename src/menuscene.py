import scene, pygame, sys
isLinux = sys.platform.startswith("linux")
if(isLinux):
    from gi.repository import Gtk
    import sugar3.activity.activity
    from sugar3.graphics.toolbarbox import ToolbarBox
    from sugar3.activity.widgets import ActivityToolbarButton
    from sugar3.graphics.toolbutton import ToolButton
    from sugar3.activity.widgets import StopButton

class MenuScene(scene.Scene):
    def __init__(self):
        self.font_color = (200,200,200)
        self.font = pygame.font.SysFont("comicsansms", 500)
        self.label = self.font.render("Play!", 1, self.font_color)
    def render(self, surface):
        surface.fill((0,0,0))
        surface.blit(self.label, (100,100))
    def update(self):
        pass
    def handle_events(self, events):
        for event in events:
            #print("event is " + str(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "this works"
                self.manager.go_to(scene.Scenes.INTERACTIVE)
    def makeToolbar(self, activity):
        toolbar = ToolbarBox()
        
        activity_button = ActivityToolbarButton(activity)
        toolbar.toolbar.insert(activity_button, -1)
        activity_button.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.toolbar.insert(separator, -1)
        separator.show()
        
        stop_button = StopButton(activity)
        toolbar.toolbar.insert(stop_button, -1)
        stop_button.show()
        
        return toolbar