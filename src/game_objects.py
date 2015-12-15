import pygame

class Tile:
    def __init__(self, image, solid = False):
        self.sprite = image
        self.solid = solid

class MovableCharacter:
    def move(self,speed = 2):
        direction = self.current_direction
        if direction == Direction.UP:
            self.yOffset -= speed
        elif direction == Direction.RIGHT:
            self.xOffset += speed
        elif direction == Direction.DOWN:
            self.yOffset += speed
        elif direction == Direction.LEFT:
            self.xOffset -= speed
        if ((direction == Direction.UP or direction == Direction.DOWN) and (self.yOffset % 50 == 0)) or ((direction == Direction.LEFT or direction == Direction.RIGHT) and (self.xOffset % 50 == 0)):
            if(self.yOffset < 0):
                self.gridY -= 1
            elif(self.yOffset > 0):
                self.gridY += 1
            self.yOffset = 0;
            if(self.xOffset < 0):
                self.gridX -= 1
            elif(self.xOffset > 0):
                self.gridX += 1
            self.xOffset = 0;
            self.moving = False;


    def change_direction(self, direction, override_opt = False):
        # Optimization
        if not override_opt and self.current_direction == direction:
            return
        self.current_direction = direction
        name = self.directional_sprites[direction]
        self.sprite = self.load_function(name)

    def __init__(self, name, load_function,list_of_bots, directional_sprites,x=0,y=0, gold=0):
        # for now this is just hard coded
        # placeholder sprite's justgonna be one of the directional sprites
        self.moving = False
        self.load_function = load_function
        self.directional_sprites = directional_sprites
        self.gridX = x
        self.gridY = y
        self.xOffset = 0
        self.yOffset = 0
        self.name = name
        self.gold = gold
        self.current_direction = Direction.UP
        self.list_of_bots = list_of_bots
        
class MainPlayer(MovableCharacter):
    pass

class EnemyPlayer(MovableCharacter):
    def move(self,speed = 2):
        pass # for now.. but implement ai

class Direction:
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3

class Element:
    NONE   = 0
    FIRE   = 1
    EARTH  = 2
    WATER  = 3
    AIR    = 4
#Z- renamed these for code readability, feel free to call them anything in game


class GenericBot:
    def __init__(self, name, sprite, speed=10, health=100,mana=100,element=Element.NONE,spell_xp=dict(),list_of_spells=[],queue_of_code_blocks = list(),pOwned = False):
        self.queue_of_code_blocks = queue_of_code_blocks
        self.name = name
        self.sprite = sprite
        self.baseSpeed = speed 
        self.speed = speed
        self.maxHealth = health
        self.health = health
        self.maxMana = mana
        self.mana = mana
        self.element = element
        self.spell_xp = spell_xp
        self.list_of_spells = list_of_spells
 
        self.pOwned = pOwned #Boolean, 'player owned':
        self.location = None #Gets set once battle begins

    # Let's you change what the string representation of this class is 
    def __repr__(self):
        return "Health: {}  Mana: {}  Speed: {}".format(str(self.health), str(self.mana), str(self.speed))

class Spells:
    def __init__(self, name, mana_cost=25, attack_power=5,multiplier=dict(),accuracy=0.5):
        self.name = name
        self.mana_cost = mana_cost
        self.attack_power = attack_power
        self.multiplier = multiplier
        self.accuracy = accuracy

class CodeBlock(object):
    def __init__(self):
        self.font = pygame.font.SysFont("comicsansms", 24)
    # Renders the Block to the screen.  Should return the total height of the block.
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        raise NotImplementedError
    # Gets the screen height of the block
    def getRenderHeight(self):
        raise NotImplementedError
    # Gets the count of arrow positions within this block (typically only the one after it)
    def getArrowCount(self):
        return 1
    # Gets the total block count within this block (typically just the one)
    def getBlockCount(self):
        return 1
    # Executes the Block, taking into consideration whether or not this is a calc-mana-cost-only dry run.  Should return mana spent in total, or a tuple of (mana total, flag saying 'had hit an End Turn block').
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        pass
    # Inserts a new Block somewhere in the listing.  True if successful, false if failed; block containers should implement something other than "always fail"
    def insert(self, blockToInsert, arrowIndex):
        return False
    # Removes the Block at the specific index inside this Block.  True if successful, false if failed; block containers should implement something other than "always fail"
    def remove(self, index):
        return False
    # Fetch the Block at a given index.
    def fetch(self, index):
        if(index == 0):
            return self
        else:
            return None

