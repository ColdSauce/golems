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
        self.speed = speed
        self.health = health
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
        self.font = pygame.font.SysFont("comicsansms", 30)
    # Renders the Block to the screen.  Should return the total height of the block.
    def render(self, surface, xOffset = 0, yOffset = 0):
        raise NotImplementedError
    # Executes the Block, taking into consideration whether or not this is a calc-mana-cost-only dry run.  Should return mana spent in total, or a tuple of (mana total, flag saying 'had hit an End Turn block').
    def execute(self, ownerBot, opponentBot, dryRun = False):
        raise NotImplementedError

# Comment Block.  Does nothing, handy for in-code notes.
class CommentBlock(CodeBlock):
    def __init__(self):
        super(CommentBlock, self).__init__()
        self.comment = "";
        self.cwidth, self.cheight = self.font.size("# ")
        self.fontRender = self.font.render("# ", 0, (0, 0, 0), (190, 255, 190))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (190, 255, 190), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
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
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (205, 205, 205), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
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
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset, 128, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        heightsum = self.cheight + 8
        for block in self.blocks:
            heightsum += block.render(surface, xOffset + 8, yOffset + heightsum)
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset + heightsum, 128, self.cheight + 8))
        pygame.draw.rect(surface, (255, 255, 190), (xOffset, yOffset, 6, heightsum))
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0

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
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (255, 64, 64), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return (0, True)

# Branch Block, Mana.  Allows for some decision making based on how much Mana a Golem has in reserve.
class IfManaBlock(CodeBlock):
    def __init__(self):
        super(IfManaBlock, self).__init__()
        self.mthresh = 0
        self.trueBlocks = []
        self.falseBlocks = []
        self.cwidth, self.cheight = self.font.size("If I have more than 9999 Mana")
        self.fontRender = self.font.render("If I have more than 0 Mana", 0, (0, 0, 0), (128, 205, 255))
        self.elseRender = self.font.render("Otherwise", 0, (0, 0, 0), (128, 205, 255))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        heightsum = self.cheight + 8
        for i in range(0, size(trueBlocks)):
            heightsum += trueBlocks[i].render(surface, xOffset + 8, yOffset + heightsum)
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + heightsum, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.elseRender, (xOffset + 4, yOffset + heightsum + 4))
        heightsum += self.cheight + 8
        for i in range(0, size(elseBlocks)):
            heightsum += falseBlocks[i].render(surface, xOffset + 8, yOffset + heightsum)
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset + heightsum, self.cwidth + 16, self.cheight + 8))
        pygame.draw.rect(surface, (128, 205, 255), (xOffset, yOffset, 6, heightsum))
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0
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
        self.cwidth, self.cheight = self.font.size("If I have less than 9999 Health")
        self.fontRender = self.font.render("If I have less than 0 Health", 0, (0, 0, 0), (255, 200, 200))
        self.elseRender = self.font.render("Otherwise", 0, (0, 0, 0), (255, 200, 200))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        heightsum = self.cheight + 8
        for i in range(0, size(trueBlocks)):
            heightsum += trueBlocks[i].render(surface, xOffset + 8, yOffset + heightsum)
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + heightsum, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.elseRender, (xOffset + 4, yOffset + heightsum + 4))
        heightsum += self.cheight + 8
        for i in range(0, size(elseBlocks)):
            heightsum += falseBlocks[i].render(surface, xOffset + 8, yOffset + heightsum)
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset + heightsum, self.cwidth + 16, self.cheight + 8))
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset, 6, heightsum))
        return heightsum + self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0
    def setThresh(self, newThresh):
        self.hthresh = newThresh
        self.fontRender = self.font.render("If I have less than " + str(self.hthresh) + " Health", 0, (0, 0, 0), (255, 200, 200))

# Heal Block.  Causes the Golem to cast the Heal spell, restoring a certain amount of health not controlled by the program.
class HealBlock(CodeBlock):
    def __init__(self):
        super(HealBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Heal on myself")
        self.fontRender = self.font.render("Cast Heal on myself", 0, (0, 0, 0), (255, 200, 200))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (255, 200, 200), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0

# Fireball Block.  Causes the Golem to cast Fireball, dealing ignis damage on an opponent.
class FireballBlock(CodeBlock):
    def __init__(self):
        super(FireballBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Fireball at the enemy")
        self.fontRender = self.font.render("Cast Fireball at the enemy", 0, (255, 255, 255), (128, 0, 0))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (128, 0, 0), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0

# Moss Leech Block.  Causes the Golem to cast Moss Leech, dealing natura damage on an opponent.
class MossLeechBlock(CodeBlock):
    def __init__(self):
        super(MossLeechBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Moss Leech at the enemy")
        self.fontRender = self.font.render("Cast Moss Leech at the enemy", 0, (255, 255, 255), (0, 128, 0))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (0, 128, 0), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0

# Douse Block.  Causes the Golem to cast Douse, dealing aqua damage on an opponent.
class DouseBlock(CodeBlock):
    def __init__(self):
        super(DouseBlock, self).__init__()
        self.cwidth, self.cheight = self.font.size("Cast Douse at the enemy")
        self.fontRender = self.font.render("Cast Douse at the enemy", 0, (255, 255, 255), (0, 0, 255))
    def render(self, surface, xOffset = 0, yOffset = 0):
        pygame.draw.rect(surface, (0, 0, 255), (xOffset, yOffset, self.cwidth + 16, self.cheight + 8))
        surface.blit(self.fontRender, (xOffset + 4, yOffset + 4))
        return self.cheight + 8
    def execute(self, ownerBot, opponentBot, dryRun = False):
        return 0

