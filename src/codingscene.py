import scene, pygame

class CodingScene(scene.Scene):
    def __init__(self, mainChar, mainScene):
        self.char = mainChar
        self.font = pygame.font.SysFont("couriernew", 24)
        self.rtnScene = mainScene
        self.keysLastFrame = None
    def render(self, surface):
        surface.fill((0,0,0))
        surface.blit(self.font.render("WIP", 0, (255, 255, 255), (0, 0, 0)), (25, 25))
    def doKeys(self):
        keys = pygame.key.get_pressed()
        if isBackPressed(keys) and not isBackPressed(self.keysLastFrame):
            self.manager.go_to(self.rtnScene)
        self.keysLastFrame = keys
    def update(self):
        self.doKeys()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.width,self.height = event.size
        pass


