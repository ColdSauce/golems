class Scene():  
    def __init__(self):
        pass

    def render(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class Scenes:
    MENU = 0
    INTERACTIVE = 1
    BATTLE = 2
    CODING = 3

    #update this with addition of new scenes!
    NUMSCENES = 4