# Comment Block.  Does nothing, handy for in-code notes.
class CommentBlock(CodeBlock):
    def __init__(self):
        super(CommentBlock, self).__init__()
        self.comment = "";
        self.cwidth, self.cheight = self.font.size("# ")
        self.fontRender = self.font.render("# ", 0, (0, 0, 0), (190, 255, 190))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (190, 255, 190), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        return 0 # Comment blocks do nothing
    def setComment(self, newComment):
        self.comment = newComment
        self.cwidth, self.cheight = self.font.size("# " + self.comment)
        self.fontRender = self.font.render("# " + self.comment, 0, (0, 0, 0), (190, 255, 190))

# Say Block.  Causes the Golem to say a bit of text.
class SayBlock(CodeBlock):
    def __init__(self):
        super(SayBlock, self).__init__()
        self.message = "";
        self.cwidth, self.cheight = self.font.size("Say \"\"")
        self.fontRender = self.font.render("Say \"\"", 0, (0, 0, 0), (205, 205, 205))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (205, 205, 205), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):

        return 0
    def setMessage(self, newMessage):
        self.message = newMessage
        self.cwidth, self.cheight = self.font.size("Say \"" + self.message + "\"")
        self.fontRender = self.font.render("Say \"" + self.message + "\"", 0, (0, 0, 0), (205, 205, 205))

