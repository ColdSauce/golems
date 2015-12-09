import scene, pygame

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
    def handle_events(self,events):
        for event in events:
            #print("event is " + str(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "this works"
                self.manager.go_to(scene.Scenes.INTERACTIVE)
            elif event.type == pygame.VIDEORESIZE:
                self.width,self.height = event.size


