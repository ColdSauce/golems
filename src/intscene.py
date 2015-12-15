import pygame, kbInput, game_objects, scene, worldmap

class InteractiveScene(scene.Scene):
    def __init__(self):
        self.movable_characters = []
        self.map = worldmap.Map(30, 15)
        self.font = pygame.font.SysFont("couriernew", 24)
        cmntBlock = game_objects.CommentBlock()
        cmntBlock.setComment("Insert code below.")
        self.main_player = game_objects.MainPlayer(name = "P1",
                                      load_function = pygame.image.load,
                                      # The sprite for the bot will just be the up picture for placeholder.."
                                      list_of_bots = [game_objects.GenericBot("Stefan's Bot", "res/main_player/up.png", pOwned = True, queue_of_code_blocks = [cmntBlock])],
                                      directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"],
                                      x = 1, 
                                      y = 1,
                                      )
        some_test_list = []
        for x in range(0,10):
            some_test_list.append(game_objects.SayBlock())
        
        
        enemyLocations = self.map.getEnemyLocations()
        numEnemies = len(enemyLocations)
        for x in range(0, numEnemies):
            position = enemyLocations[x]
            xLoc = position[0]
            yLoc = position[1]
            self.enemy_player = game_objects.EnemyPlayer(name = "AI-" + str(x),
                                        load_function = pygame.image.load,
                                        list_of_bots = [game_objects.GenericBot("enemy's Bot", "res/main_player/up.png",queue_of_code_blocks = some_test_list,speed=8)],
                                        directional_sprites = ["res/main_player/up.png", 
                                                             "res/main_player/right.png", 
                                                             "res/main_player/down.png", 
                                                             "res/main_player/left.png"], 
                                        x = xLoc,
                                        y = yLoc)
            
            self.enemy_player.change_direction(self.enemy_player.current_direction, override_opt = True)
            self.movable_characters.append(self.enemy_player)

        self.main_player.change_direction(self.main_player.current_direction, override_opt = True)
        self.movable_characters.append(self.main_player)
        
        self.renderMenu = False
        self.keysLastFrame = None
        
        self.menuIndex = 0

    def doKeys(self,char):
        if char.moving: # Player's currently moving, ignore keypresses
            return
        keys = pygame.key.get_pressed()
        if kbInput.isMenuPressed(keys) and not kbInput.isMenuPressed(self.keysLastFrame):
            self.renderMenu = not self.renderMenu
        if(self.renderMenu):
            if kbInput.isUpPressed(keys) and not kbInput.isUpPressed(self.keysLastFrame):
                pass  # If we have more items, this decrements the menuIndex
            elif kbInput.isDownPressed(keys) and not kbInput.isDownPressed(self.keysLastFrame):
                pass  # If we have more items, this increments the menuIndex
            elif kbInput.isOkayPressed(keys) and not kbInput.isOkayPressed(self.keysLastFrame):
                self.renderMenu = False
                self.manager.go_to(scene.Scenes.CODING, plyr = self.main_player)
            elif kbInput.isBackPressed(keys) and not kbInput.isBackPressed(self.keysLastFrame):
                self.renderMenu = False
        else:
            # Use change_direction instead of just changing the
            # variable since it also changes the sprite image
            if kbInput.isUpPressed(keys):
                self.move(char,game_objects.Direction.UP)
            elif kbInput.isRightPressed(keys):
                self.move(char,game_objects.Direction.RIGHT)
            elif kbInput.isDownPressed(keys):
                self.move(char,game_objects.Direction.DOWN)
            elif kbInput.isLeftPressed(keys):
                self.move(char,game_objects.Direction.LEFT)
        self.keysLastFrame = keys

    def render(self, surface):
        surface.fill((0,0,0))
        self.map.render(surface, self.main_player.gridX * 50 + self.main_player.xOffset, self.main_player.gridY * 50 + self.main_player.yOffset)
        width, height = surface.get_size()
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
        self.manager.go_to(scene.Scenes.BATTLE, c1 = char1, c2 = char2)

    def move(self,character,direction):
        xMod = yMod = 0
        character.change_direction(direction)
        if direction is game_objects.Direction.UP: yMod = -1
        elif direction is game_objects.Direction.RIGHT: xMod = 1
        elif direction is game_objects.Direction.DOWN: yMod = 1
        elif direction is game_objects.Direction.LEFT: xMod = -1
	
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
        pass