# While Block.  Performs a task while a condition remains true.
class WhileBlock(CodeBlock):
    def __init__(self):
        super(WhileBlock, self).__init__()
        self.blocks = []
        _, self.cheight = self.font.size("WAAA")
        self.fontRender = self.font.render("Do Forever", 0, (0, 0, 0), (255, 255, 190))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + 196 + 26, yOffset), (xOffset + 196 + 26, yOffset + 6), (xOffset + 196 + 16, yOffset + 1)])
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset + 1, 196, self.cheight + 6))
        heightsum = self.cheight + 8
        selCount = 1
        for block in self.blocks:
            heightsum += block.render(surface, xOffset + 8, yOffset + heightsum, selIndex - selCount, mode)
            if(mode == 0):
                selCount += block.getArrowCount()
            else:
                selCount += block.getBlockCount()
        if(mode == 0 and selIndex == selCount):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + heightsum + 1), (xOffset - 10, yOffset + 6 + heightsum), (xOffset - 10, yOffset + heightsum), (xOffset + 196 + 26, yOffset + heightsum), (xOffset + 196 + 26, yOffset + 6 + heightsum), (xOffset + 196 + 16, yOffset + heightsum + 1)])
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset + 1 + heightsum, 196, self.cheight + 6))
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset + 1, 6, heightsum + self.cheight + 8 - 2))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, 196, heightsum + self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, 196, heightsum + self.cheight + 6), 2)
        return heightsum + self.cheight + 8
    def getArrowCount(self):
        rtn = 2
        for block in self.blocks:
            rtn += block.getArrowCount()
        return rtn
    def getBlockCount(self):
        rtn = 1
        for block in self.blocks:
            rtn += block.getBlockCount()
        return rtn
    def getRenderHeight(self):
        heightsum = self.cheight + 8
        for block in self.blocks:
            heightsum += self.trueBlocks[i].getRenderHeight()
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        for block in self.blocks:
            block.execute(ownerBot,opponentBot, callback)
    def insert(self, blockToInsert, arrowIndex):
        if(arrowIndex == 0):  # Insert before current block
            return False  # Should have been handled by calling function 
        elif(arrowIndex == 1):  # Insert before rest of list
            self.blocks = [blockToInsert] + self.blocks
            return True
        elif(arrowIndex == self.getArrowCount() - 1):  # Insert at end of list
            self.blocks.append(blockToInsert)
            return True
        else:  # Insert into middle of list
            currArrowIndex = arrowIndex - 1;
            for i in range(0, len(self.blocks)):
                if(currArrowIndex == 0):
                    self.blocks.insert(i, blockToInsert)
                    return True
                elif(self.blocks[i].insert(blockToInsert, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.blocks[i].getArrowCount()
            return False
    def remove(self, index):
        if(index == 0):  # Remove current block
            return False  # Should have been handled by calling function
        else:
            currIndex = index - 1;
            for i in range(0, len(self.blocks)):
                if(currIndex == 0):
                    del self.blocks[i]
                    return True
                elif(self.blocks[i].remove(currIndex)):
                    return True
                else:
                    currIndex -= self.blocks[i].getBlockCount()
            return False
    def fetch(self, index):
        if(index == 0):
            return self
        else:
            currIndex = index - 1;
            for i in range(0, len(self.blocks)):
                if(currIndex == 0):
                    return self.blocks[i]
                rtn = self.blocks[i].fetch(currIndex)
                if(rtn != None): return rtn
                currIndex -= self.blocks[i].getBlockCount()
            return None

# For Block.  Performs a task on each Golem being faced.  Do not implement, only doing 1v1 battles atm.
#class ForBlock(CodeBlock):
#    def __init__(self):
#        pass
#    def render(self, surface, xOffset = 0, yOffset = 0):
#        return 0
#    def execute(self, ownerBot, opponentBot, dryRun = False):
#        return 0

# End Turn Block.  Immediately stops the Golem's execution, and ends their turn.
class EndTurnBlock(CodeBlock):
    def __init__(self):
        super(EndTurnBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("End my Turn")
        self.fontRender = self.font.render("End my Turn", 0, (0, 0, 0), (255, 64, 64))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (255, 64, 64), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        return (0, True)

# Branch Block, Mana.  Allows for some decision making based on how much Mana a Golem has in reserve.
class IfManaBlock(CodeBlock):
    def __init__(self):
        super(IfManaBlock, self).__init__()
        self.mthresh = 0
        self.trueBlocks = []
        self.falseBlocks = []
        self.cwidth, self.cheight = self.font.size("If I have more than 999999 Mana")
        self.fontRender = self.font.render("If I have more than 0 Mana", 0, (0, 0, 0), (128, 205, 255))
        self.elseRender = self.font.render("Otherwise", 0, (0, 0, 0), (128, 205, 255))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        heightsum = self.cheight + 8
        selCount = 1
        for i in range(0, len(self.trueBlocks)):
            heightsum += self.trueBlocks[i].render(surface, xOffset + 8, yOffset + heightsum, selIndex - selCount, mode)
            if(mode == 0):
                selCount += self.trueBlocks[i].getArrowCount()
            else:
                selCount += self.trueBlocks[i].getBlockCount()
        if(mode == 0 and selIndex == selCount):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + heightsum + 1), (xOffset - 10, yOffset + 6 + heightsum), (xOffset - 10, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + 6 + heightsum), (xOffset + self.cwidth + 16, yOffset + heightsum + 1)])
        if(mode == 0):
            selCount += 1
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + 1 + heightsum, self.cwidth + 16, self.cheight + 6))
        secondBlitHeight = heightsum
        heightsum += self.cheight + 8
        for i in range(0, len(self.falseBlocks)):
            heightsum += self.falseBlocks[i].render(surface, xOffset + 8, yOffset + heightsum, selIndex - selCount, mode)
            if(mode == 0):
                selCount += self.falseBlocks[i].getArrowCount()
            else:
                selCount += self.falseBlocks[i].getBlockCount()
        if(mode == 0 and selIndex == selCount):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + heightsum + 1), (xOffset - 10, yOffset + 6 + heightsum), (xOffset - 10, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + 6 + heightsum), (xOffset + self.cwidth + 16, yOffset + heightsum + 1)])
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + 1 + heightsum, self.cwidth + 16, self.cheight + 6))
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + 1, 6, heightsum + self.cheight + 8 - 2))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        surface.blit(self.elseRender, (xOffset + 4, yOffset + secondBlitHeight + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, heightsum + self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, heightsum + self.cheight + 6), 2)
        return heightsum + self.cheight + 8
    def getArrowCount(self):
        rtn = 3
        for block in self.trueBlocks:
            rtn += block.getArrowCount()
        for block in self.falseBlocks:
            rtn += block.getArrowCount()
        return rtn
    def getBlockCount(self):
        rtn = 1
        for block in self.trueBlocks:
            rtn += block.getBlockCount()
        for block in self.falseBlocks:
            rtn += block.getBlockCount()
        return rtn
    def getRenderHeight(self):
        heightsum = self.cheight + 8
        for i in range(0, len(self.trueBlocks)):
            heightsum += trueBlocks[i].getRenderHeight()
        heightsum += self.cheight + 8
        for i in range(0, len(self.falseBlocks)):
            heightsum += falseBlocks[i].getRenderHeight()
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        if ownerBot.mana > self.mthresh:
            for t_block in self.trueBlocks:
                t_block.execute(ownerBot, opponentBot,callback)
        else:
            for f_block in self.falseBlocks:
                f_block.execute(ownerBot, opponentBot,callback)
    def insert(self, blockToInsert, arrowIndex):
        if(arrowIndex == 0):  # Insert before current block
            return False  # Should have been handled by calling function 
        else:  # Insert into middle of list
            currArrowIndex = arrowIndex - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currArrowIndex == 0):
                    self.trueBlocks.insert(i, blockToInsert)
                    return True
                elif(self.trueBlocks[i].insert(blockToInsert, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.trueBlocks[i].getArrowCount()
            if(currArrowIndex == 0):  # Insert at end of TrueBlocks
                self.trueBlocks.append(blockToInsert)
                return True
            currArrowIndex -= 1
            for i in range(0, len(self.falseBlocks)):
                if(currArrowIndex == 0):
                    self.falseBlocks.insert(i, blockToInsert)
                    return True
                elif(self.falseBlocks[i].insert(blockToInsert, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.falseBlocks[i].getArrowCount()
            if(currArrowIndex == 0):  # Insert at end of FalseBlocks
                self.falseBlocks.append(blockToInsert)
                return True
            
            return False
    def remove(self, index):
        if(index == 0):  # Remove current block
            return False  # Should have been handled by calling function
        else:
            currIndex = index - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currIndex == 0):
                    del self.trueBlocks[i]
                    return True
                elif(self.trueBlocks[i].remove(currIndex)):
                    return True
                else:
                    currIndex -= self.trueBlocks[i].getBlockCount()
            for i in range(0, len(self.falseBlocks)):
                if(currIndex == 0):
                    del self.falseBlocks[i]
                    return True
                elif(self.falseBlocks[i].remove(currIndex)):
                    return True
                else:
                    currIndex -= self.falseBlocks[i].getBlockCount()
            return False
    def fetch(self, index):
        if(index == 0):
            return self
        else:
            currIndex = index - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currIndex == 0):
                    return self.falseBlocks[i]
                rtn = self.falseBlocks[i].fetch(currIndex)
                if(rtn != None): return rtn
                currIndex -= self.falseBlocks[i].getBlockCount()
            for i in range(0, len(self.falseBlocks)):
                if(currIndex == 0):
                    return self.falseBlocks[i]
                rtn = self.falseBlocks[i].fetch(currIndex)
                if(rtn != None): return rtn
                currIndex -= self.falseBlocks[i].getBlockCount()
            return None

    def setThresh(self, newThresh):
        self.mthresh = newThresh
        self.fontRender = self.font.render("If I have more than " + str(self.mthresh) + " Mana", 0, (0, 0, 0), (128, 205, 255))

# Branch Block, Health.  Allows for some decision making based on how much Health a Golem has.
class IfOwnHealthBlock(CodeBlock):
    def __init__(self):
        super(IfOwnHealthBlock, self).__init__()
        self.hthresh = 0
        self.trueBlocks = []
        self.falseBlocks = []
        self.cwidth, self.cheight = self.font.size("If I have less than 999999 Health")
        self.fontRender = self.font.render("If I have less than 0 Health", 0, (0, 0, 0), (255, 200, 200))
        self.elseRender = self.font.render("Otherwise", 0, (0, 0, 0), (255, 200, 200))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        heightsum = self.cheight + 8
        selCount = 1
        for i in range(0, len(self.trueBlocks)):
            heightsum += self.trueBlocks[i].render(surface, xOffset + 8, yOffset + heightsum, selIndex - selCount, mode)
            if(mode == 0):
                selCount += self.trueBlocks[i].getArrowCount()
            else:
                selCount += self.trueBlocks[i].getBlockCount()
        if(mode == 0 and selIndex == selCount):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + heightsum + 1), (xOffset - 10, yOffset + 6 + heightsum), (xOffset - 10, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + 6 + heightsum), (xOffset + self.cwidth + 16, yOffset + heightsum + 1)])
        if(mode == 0):
            selCount += 1
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + 1 + heightsum, self.cwidth + 16, self.cheight + 6))
        secondBlitHeight = heightsum
        heightsum += self.cheight + 8
        for i in range(0, len(self.falseBlocks)):
            heightsum += self.falseBlocks[i].render(surface, xOffset + 8, yOffset + heightsum, selIndex - selCount, mode)
            if(mode == 0):
                selCount += self.falseBlocks[i].getArrowCount()
            else:
                selCount += self.falseBlocks[i].getBlockCount()
        if(mode == 0 and selIndex == selCount):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + heightsum + 1), (xOffset - 10, yOffset + 6 + heightsum), (xOffset - 10, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + heightsum), (xOffset + self.cwidth + 26, yOffset + 6 + heightsum), (xOffset + self.cwidth + 16, yOffset + heightsum + 1)])
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + 1 + heightsum, self.cwidth + 16, self.cheight + 6))
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + 1, 6, heightsum + self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        surface.blit(self.elseRender, (xOffset + 4, yOffset + secondBlitHeight + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, heightsum + self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, heightsum + self.cheight + 6), 2)
        return heightsum + self.cheight + 8
    def getArrowCount(self):
        rtn = 3
        for block in self.trueBlocks:
            rtn += block.getArrowCount()
        for block in self.falseBlocks:
            rtn += block.getArrowCount()
        return rtn
    def getBlockCount(self):
        rtn = 1
        for block in self.trueBlocks:
            rtn += block.getBlockCount()
        for block in self.falseBlocks:
            rtn += block.getBlockCount()
        return rtn
    def getRenderHeight(self):
        heightsum = self.cheight + 8
        for i in range(0, len(self.trueBlocks)):
            heightsum += self.trueBlocks[i].getRenderHeight()
        heightsum += self.cheight + 8
        for i in range(0, len(self.falseBlocks)):
            heightsum += self.falseBlocks[i].getRenderHeight()
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback,dryRun = False):
        if ownerBot.health < self.hthresh:
            for t_block in self.trueBlocks:
                t_block.execute(ownerBot, opponentBot,callback)
        else:
            for f_block in self.falseBlocks:
                f_block.execute(ownerBot, opponentBot,callback)
    def insert(self, blockToInsert, arrowIndex):
        if(arrowIndex == 0):  # Insert before current block
            return False  # Should have been handled by calling function 
        else:  # Insert into middle of list
            currArrowIndex = arrowIndex - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currArrowIndex == 0):
                    self.trueBlocks.insert(i, blockToInsert)
                    return True
                elif(self.trueBlocks[i].insert(blockToInsert, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.trueBlocks[i].getArrowCount()
            if(currArrowIndex == 0):  # Insert at end of TrueBlocks
                self.trueBlocks.append(blockToInsert)
                return True
            currArrowIndex -= 1
            for i in range(0, len(self.falseBlocks)):
                if(currArrowIndex == 0):
                    self.falseBlocks.insert(i, blockToInsert)
                    return True
                elif(self.falseBlocks[i].insert(blockToInsert, currArrowIndex)):
                    return True
                else:
                    currArrowIndex -= self.falseBlocks[i].getArrowCount()
            if(currArrowIndex == 0):  # Insert at end of FalseBlocks
                self.falseBlocks.append(blockToInsert)
                return True
            
            return False
    def remove(self, index):
        if(index == 0):  # Remove current block
            return False  # Should have been handled by calling function
        else:
            currIndex = index - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currIndex == 0):
                    del self.trueBlocks[i]
                    return True
                elif(self.trueBlocks[i].remove(currIndex)):
                    return True
                else:
                    currIndex -= self.trueBlocks[i].getBlockCount()
            for i in range(0, len(self.falseBlocks)):
                if(currIndex == 0):
                    del self.falseBlocks[i]
                    return True
                elif(self.falseBlocks[i].remove(currIndex)):
                    return True
                else:
                    currIndex -= self.falseBlocks[i].getBlockCount()
            return False
    def fetch(self, index):
        if(index == 0):
            return self
        else:
            currIndex = index - 1;
            for i in range(0, len(self.trueBlocks)):
                if(currIndex == 0):
                    return self.falseBlocks[i]
                rtn = self.falseBlocks[i].fetch(currIndex)
                if(rtn != None): return rtn
                currIndex -= self.falseBlocks[i].getBlockCount()
            for i in range(0, len(self.falseBlocks)):
                if(currIndex == 0):
                    return self.falseBlocks[i]
                rtn = self.falseBlocks[i].fetch(currIndex)
                if(rtn != None): return rtn
                currIndex -= self.falseBlocks[i].getBlockCount()
            return None

    def setThresh(self, newThresh):
        self.hthresh = newThresh
        self.fontRender = self.font.render("If I have less than " + str(self.hthresh) + " Health", 0, (0, 0, 0), (255, 200, 200))

# Heal Block.  Causes the Golem to cast the Heal spell, restoring a certain amount of health not controlled by the program.
class HealBlock(CodeBlock):
    def __init__(self, heal_amount, mana_cost):
        super(HealBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Heal on myself")
        self.mana_cost = mana_cost
        self.heal_amount = heal_amount
        self.fontRender = self.font.render("Cast Heal on myself", 0, (0, 0, 0), (255, 200, 200))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        if dryRun:
            return (ownerBot.mana - self.mana_cost, False)
        callback(ownerBot.name + " healed " + opponentBot.name + " Cost: " + str(self.mana_cost) + " Amount: " + str(self.heal_amount))
        ownerBot.mana -= self.mana_cost
        ownerBot.health = (ownerBot.health + self.heal_amount)
        if ownerBot.health > ownerBot.maxHealth: ownerBot.health = ownerBot.maxHealth  

# Fireball Block.  Causes the Golem to cast Fireball, dealing ignis damage on an opponent.
class FireballBlock(CodeBlock):
    def __init__(self, damage_amount, mana_cost):
        super(FireballBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Fireball at the enemy")
        self.mana_cost = mana_cost
        self.damage_amount = damage_amount
        self.fontRender = self.font.render("Cast Fireball at the enemy", 0, (255, 255, 255), (128, 0, 0))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (128, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        if dryRun:
            return (ownerBot.mana - self.mana_cost, False)

        callback(ownerBot.name + " hit " + opponentBot.name + "w/ a Fireball!" +  " Cost: " + str(self.mana_cost) + " Damage: " + str(self.damage_amount))
        ownerBot.mana -= self.mana_cost
        opponentBot.health -= self.damage_amount

# Moss Leech Block.  Causes the Golem to cast Moss Leech, dealing natura damage on an opponent.
class MossLeechBlock(CodeBlock):
    def __init__(self, damage_amount, mana_cost):
        super(MossLeechBlock, self).__init__()
        self.mana_cost = mana_cost
        self.damage_amount = damage_amount
        self.cwidth, self.cheight = self.font.size("Cast Moss Leech at the enemy")
        self.fontRender = self.font.render("Cast Moss Leech at the enemy", 0, (255, 255, 255), (0, 128, 0))
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (0, 128, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        if dryRun:
            return (ownerBot.mana - self.mana_cost, False)
        callback(ownerBot.name + " moss leeched " + opponentBot.name + "!" + " Cost: " + str(self.mana_cost) + " Damage: " + str(self.damage_amount))
        ownerBot.mana -= self.mana_cost
        opponentBot.health -= self.damage_amount

# Douse Block.  Causes the Golem to cast Douse, dealing aqua damage on an opponent.
class DouseBlock(CodeBlock):
    def __init__(self, damage_amount, mana_cost):
        super(DouseBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Douse at the enemy")
        self.fontRender = self.font.render("Cast Douse at the enemy", 0, (255, 255, 255), (0, 0, 255))
        self.damage_amount = damage_amount
        self.mana_cost = mana_cost
    def render(self, surface, xOffset = 0, yOffset = 0, selIndex = -1, mode = -1):
        if(mode == 0 and selIndex == 0):
            pygame.draw.polygon(surface, (255, 255, 255), [(xOffset, yOffset + 1), (xOffset - 10, yOffset + 6), (xOffset - 10, yOffset), (xOffset + self.cwidth + 26, yOffset), (xOffset + self.cwidth + 26, yOffset + 6), (xOffset + self.cwidth + 16, yOffset + 1)])
        pygame.draw.rect(surface, (0, 0, 255), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        if(mode == 1 and selIndex == 0):
            pygame.draw.rect(surface, (128, 110, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        if(mode == 2 and selIndex == 0):
            pygame.draw.rect(surface, (255, 0, 0), (xOffset, yOffset + 1, self.cwidth + 16, self.cheight + 6), 2)
        return self.cheight + 8
    def getRenderHeight(self):
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, callback, dryRun = False):
        if dryRun:
            return (ownerBot.mana - self.mana_cost, False)
        callback(ownerBot.name + " doused " + opponentBot.name + "!" + " Cost: " + str(self.mana_cost) + " Damage: " + str(self.damage_amount))
        ownerBot.mana -= self.mana_cost
        opponentBot.health -= self.damage_amount

