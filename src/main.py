import pygame
from worldmap import *
from game_objects import *
from pygame.locals import *
import sys

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
isLinux = sys.platform.startswith("linux")
if(isLinux):
    from gi.repository import Gtk

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

class BattleScene(Scene):
    
    def __init__(self, char1, char2):
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        self.MAIN_CHARACTER_TURN = 0
        self.ENEMY_TURN = 1
        width = SCREEN_WIDTH/4
        height = SCREEN_HEIGHT/2
        self.char1 = char1
        self.char2 = char2
        self.spell_rect1 = self.SpellRect(100,100,width,height,char1, 0)
        self.spell_rect2 = self.SpellRect(200 + width, 100, width,height,char2,0)
        self.ui_rect = self.UIRect(2 * width  + 300, 100, width,height, char1,char2)
        self.grid = self.makeGrid() 
       
    def render(self,surface):
        surface.fill((150,150,150))
        pygame.draw.rect(surface,(100,100,100),(0,0,1200,300))
        surface.blit(self.grid,(0,300))
        #self.spell_rect1.render(surface)
        #self.spell_rect2.render(surface)
        #self.ui_rect.render(surface)
 
    def update(self):
        pass
    
    def handle_events(self, events):
        pass

    class UIRect():
        def __init__(self,x,y,width,height,char1, char2):
            self.MAIN_CHARACTER_TURN = 0
            self.ENEMY_TURN = 1
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.char1 = char1
            self.char2 = char2
            self.rect_color = (255,255,255)
            self.rect = (x,y,width,height)
            self.basic_font = pygame.font.SysFont("comicsansms",30)
            self.p1_amount_codeblocks_executed = 0
            self.p2_amount_codeblocks_executed = 0
            self.lines_to_write = []

            # Implemented __repr__ function which let's you change what is returned from str()
            p1_golem_name = self.basic_font.render(self.char1.list_of_bots[0].name, 1, (255,255,255))

            p1_golem_stats = self.basic_font.render(str(self.char1.list_of_bots[0]),1,(255,255,255))

            p2_golem_name = self.basic_font.render(self.char2.list_of_bots[0].name, 1, (255,255,255))

            p2_golem_stats = self.basic_font.render(str(self.char2.list_of_bots[0]),1,(255,255,255))

            p1_execution_left = self.basic_font.render("Codeblocks used: " + str(self.p1_amount_codeblocks_executed) + "/" + str(self.char1.list_of_bots[0].mana), 1, (255,255,255))

            p2_execution_left = self.basic_font.render("Codeblocks used: " + str(self.p2_amount_codeblocks_executed) + "/" + str(self.char2.list_of_bots[0].mana), 1, (255,255,255))

            which_turn = 0
            whos_turn = self.who_starts(self.char1.list_of_bots[0], self.char2.list_of_bots[0])
            self.lines_to_write = [p1_golem_name, p1_golem_stats, p1_execution_left,p2_golem_name, p2_golem_stats, p2_execution_left]

        # The faster golem starts first
        def who_starts(self, golem1, golem2):
            if golem1.speed > golem2.speed:
                return self.MAIN_CHARACTER_TURN
            return self.ENEMY_TURN

        def render(self, surface):
            pygame.draw.rect(surface, self.rect_color, self.rect,3)
            for index, line in enumerate(self.lines_to_write):
                y_offset = index * 20
                surface.blit(line, (self.x + 5, self.y + 5 + y_offset))

    class SpellRect():

        def __init__(self,x,y,width,height,char, bot_id):
            # bot_id is the index of the bot that you want to get spells from is
            self.bot_id = bot_id
            self.x = x
            self.y = y
            self.height = height
            self.rect = (x, y, width, height)
            self.rect_color = (255,255,255)
            self.char = char

        def render(self,surface):
            pygame.draw.rect(surface, self.rect_color, self.rect, 3)
            # This is really ugly code but it's late at night and I wanna go to sleep so I'll fix it tomorrow :p
            for index, code_block in enumerate(self.char.list_of_bots[self.bot_id].queue_of_code_blocks):
                # Ideally, this should be the height of the codeblock but that's not an attribute of codeblock. I think it should be..
                y_offset = index * 64
                code_block.render(surface, xOffset = self.x, yOffset = self.y + y_offset)

    def next_turn(self):
        # alternates between 0 and 1
        self.ui_rect.whos_turn += 1
        self.ui_rect.whos_turn = self.ui_rect.whos_turn % 2


    #called once in init, the return value is stored in self.grid 
    def makeGrid(self):
        color = (255,0,0)
        color2 = (0,0,255)
        nDist = 80
        fDist = nDist * 2 / 3
        h0 = 250
        h1 = 150
        h2 = 75
        h3 = 25
        
        grid = pygame.Surface((400,300))
       	rgrid = pygame.Surface((400,300))
        rgFix = pygame.Surface((400,300))
        final = pygame.Surface((900,300))
        #left Grid vertical lines
        pygame.draw.line(grid,color,(nDist,h0),(2*nDist,h3),2)
        pygame.draw.line(grid,color,(nDist*2,h0),(2*nDist+fDist,h3),2)  
        pygame.draw.line(grid,color,(nDist*3,h0),(2*nDist+2*fDist,h3),2)
        pygame.draw.line(grid,color,(nDist*4,h0),(nDist*4,h3),2)
        
        #left grid horiz lines
        pygame.draw.line(grid,color,(nDist,h0),(nDist*4,h0),2)
        pygame.draw.line(grid,color,(15+nDist+nDist/3,h1),(nDist*4,h1),2)
        pygame.draw.line(grid,color,(15+nDist+nDist/3*2,h2),(nDist*4,h2),2)
        pygame.draw.line(grid,color,(nDist*2,h3),(nDist*4,h3),2)
                
        #right Grid vertical lines
        pygame.draw.line(rgrid,color2,(nDist,h0),(2*nDist,h3),2)
        pygame.draw.line(rgrid,color2,(nDist*2,h0),(2*nDist+fDist,h3),2)  
        pygame.draw.line(rgrid,color2,(nDist*3,h0),(2*nDist+2*fDist,h3),2)
        pygame.draw.line(rgrid,color2,(nDist*4,h0),(nDist*4,h3),2)
        
        #right grid horiz lines
        pygame.draw.line(rgrid,color2,(nDist,h0),(nDist*4,h0),2)
        pygame.draw.line(rgrid,color2,(15+nDist+nDist/3,h1),(nDist*4,h1),2)
        pygame.draw.line(rgrid,color2,(15+nDist+nDist/3*2,h2),(nDist*4,h2),2)
        pygame.draw.line(rgrid,color2,(nDist*2,h3),(nDist*4,h3),2)
        
        rgFix.blit(rgrid,(-50,0))
        rgFix = pygame.transform.flip(rgFix,True,False)
        
        final.blit(rgFix,(500,0))
        final.blit(grid,(0,0))
        final.set_colorkey((0,0,0))
        
        return final

   

