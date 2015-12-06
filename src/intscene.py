import pygame, kbInput, game_objects

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
                                      list_of_bots = [GenericBot("Stefan's Bot", "res/main_player/up.png", pOwned = True, queue_of_code_blocks = some_test_list)],
                                      directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"],
                                      x = 1, 
                                      y = 1,
                                      )
        some_test_list = []
        for x in range(0,10):
            some_test_list.append(SayBlock())
        self.enemy_player = EnemyPlayer(name = "Example AI",
                                        load_function = pygame.image.load,
                                        list_of_bots = [GenericBot("enemy's Bot", "res/main_player/up.png",queue_of_code_blocks = some_test_list,speed=8)],
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


