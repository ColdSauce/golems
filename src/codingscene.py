import scene, kbInput, pygame

class CodingScene(scene.Scene):
    def __init__(self, mainChar):
        self.char = mainChar
        self.font = pygame.font.SysFont("couriernew", 24)
        self.keysLastFrame = None
        self.currentArrowIndex = 0
        self.totalArrowCount = 0
        self.menuIndex = 0
    def render(self, surface):
        surface.fill((0,0,0))
        top = 16
        arrIndex = self.currentArrowIndex
        for block in self.char.list_of_bots[0].queue_of_code_blocks:
            top += block.render(surface, 16, top, arrIndex) 
            arrIndex -= block.getArrowCount()
    def doKeys(self):
        keys = pygame.key.get_pressed()
        else:
            if kbInput.isBackPressed(keys) and not kbInput.isBackPressed(self.keysLastFrame):
                self.manager.go_to(scene.Scenes.INTERACTIVE)
            if kbInput.isDownPressed(keys) and not kbInput.isDownPressed(self.keysLastFrame):
                self.currentArrowIndex = min(self.currentArrowIndex + 1, self.totalArrowCount - 1)
            if kbInput.isUpPressed(keys) and not kbInput.isUpPressed(self.keysLastFrame):
                self.currentArrowIndex = max(self.currentArrowIndex - 1, 0)
        self.keysLastFrame = keys
    def update(self):
        self.totalArrowCount = 0
        for block in self.char.list_of_bots[0].queue_of_code_blocks:
            self.totalArrowCount += block.getArrowCount()
        self.doKeys()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.width,self.height = event.size
        pass