class InteractiveScene(Scene):
    def __init__(self):
        global SCREEN_HEIGHT
        global SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.width = SCREEN_WIDTH
        self.movable_characters = []
        self.map = Map(30, 15)
        self.font = pygame.font.SysFont("couriernew", 24)
        some_test_list = []
        for x in range(0,10):
            some_test_list.append(WhileBlock())
        self.main_player = MainPlayer(name = "P1",
                                      load_function = pygame.image.load,
                                      # The sprite for the bot will just be the up picture for placeholder.."
                                      list_of_bots = [GenericBot("Stefan's Bot", "res/main_player/up.png", queue_of_code_blocks = some_test_list)],
                                      directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"],
                                      x = 1, 
                                      y = 1)
        some_test_list = []
        for x in range(0,10):
            some_test_list.append(SayBlock())
        self.enemy_player = EnemyPlayer(name = "Example AI",
                                        load_function = pygame.image.load,
                                        list_of_bots = [GenericBot("enemy's Bot", "res/main_player/up.png", queue_of_code_blocks = some_test_list)],
                                        directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"], 
                                        x = 2,
                                        y = 2)

        self.main_player.change_direction(self.main_player.current_direction, override_opt = True)
        self.enemy_player.change_direction(self.enemy_player.current_direction, override_opt = True)

        self.movable_characters.append(self.main_player)
        self.movable_characters.append(self.enemy_player)
        
        self.renderMenu = False
        self.keysLastFrame = None
        
        self.menuIndex = 0

    def doKeys(self,char):
        if char.moving: # Player's currently moving, ignore keypresses
            return
        keys = pygame.key.get_pressed()
        if isMenuPressed(keys) and not isMenuPressed(self.keysLastFrame):
            self.renderMenu = not self.renderMenu
        if(self.renderMenu):
            if isUpPressed(keys) and not isUpPressed(self.keysLastFrame):
                pass  # If we have more items, this decrements the menuIndex
            elif isDownPressed(keys) and not isDownPressed(self.keysLastFrame):
                pass  # If we have more items, this increments the menuIndex
            elif isOkayPressed(keys) and not isOkayPressed(self.keysLastFrame):
                self.renderMenu = False
                self.manager.go_to(CodingScene(self.main_player, self))
            elif isBackPressed(keys) and not isBackPressed(self.keysLastFrame):
                self.renderMenu = False
        else:
            # Use change_direction instead of just changing the
            # variable since it also changes the sprite image
            if isUpPressed(keys):
                self.move(char,Direction.UP)
            elif isRightPressed(keys):
                self.move(char,Direction.RIGHT)
            elif isDownPressed(keys):
                self.move(char,Direction.DOWN)
            elif isLeftPressed(keys):
                self.move(char,Direction.LEFT)
        self.keysLastFrame = keys

    def render(self, surface):
        surface.fill((0,0,0))
        self.map.render(surface, self.main_player.gridX * 50 + self.main_player.xOffset, self.main_player.gridY * 50 + self.main_player.yOffset)
        width = self.width
        height = self.height
        for character in self.movable_characters:
            surface.blit(character.sprite, ((width / 2) - 25 - (self.main_player.gridX * 50 + self.main_player.xOffset) + (character.gridX * 50 + character.xOffset), (height / 2) - 25 - (self.main_player.gridY * 50 + self.main_player.yOffset) + (character.gridY * 50 + character.yOffset)))
        if(self.renderMenu):
            pygame.draw.rect(surface, (0, 230, 180), (width - 266, 10, 256, 512))
            menuItemOne = self.font.render("EDIT CODE", 0, (0, 0, 0), (0, 230, 180))
            surface.blit(menuItemOne, (width - 221, 25))
            if(self.menuIndex == 0):
                pygame.draw.polygon(surface, (0, 0, 0), [(width - 241, 25), (width - 241, 49), (width - 235, 37)], 4)

    def what_character_on_tile(self,x,y):
        for character in self.movable_characters:
            if character.gridX == x and character.gridY == y:
                return character
        return None
    
    def collided_with_another_character(self, char1, char2):
        self.manager.go_to(BattleScene(char1,char2))

    def move(self,character,direction):
        xMod = yMod = 0
        character.change_direction(direction)
        if direction is Direction.UP: yMod = -1
        elif direction is Direction.RIGHT: xMod = 1
        elif direction is Direction.DOWN: yMod = 1
        elif direction is Direction.LEFT: xMod = -1
	
        character_at_loc =  self.what_character_on_tile(character.gridX + xMod, character.gridY + yMod) 
        if character_at_loc is not None:
            if character_at_loc is not character: # This will need to be changed once we have multiple things to interact with.
                self.collided_with_another_character(character,character_at_loc)
                return
        if(not self.map.isSolid(character.gridX + xMod, character.gridY + yMod)):
            character.moving = True

    def update(self):
        for character in self.movable_characters:
            if character.moving:
                if character == self.main_player:
                    character.move(10) 
                else:
                    character.move()
        self.doKeys(self.main_player)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.width,self.height = event.size

        pass

