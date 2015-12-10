import scene, game_objects, kbInput, pygame

class CodingScene(scene.Scene):
    def __init__(self, mainChar):
        self.char = mainChar
        self.font = pygame.font.SysFont("couriernew", 24)
        self.keysLastFrame = None
        self.currentArrowIndex = 0
        self.totalArrowCount = 0
        self.blockMenu = False
        self.menuIndex = 0
        self.height = 900 # help with globals?
        self.width = 1200
    def render(self, surface):
        width, height = (self.width, self.height)
        surface.fill((0,0,0))
        top = 16
        arrIndex = self.currentArrowIndex
        for block in self.char.list_of_bots[0].queue_of_code_blocks:
            top += block.render(surface, 16, top, arrIndex) 
            arrIndex -= block.getArrowCount()
        if(self.blockMenu):
            pygame.draw.rect(surface, (0, 230, 180), (width - 266, 10, 256, 512))
            menuItem = self.font.render("MODIFY BLOCK", 0, (0, 0, 0), (0, 230, 180))
            top = 25
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 0):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            menuItem = self.font.render("REMOVE BLOCK", 0, (0, 0, 0), (0, 230, 180))
            top += 30
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 1):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            pygame.draw.line(surface, (0, 0, 0), (width - 240, top), (width - 26, top), 3)
            top += 5
            menuItem = self.font.render("ADD BLOCK", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 200, top))
            top += 30
            menuItem = self.font.render("Comment", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 2):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("Say", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 3):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("While", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 4):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("If (Mana)", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 5):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("If (Health)", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 6):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 40
            menuItem = self.font.render("Heal", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 7):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("Fireball", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 8):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("Moss Leech", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 9):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 30
            menuItem = self.font.render("Douse", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 10):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
            top += 40
            menuItem = self.font.render("End Turn", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItem, (width - 221, top))
            if(self.menuIndex == 11):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
    def doKeys(self):
        keys = pygame.key.get_pressed()
        if(self.blockMenu):
            if (kbInput.isBackPressed(keys) and not kbInput.isBackPressed(self.keysLastFrame)) or (kbInput.isMenuPressed(keys) and not kbInput.isMenuPressed(self.keysLastFrame)):
                self.blockMenu = False
                self.menuIndex = 0
            if kbInput.isDownPressed(keys) and not kbInput.isDownPressed(self.keysLastFrame):
                self.menuIndex = min(self.menuIndex + 1, 10)
            if kbInput.isUpPressed(keys) and not kbInput.isUpPressed(self.keysLastFrame):
                self.menuIndex = max(self.menuIndex - 1, 0)
            if kbInput.isOkayPressed(keys) and not kbInput.isOkayPressed(self.keysLastFrame):
                if(self.menuIndex == 0):
                    pass # Implement "modify block" later
                elif(self.menuIndex == 1):
                    pass # Implement "remove block" later
                elif(self.menuIndex == 2):
                    self.insert(game_objects.CommentBlock())
                elif(self.menuIndex == 3):
                    self.insert(game_objects.SayBlock())
                elif(self.menuIndex == 4):
                    self.insert(game_objects.WhileBlock())
                elif(self.menuIndex == 5):
                    self.insert(game_objects.IfOwnManaBlock())
                elif(self.menuIndex == 6):
                    self.insert(game_objects.IfOwnHealthBlock())
                elif(self.menuIndex == 7):
                    self.insert(game_objects.HealBlock(20))
                elif(self.menuIndex == 8):
                    self.insert(game_objects.FireballBlock(10))
                elif(self.menuIndex == 9):
                    self.insert(game_objects.MossLeechBlock(10))
                elif(self.menuIndex == 10):
                    self.insert(game_objects.DouseBlock(10))
                elif(self.menuIndex == 11):
                    self.insert(game_objects.EndTurnBlock())
                
        else:
            if kbInput.isBackPressed(keys) and not kbInput.isBackPressed(self.keysLastFrame):
                self.manager.go_to(scene.Scenes.INTERACTIVE)
                self.currentArrowIndex = 0
            if kbInput.isDownPressed(keys) and not kbInput.isDownPressed(self.keysLastFrame):
                self.currentArrowIndex = min(self.currentArrowIndex + 1, self.totalArrowCount - 1)
            if kbInput.isUpPressed(keys) and not kbInput.isUpPressed(self.keysLastFrame):
                self.currentArrowIndex = max(self.currentArrowIndex - 1, 0)
            if kbInput.isMenuPressed(keys) and not kbInput.isMenuPressed(self.keysLastFrame):
                self.blockMenu = True
        self.keysLastFrame = keys
    def insert(self, block):
        if(self.currentArrowIndex == 0):  # Insert block at beginning of list
            self.char.list_of_bots[0].queue_of_code_blocks.append(block)
        else:  # Insert somewhere in list
            currArrowIndex = self.currentArrowIndex - 1
            for i in range(0, len(self.char.list_of_bots[0].queue_of_code_blocks)):
                if(currArrowIndex == 0):
                    self.char.list_of_bots[0].queue_of_code_blocks.insert(i, blockToInsert)
                    return
                elif(self.char.list_of_bots[0].queue_of_code_blocks[i].insert(blockToInsert, currArrowIndex)):
                    return
                else:
                    currArrowIndex -= self.char.list_of_bots[0].queue_of_code_blocks[i].getArrowCount()
            return False
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


