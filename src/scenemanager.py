class SceneManager():
    def __init__(self):
        self.go_to(MenuScreen())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class Scene():
    def __init__(self):
        pass

    def render(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