class CodingScene(Scene):
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

class MenuScreen(Scene):
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
            print "event is " + str(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "this works"
                self.manager.go_to(InteractiveScene())



class GolemsGame:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
                
        # run the game loop
    def game_loop(self):
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        FPS = 30
        surface = pygame.display.get_surface()
        width, height = surface.get_size()
        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height

        manager = SceneManager()
        while True:
            if(isLinux):
                while Gtk.events_pending():
                    Gtk.main_iteration()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)

            manager.scene.handle_events(events)
            manager.scene.update()
            manager.scene.render(surface)

            pygame.display.update()
            self.clock.tick(FPS)
     
    # Called when loading a saved state from the Journal
    def read_file(self, file_path):
        stub = 0

    # Called when saving a saved state to the Journal
    def write_file(self, file_path):
        stub = 0

def isUpPressed(keys):
    return keys != None and (keys[pygame.K_UP] or keys[pygame.K_KP8] or keys[pygame.K_k])
def isDownPressed(keys):
    return keys != None and (keys[pygame.K_DOWN] or keys[pygame.K_KP2] or keys[pygame.K_j])
def isLeftPressed(keys):
    return keys != None and (keys[pygame.K_LEFT] or keys[pygame.K_KP4] or keys[pygame.K_h])
def isRightPressed(keys):
    return keys != None and (keys[pygame.K_RIGHT] or keys[pygame.K_KP6] or keys[pygame.K_l])
def isOkayPressed(keys): # Okay uses Check on Gamepad. 
    return keys != None and (keys[pygame.K_RETURN] or keys[pygame.K_KP1])
def isBackPressed(keys): # Back uses the X
    return keys != None and (keys[pygame.K_BACKSPACE] or keys[pygame.K_KP3])
def isMenuPressed(keys): # Menu uses the Square.
    return keys != None and (keys[pygame.K_TAB] or keys[pygame.K_KP7])
