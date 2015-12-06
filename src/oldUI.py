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



