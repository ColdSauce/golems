from gettext import gettext as _
import scene, game_objects, kbInput, pygame, sys
isLinux = sys.platform.startswith("linux")
if(isLinux):
    try:
        from gi.repository import Gtk
        import sugar3.activity.activity
        from sugar3.graphics.toolbarbox import ToolbarBox
        from sugar3.graphics.toolbarbox import ToolbarButton
        from sugar3.activity.widgets import ActivityToolbarButton
        from sugar3.graphics.toolbutton import ToolButton
        from sugar3.activity.widgets import StopButton
    except ImportError:
        isLinux = False

class CodingScene(scene.Scene):
    def __init__(self, mainChar):
        self.char = mainChar
        self.font = pygame.font.SysFont("couriernew", 24)
        self.keysLastFrame = None
        self.selIndex = 0
        self.selBlock = None
        self.totalArrowCount = 0
        self.totalBlockCount = 0
        self.mode = 0
        self.blockMenu = False
        self.menuIndex = 0
        self.inputIndex = 0
        self.toolbars = [None, None, None, None]
        self.isSugar = False
        
    def enter(self):
        self.mode = 0
        self.blockMenu = False
        self.selIndex = 0
        self.menuIndex = 0
        self.inputIndex = 0
    
    def render(self, surface):
        width, height = surface.get_size()
        surface.fill((0,0,0))
        top = 16
        arrIndex = self.selIndex
        for block in self.char.list_of_bots[0].queue_of_code_blocks:
            top += block.render(surface, 16, top, arrIndex, self.mode)
            arrIndex -= block.getArrowCount()
        if(self.mode == 0 and arrIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(16, top + 1), (16 - 10, top + 6), (16 - 10, top), (16 + 512 + 26, top), (16 + 512 + 26, top + 6), (16 + 512 + 16, top + 1)])
        if(self.blockMenu):
            if(self.isSugar and self.mode == 1):
                pygame.draw.rect(surface, (0, 230, 180), (width - 522, 10, 512, 256))
                top = 25
                if(isinstance(self.selBlock, game_objects.CommentBlock)):
                    menuItem = self.font.render("Comment:", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 477, top))
                    menuItem = self.font.render(self.selBlock.comment, 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 506, top))
                    inWidth, _ = self.font.size(self.selBlock.comment[:self.inputIndex])
                    pygame.draw.line(surface, (0, 0, 0), (width - 506 + inWidth, top), (width - 506 + inWidth, top + 30), 2)
                elif(isinstance(self.selBlock, game_objects.SayBlock)):
                    menuItem = self.font.render("Message:", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 477, top))
                    menuItem = self.font.render(self.selBlock.message, 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 506, top))
                    inWidth, _ = self.font.size(self.selBlock.message[:self.inputIndex])
                    pygame.draw.line(surface, (0, 0, 0), (width - 506 + inWidth, top), (width - 506 + inWidth, top + 30), 2)
                elif(isinstance(self.selBlock, game_objects.IfManaBlock)):
                    menuItem = self.font.render("Req Mana:", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 477, top))
                    menuItem = self.font.render(str(self.selBlock.mthresh), 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 506, top))
                    inWidth, _ = self.font.size(str(self.selBlock.mthresh)[:self.inputIndex])
                    pygame.draw.line(surface, (0, 0, 0), (width - 506 + inWidth, top), (width - 506 + inWidth, top + 30), 2)
                elif(isinstance(self.selBlock, game_objects.IfOwnHealthBlock)):
                    menuItem = self.font.render("Req Health:", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 477, top))
                    menuItem = self.font.render(str(self.selBlock.hthresh), 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 506, top))
                    inWidth, _ = self.font.size(str(self.selBlock.hthresh)[:self.inputIndex])
                    pygame.draw.line(surface, (0, 0, 0), (width - 506 + inWidth, top), (width - 506 + inWidth, top + 30), 2)
            else:
                pygame.draw.rect(surface, (0, 230, 180), (width - 266, 10, 256, 512))
                menuItem = self.font.render("ADD BLOCK", 0, (0, 0, 0), (0, 230, 180))
                top = 25
                surface.blit(menuItem, (width - 200, top))
                if(self.menuIndex == 0):
                    pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                menuItem = self.font.render("MODIFY BLOCK", 0, (0, 0, 0), (0, 230, 180))
                top += 30
                surface.blit(menuItem, (width - 221, top))
                if(self.menuIndex == 1):
                    pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                menuItem = self.font.render("REMOVE BLOCK", 0, (0, 0, 0), (0, 230, 180))
                top += 30
                surface.blit(menuItem, (width - 221, top))
                if(self.menuIndex == 2):
                    pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                top += 30
                pygame.draw.line(surface, (0, 0, 0), (width - 240, top), (width - 26, top), 3)
                top += 5
                if(self.mode == 0):
                    menuItem = self.font.render("ADD BLOCK", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 200, top))
                    top += 30
                    menuItem = self.font.render("Comment", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 3):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("Say", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 4):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("While", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 5):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("If (Mana)", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 6):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("If (Health)", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 7):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 40
                    menuItem = self.font.render("Heal", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 8):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("Fireball", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 9):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("Moss Leech", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 10):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 30
                    menuItem = self.font.render("Douse", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 11):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    top += 40
                    menuItem = self.font.render("End Turn", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 12):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                elif(self.mode == 1):
                    menuItem = self.font.render("MODIFY BLOCK", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    top += 45
                    if(isinstance(self.selBlock, game_objects.CommentBlock)):
                        menuItem = self.font.render("Comment:", 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 221, top))
                        top += 30
                        menuItem = self.font.render(self.selBlock.comment, 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 250, top))
                        if(self.menuIndex == 3):
                            inWidth, _ = self.font.size(self.selBlock.comment[:self.inputIndex])
                            pygame.draw.line(surface, (0, 0, 0), (width - 250 + inWidth, top), (width - 250 + inWidth, top + 30), 2)
                    elif(isinstance(self.selBlock, game_objects.SayBlock)):
                        menuItem = self.font.render("Message:", 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 221, top))
                        top += 30
                        menuItem = self.font.render(self.selBlock.message, 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 250, top))
                        if(self.menuIndex == 3):
                            inWidth, _ = self.font.size(self.selBlock.message[:self.inputIndex])
                            pygame.draw.line(surface, (0, 0, 0), (width - 250 + inWidth, top), (width - 250 + inWidth, top + 30), 2)
                    elif(isinstance(self.selBlock, game_objects.IfManaBlock)):
                        menuItem = self.font.render("Req Mana:", 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 221, top))
                        top += 30
                        menuItem = self.font.render(str(self.selBlock.mthresh), 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 250, top))
                        if(self.menuIndex == 3):
                            inWidth, _ = self.font.size(str(self.selBlock.mthresh)[:self.inputIndex])
                            pygame.draw.line(surface, (0, 0, 0), (width - 250 + inWidth, top), (width - 250 + inWidth, top + 30), 2)
                    elif(isinstance(self.selBlock, game_objects.IfOwnHealthBlock)):
                        menuItem = self.font.render("Req Health:", 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 221, top))
                        top += 30
                        menuItem = self.font.render(str(self.selBlock.hthresh), 0, (0, 0, 0), (0, 230, 180))
                        surface.blit(menuItem, (width - 250, top))
                        if(self.menuIndex == 3):
                            inWidth, _ = self.font.size(str(self.selBlock.hthresh)[:self.inputIndex])
                            pygame.draw.line(surface, (0, 0, 0), (width - 250 + inWidth, top), (width - 250 + inWidth, top + 30), 2)
                elif(self.mode == 2):
                    menuItem = self.font.render("REMOVE BLOCK", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    top += 30
                    if(self.menuIndex == 3):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 148, top), (width - 128, top), (width - 138, top + 12)], 4)
                    else:
                        pygame.draw.polygon(surface, (128, 128, 128), [(width - 148, top), (width - 128, top), (width - 138, top + 12)])
                    top += 20
                    if(self.menuIndex == 4):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 148, top), (width - 128, top), (width - 138, top + 12)], 4)
                    else:
                        pygame.draw.polygon(surface, (128, 128, 128), [(width - 148, top), (width - 128, top), (width - 138, top + 12)])
                    top += 20
                    if(self.menuIndex == 5):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 148, top), (width - 128, top), (width - 138, top + 12)], 4)
                    else:
                        pygame.draw.polygon(surface, (128, 128, 128), [(width - 148, top), (width - 128, top), (width - 138, top + 12)])
                    top += 20
                    menuItem = self.font.render("Yes, Remove!", 0, (0, 0, 0), (0, 230, 180))
                    surface.blit(menuItem, (width - 221, top))
                    if(self.menuIndex == 6):
                        pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, top), (width - 241, top + 24), (width - 235, top + 12)], 4)
                    
    def doKeys(self):
        keys = pygame.key.get_pressed()
        if(self.blockMenu): # Menu is open
        
            if(self.isSugar): # Only do if we're on a Sugar-based System
                if kbInput.isOkayPressed(keys) and not kbInput.isOkayPressed(self.keysLastFrame):
                    self.blockMenu = False
                    self.inputIndex = 0
                elif(isinstance(self.selBlock, game_objects.CommentBlock)):
                    if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                        self.inputIndex = max(self.inputIndex - 1, 0)
                    elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                        self.inputIndex = min(self.inputIndex + 1, len(self.selBlock.comment))
                    newCmmnt, self.inputIndex = kbInput.kbTextInput(keys, self.keysLastFrame, self.selBlock.comment, self.inputIndex)
                    self.selBlock.setComment(newCmmnt)
                elif(isinstance(self.selBlock, game_objects.SayBlock)):
                    if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                        self.inputIndex = max(self.inputIndex - 1, 0)
                    elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                        self.inputIndex = min(self.inputIndex + 1, len(self.selBlock.message))
                    newMsg, self.inputIndex = kbInput.kbTextInput(keys, self.keysLastFrame, self.selBlock.message, self.inputIndex)
                    self.selBlock.setMessage(newMsg)
                elif(isinstance(self.selBlock, game_objects.IfManaBlock)):
                    if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                        self.inputIndex = max(self.inputIndex - 1, 0)
                    elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                        self.inputIndex = min(self.inputIndex + 1, len(str(self.selBlock.mthresh)))
                    newThresh, self.inputIndex = kbInput.kbNumInput(keys, self.keysLastFrame, self.selBlock.mthresh, self.inputIndex)
                    self.selBlock.setThresh(newThresh)
                elif(isinstance(self.selBlock, game_objects.IfOwnHealthBlock)):
                    if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                        self.inputIndex = max(self.inputIndex - 1, 0)
                    elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                        self.inputIndex = min(self.inputIndex + 1, len(str(self.selBlock.hthresh)))
                    newThresh, self.inputIndex = kbInput.kbNumInput(keys, self.keysLastFrame, self.selBlock.hthresh, self.inputIndex)
                    self.selBlock.setThresh(newThresh)
                self.inputIndex = max(self.inputIndex, 0)
                
            else: # Do on a non-Sugar System
                if kbInput.isMenuPressed(keys) and not kbInput.isMenuPressed(self.keysLastFrame):
                    self.blockMenu = False
                    self.menuIndex = 0
                if kbInput.isDownPressed(keys) and not keys[pygame.K_j] and not kbInput.isDownPressed(self.keysLastFrame):
                    self.inputIndex = 0
                    if(self.mode == 0):
                        self.menuIndex = min(self.menuIndex + 1, 12)
                    elif(self.mode == 1):
                        self.menuIndex = min(self.menuIndex + 1, 3)
                    elif(self.mode == 2):
                        self.menuIndex = min(self.menuIndex + 1, 6)
                if kbInput.isUpPressed(keys) and not keys[pygame.K_k] and not kbInput.isUpPressed(self.keysLastFrame):
                    self.inputIndex = 0
                    self.menuIndex = max(self.menuIndex - 1, 0)
                if kbInput.isOkayPressed(keys) and not kbInput.isOkayPressed(self.keysLastFrame):
                    if(self.menuIndex < 3):
                        self.mode = self.menuIndex
                        self.blockMenu = False
                        self.menuIndex = 0
                        self.selIndex = 0
                        self.currentBlockIndex = 0
                    else:
                        if(self.mode == 0):
                            newBlock = None
                            if(self.menuIndex == 3):
                                newBlock = game_objects.CommentBlock()
                            elif(self.menuIndex == 4):
                                newBlock = game_objects.SayBlock()
                            elif(self.menuIndex == 5):
                                newBlock = game_objects.WhileBlock()
                            elif(self.menuIndex == 6):
                                newBlock = game_objects.IfManaBlock()
                            elif(self.menuIndex == 7):
                                newBlock = game_objects.IfOwnHealthBlock()
                            elif(self.menuIndex == 8):
                                newBlock = game_objects.HealBlock(20, 15)
                            elif(self.menuIndex == 9):
                                newBlock = game_objects.FireballBlock(10, 15)
                            elif(self.menuIndex == 10):
                                newBlock = game_objects.MossLeechBlock(10, 15)
                            elif(self.menuIndex == 11):
                                newBlock = game_objects.DouseBlock(10, 15)
                            elif(self.menuIndex == 12):
                                newBlock = game_objects.EndTurnBlock()
                            if(self.insert(newBlock)):
                                self.selIndex += 1
                        elif(self.mode == 2):
                            if(self.menuIndex == 6):
                                self.remove()
                if(self.mode == 1 and self.menuIndex == 3):
                    if(isinstance(self.selBlock, game_objects.CommentBlock)):
                        if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                            self.inputIndex = max(self.inputIndex - 1, 0)
                        elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                            self.inputIndex = min(self.inputIndex + 1, len(self.selBlock.comment))
                        newCmmnt, self.inputIndex = kbInput.kbTextInput(keys, self.keysLastFrame, self.selBlock.comment, self.inputIndex)
                        self.selBlock.setComment(newCmmnt)
                    elif(isinstance(self.selBlock, game_objects.SayBlock)):
                        if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                            self.inputIndex = max(self.inputIndex - 1, 0)
                        elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                            self.inputIndex = min(self.inputIndex + 1, len(self.selBlock.message))
                        newMsg, self.inputIndex = kbInput.kbTextInput(keys, self.keysLastFrame, self.selBlock.message, self.inputIndex)
                        self.selBlock.setMessage(newMsg)
                    elif(isinstance(self.selBlock, game_objects.IfManaBlock)):
                        if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                            self.inputIndex = max(self.inputIndex - 1, 0)
                        elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                            self.inputIndex = min(self.inputIndex + 1, len(str(self.selBlock.mthresh)))
                        newThresh, self.inputIndex = kbInput.kbNumInput(keys, self.keysLastFrame, self.selBlock.mthresh, self.inputIndex)
                        self.selBlock.setThresh(newThresh)
                    elif(isinstance(self.selBlock, game_objects.IfOwnHealthBlock)):
                        if kbInput.isLeftPressed(keys) and not kbInput.isLeftPressed(self.keysLastFrame):
                            self.inputIndex = max(self.inputIndex - 1, 0)
                        elif kbInput.isRightPressed(keys) and not kbInput.isRightPressed(self.keysLastFrame):
                            self.inputIndex = min(self.inputIndex + 1, len(str(self.selBlock.hthresh)))
                        newThresh, self.inputIndex = kbInput.kbNumInput(keys, self.keysLastFrame, self.selBlock.hthresh, self.inputIndex)
                        self.selBlock.setThresh(newThresh)
                    self.inputIndex = max(self.inputIndex, 0)
                    
        else: # Menu is closed
            if kbInput.isBackPressed(keys) and not kbInput.isBackPressed(self.keysLastFrame):
                self.manager.go_to(scene.Scenes.INTERACTIVE)
                self.selIndex = 0
            if kbInput.isDownPressed(keys) and not kbInput.isDownPressed(self.keysLastFrame):
                if(self.mode == 0):
                    self.selIndex = min(self.selIndex + 1, self.totalArrowCount)
                else:
                    self.selIndex = min(self.selIndex + 1, self.totalBlockCount - 1)
            if kbInput.isUpPressed(keys) and not kbInput.isUpPressed(self.keysLastFrame):
                self.selIndex = max(self.selIndex - 1, 0)
            if kbInput.isMenuPressed(keys) and not kbInput.isMenuPressed(self.keysLastFrame): # Won't be touched by Sugar code
                self.blockMenu = True
        self.keysLastFrame = keys
    def insert(self, block):
        if(self.selIndex == 0):  # Insert block at beginning of list
            self.char.list_of_bots[0].queue_of_code_blocks.insert(0, block)
            return True
        elif(self.selIndex == self.totalArrowCount):  # Append block to end of list
            self.char.list_of_bots[0].queue_of_code_blocks.append(block)
            return True
        else:  # Insert somewhere in list
            currArrowIndex = self.selIndex
            for i in range(0, len(self.char.list_of_bots[0].queue_of_code_blocks)):
                if(currArrowIndex == 0):
                    self.char.list_of_bots[0].queue_of_code_blocks.insert(i, block)
                    return True
                elif(self.char.list_of_bots[0].queue_of_code_blocks[i].insert(block, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.char.list_of_bots[0].queue_of_code_blocks[i].getArrowCount()
            print("Failed to insert a new block at insertion point " + str(self.selIndex))
            return False
    def remove(self):
        currSel = self.selIndex
        
        for i in range(0, len(self.char.list_of_bots[0].queue_of_code_blocks)):
            if(currSel == 0):
                del self.char.list_of_bots[0].queue_of_code_blocks[i]
                return True
            elif(self.char.list_of_bots[0].queue_of_code_blocks[i].remove(currSel)):
                return True
            else:
                currSel -= self.char.list_of_bots[0].queue_of_code_blocks[i].getBlockCount()
    def fetch(self):
        currSel = self.selIndex
        
        for i in range(0, len(self.char.list_of_bots[0].queue_of_code_blocks)):
            if(currSel == 0):
                return self.char.list_of_bots[0].queue_of_code_blocks[i]
            rtn = self.char.list_of_bots[0].queue_of_code_blocks[i].fetch(currSel)
            if(rtn != None):
                return rtn
            currSel -= self.char.list_of_bots[0].queue_of_code_blocks[i].getBlockCount()
        return None
    def update(self):
        self.totalArrowCount = 0
        self.totalBlockCount = 0
        for block in self.char.list_of_bots[0].queue_of_code_blocks:
            self.totalArrowCount += block.getArrowCount()
            self.totalBlockCount += block.getBlockCount()
        if(self.mode == 1):
            self.selBlock = self.fetch()
        self.doKeys()
    def handle_events(self, events):
        pass
    def makeToolbar(self, activity):
        self.isSugar = True
        self.toolbars[3] = self.makeModeToolbar(activity)
        self.toolbars[0] = self.makeAddToolbar(activity)
        self.toolbars[1] = self.makeModToolbar(activity)
        self.toolbars[2] = self.makeDelToolbar(activity)
        
        return self.toolbars[0]
        
    def makeModeToolbar(self, activity):
        toolbar = Gtk.Toolbar()
        
        addButton = ToolButton('mode-add')
        addButton.set_tooltip(_('Add Block Mode'))
        addButton.props.accelerator = '<Ctrl>1'
        addButton.connect('clicked', self.enterModeAdd)
        addButton.show()
        
        modButton = ToolButton('mode-mod')
        modButton.set_tooltip(_('Modify Block Mode'))
        modButton.props.accelerator = '<Ctrl>2'
        modButton.connect('clicked', self.enterModeModify)
        modButton.show()
        
        delButton = ToolButton('mode-del')
        delButton.set_tooltip(_('Delete Block Mode'))
        delButton.props.accelerator = '<Ctrl>3'
        delButton.connect('clicked', self.enterModeDelete)
        delButton.show()
        
        toolbar.show()
        
        return toolbar
        
    def enterMode(self, modenum):
        self.mode = modenum
        self.selIndex = 0
        self.currentBlockIndex = 0
        self.activity.set_toolbar_box(self.toolbars[modenum])
        self.toolbars[modenum].show()
    def enterModeAdd(self, button=None):
        self.enterMode(0)
    def enterModeModify(self, button=None):
        self.enterMode(1)
    def enterModeDelete(self, button=None):
        self.enterMode(2)
        
    def makeGenericToolbar(self, activity):
        toolbar = ToolbarBox()
        
        activity_button = ActivityToolbarButton(activity)
        toolbar.toolbar.insert(activity_button, -1)
        activity_button.show()
        
        modebarButton = ToolbarButton(
            page=self.toolbars[3],
            icon_name='toolbar-mode'
        )
        toolbar.toolbar.insert(modebarButton, -1)
        modebarButton.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.toolbar.insert(separator, -1)
        separator.show()
        
        stop_button = StopButton(activity)
        toolbar.toolbar.insert(stop_button, -1)
        stop_button.show()
        
        return toolbar
        
    def makeAddToolbar(self, activity):
        toolbar = self.makeGenericToolbar(activity)
        
        blockbarButton = ToolbarButton(
            page=self.makeBlockToolbar(activity),
            icon_name='toolbar-block'
        )
        toolbar.toolbar.insert(blockbarButton, -4)
        blockbarButton.show()
        
        return toolbar
        
    def makeBlockToolbar(self, activity):
        toolbar = Gtk.Toolbar()
        
        btn = ToolButton('block-comment')
        btn.set_tooltip(_('Add Comment Block'))
        btn.connect('clicked', self.insertBlockComment)
        btn.show()
        
        btn = ToolButton('block-say')
        btn.set_tooltip(_('Add Say Block'))
        btn.connect('clicked', self.insertBlockSay)
        btn.show()
        
        btn = ToolButton('block-while')
        btn.set_tooltip(_('Add While Block'))
        btn.connect('clicked', self.insertBlockWhile)
        btn.show()
        
        btn = ToolButton('block-ifmana')
        btn.set_tooltip(_('Add If-Mana Block'))
        btn.connect('clicked', self.insertBlockIfMana)
        btn.show()
        
        btn = ToolButton('block-ifhealth')
        btn.set_tooltip(_('Add If-Health Block'))
        btn.connect('clicked', self.insertBlockIfHealth)
        btn.show()
        
        btn = ToolButton('block-heal')
        btn.set_tooltip(_('Add Heal Block'))
        btn.connect('clicked', self.insertBlockHeal)
        btn.show()
        
        btn = ToolButton('block-fireball')
        btn.set_tooltip(_('Add Fireball Block'))
        btn.connect('clicked', self.insertBlockFireball)
        btn.show()
        
        btn = ToolButton('block-mossleech')
        btn.set_tooltip(_('Add Moss Leech Block'))
        btn.connect('clicked', self.insertBlockMossLeech)
        btn.show()
        
        btn = ToolButton('block-douse')
        btn.set_tooltip(_('Add Douse Block'))
        btn.connect('clicked', self.insertBlockDouse)
        btn.show()
        
        btn = ToolButton('block-endturn')
        btn.set_tooltip(_('Add End Turn Block'))
        btn.connect('clicked', self.insertBlockEndTurn)
        btn.show()
        
        toolbar.show()
        
        return toolbar
        
    def insertMenu(self, block):
        if(self.insert(block)):
            self.selIndex += 1
    def insertBlockComment(self, button=None):
        insertMenu(game_objects.CommentBlock())
    def insertBlockSay(self, button=None):
        insertMenu(game_objects.SayBlock())
    def insertBlockWhile(self, button=None):
        insertMenu(game_objects.WhileBlock())
    def insertBlockIfMana(self, button=None):
        insertMenu(game_objects.IfManaBlock())
    def insertBlockIfHealth(self, button=None):
        insertMenu(game_objects.IfOwnHealthBlock())
    def insertBlockHeal(self, button=None):
        insertMenu(game_objects.HealBlock(20, 15))
    def insertBlockFireball(self, button=None):
        insertMenu(game_objects.FireballBlock(10, 15))
    def insertBlockMossLeech(self, button=None):
        insertMenu(game_objects.MossLeechBlock(10, 15))
    def insertBlockDouse(self, button=None):
        insertMenu(game_objects.DouseBlock(10, 15))
    def insertBlockEndTurn(self, button=None):
        insertMenu(game_objects.EndTurnBlock())
    
    def makeModToolbar(self, activity):
        toolbar = self.makeGenericToolbar(activity)
        
        btn = ToolButton('block-edit')
        btn.set_tooltip(_('Edit Selected Block'))
        btn.props.accelerator = '<Ctrl>e'
        btn.connect('clicked', self.menuEdit)
        btn.show()
        
        return toolbar
    
    def menuEdit(self, button=None):
        self.blockMenu = True
        
    def makeDelToolbar(self, activity):
        toolbar = self.makeGenericToolbar(activity)
        
        btn = ToolButton('block-delete')
        btn.set_tooltip(_('Delete Selected Block'))
        btn.connect('clicked', self.menuRemove)
        btn.show()
        
        return toolbar
        
    def menuRemove(self, button=None):
        self.remove()
        
        

