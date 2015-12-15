import pygame, kbInput, game_objects, scene, uimgr, time, sys
isLinux = sys.platform.startswith("linux")
if(isLinux):
    try:
        from gi.repository import Gtk
        import sugar3.activity.activity
        from sugar3.graphics.toolbarbox import ToolbarBox
        from sugar3.activity.widgets import ActivityToolbarButton
        from sugar3.graphics.toolbutton import ToolButton
        from sugar3.activity.widgets import StopButton
    except ImportError:
        isLinux = False

class BattleScene(scene.Scene):
    
    def __init__(self, char1, char2):
        self.grid = self.makeGrid()
        self.char1 = char1
        self.char2 = char2
        self.startBattle()

        self.UI = uimgr.UIManager()
        
        self.makeStatBox()
        self.updateStatBox()
         
        #testEle = self.UI.UIElement((100,100,250,250),borderColor = (0,255,0))
        #self.UI.addElement(testEle,"test")

        #textTest = self.UI.TextElement((100,100),"This is a test",(255,0,0),30)
        #self.UI.addElement(textTest,"text")
       
    def render(self,surface):
        surface.fill((150,150,150)) # bg color
        pygame.draw.rect(surface,(100,100,100),(0,0,1200,450)) # wall color + size
        surface.blit(self.grid,(0,300))
        
        self.drawBots(surface)
        self.drawStatBox(surface)
        self.UI.render(surface) 
        
    def handle_events(self, events):
        pass

    def update(self, keys, keysLastFrame):
        if kbInput.isUpPressed(keys):
            self.moveBotByDir(self.c1Bots[0],0,1)
            self.moveBotByDir(self.c2Bots[0],0,1)
        elif kbInput.isRightPressed(keys):
            self.moveBotByDir(self.c1Bots[0],1,0)
            self.moveBotByDir(self.c2Bots[0],1,0)
        elif kbInput.isDownPressed(keys):
            self.moveBotByDir(self.c1Bots[0],0,-1)
            self.moveBotByDir(self.c2Bots[0],0,-1)
        elif kbInput.isLeftPressed(keys):
            self.moveBotByDir(self.c1Bots[0],-1,0)
            self.moveBotByDir(self.c2Bots[0],-1,0)

        
    def moveBotByDir(self,bot,xMod,yMod):
        oldX = bot.location[0]
        oldY = bot.location[1]

        x = xMod + oldX
        y = yMod + oldY

        if x > 2: x = 2
        if y > 2: y = 2
        if x < 0: x = 0
        if y < 0: y = 0

        if bot.pOwned is True:
            self.grid1[oldX][oldY] = None
            self.grid1[x][y] = bot
        else:
            self.grid2[oldX][oldY] = None
            self.grid2[x][y] = bot
        bot.location = [x,y]

    def moveToSpace(self,bot,newX,newY):
        x = y = -1
        if bot.location is not None: #if bot has a prev location get its loc. ready
            x = bot.location[0]
            y = bot.location[1]    
        
        if bot.pOwned is True:
            if x is not -1: 
                self.grid1[x][y] = None # remove it from prev. location   
            self.grid1[newX][newY] = bot #add into new space

        else: #same thing for npc bots
            if x is not -1:
                self.grid2[x][y] = None
            self.grid2[newX][newY] = bot
        
        bot.location = [newX,newY] # all bots know their location when in battle
            
    def sendToBattle(self, c1, c2):
        self.char1 = c1
        self.char2 = c2
        startBattle()

    def startBattle(self):
        self.c1Bots = self.char1.list_of_bots
        self.c2Bots = self.char2.list_of_bots
        self.allBots = []
        self.allBots.extend(self.c1Bots)
        self.allBots.extend(self.c2Bots)

        self.c1NB = len(self.c1Bots)
        self.c2NB = len(self.c2Bots) 

        self.grid1 = [[None] * 3 for i in range(3)]
        self.grid2 = [[None] * 3 for i in range(3)]

        #this is just hard coded for a 1v1 fight. We need to write a real function for this later.
        self.moveToSpace(self.c1Bots[0],1,1)
        self.moveToSpace(self.c2Bots[0],1,1)
        
        for bot in self.allBots:
            bot.ready = 0
        pass
        
        
    def showDefeatSplash(self):
        print "Defeated Har Har Har"

    def showVictorySplash(self):
        print "Victorious hyuk hyuk hyuk"

    def testDidLose(self, bot):
        if bot.health <= 0:
            if bot in self.c1Bots:
                self.showDefeatSplash()
            else:
                self.showVictorySplash()

    def nextTurn(self):
        # Readiness increases for all bots.
        for bot in self.allBots:
            bot.ready += bot.speed

        # Determine the fastest bot
        fastestBot = self.allBots[0]
        for bot in self.allBots:
            if bot.ready > fastestBot.ready:
                fastestBot = bot
        slowestBot = self.allBots[map(lambda x: x != fastestBot, self.allBots).index(True)]


        while slowestBot.health > 0 and fastestBot.health > 0:
            print "It's " + fastestBot.name + "'s turn!"
            self.takeAction(fastestBot, slowestBot)
            time.sleep(3)

            print "It's " + slowestBot.name + "'s turn!"
            self.takeAction(slowestBot, fastestBot)
            time.sleep(3)


        self.testDidLose(slowestBot)
        self.testDidLose(fastestBot)
        
    #this is where the CodeBlocks stuff will take place?
    def takeAction(self,ownerBot, opponentBot):
        ownerBot.ready -= ownerBot.speed
        def log(text):
            # textTest = self.UI.TextElement((100,100),text,(255,0,0),30)
            # someTest = self.UI.TextElement((400,100), "some stuff", (255,3,3), 30)
            # self.UI.addElement(textTest,"text")
            # self.UI.addElement(someTest,"text")
            print str(text)

        for cb in ownerBot.queue_of_code_blocks:
            cb.execute(ownerBot, opponentBot, log)

    #This gets called by the renderer, and draws the bots into the proper location on the grid
    def drawBots(self,surface):
        c = (0,255,0)
        c2 = (255,0,255)
        testBot = pygame.Surface((80,80))
        pygame.draw.circle(testBot,c2,(40,40),40)
        testBot.set_colorkey((0,0,0))
       
        baseX = 300
        xInc = 75
        xIncMod = 20
        y0 = 650
        y1 = 575
        y2 = 500
            
        for bot in self.allBots:
            x = bot.location[0]
            y = bot.location[1]
            #print("botX:" + str(x) + ", botY:" + str(y))
            height = y0
            if y is 1: height = y1
            if y is 2: height = y2
           
            xSpec = (2-x)*xIncMod
            if y is 0 : xSpec = 0
            if y is 1 : xSpec = xSpec/2

            xSpec2 = x*xIncMod
            if y is 0 : xSpec2 = 0
            if y is 1 : xSpec2 = xSpec2/2                    
            
            xLoc = None
            if bot.pOwned is True:
                xLoc = baseX+xInc*x+xSpec
                surface.blit(testBot,(xLoc,height))
                
            else:
                xLoc = baseX+370+xInc*x-xSpec2
                surface.blit(testBot,(xLoc,height))
            self.drawHPBar(surface,bot,xLoc,height)

    #end drawBots
    

    def makeStatBox(self):
        #o is our team, t is bot team
        oColor = (255,0,0) 
        tColor = (0,0,255)
        bColor = (0,0,0)
        textColor = (0,0,0) 
        fontSizeL = 30
        fontSize = 20
        padL = 50 #large padding
        pad = 10 #padding

        oNum = len(self.c1Bots)
        tNum = len(self.c2Bots)

        sWidth = 1200
        sHeight = 900

        cWidth = 150
        cHeight = 100
        self.oStatContainer = self.UI.Container((padL,padL,cWidth,cHeight*oNum),bgColor = oColor, borderColor = bColor)
        self.oStatBoxes = []
      
        self.tStatContainer = self.UI.Container((sWidth-cWidth-padL,padL,cWidth,cHeight*tNum),bgColor = tColor, borderColor = bColor)
        self.tStatBoxes = []
        
        for i in range(0,oNum+tNum):
           
            statBox = None
            if i < oNum:     
                statBox = self.UI.Container((pad,pad+20,130,60), bgColor = oColor, borderColor = bColor)
            else:
                statBox = self.UI.Container((pad,pad+20,130,60), bgColor = tColor, borderColor = bColor)

            yOff = 15
            #ORDER of these elements matters for updateStatBox! 
            hp = self.UI.Text((pad,pad),"UPDATEDLATER",textColor,fontSize)
            statBox.addChild(hp)
            
            mp = self.UI.Text((pad,pad*2+yOff),"UPDATEDLATER",textColor,fontSize)
            statBox.addChild(mp)

            name = self.UI.Text((pad,-pad*2),"BOT NAME",textColor,fontSizeL)
            statBox.addChild(name)
            
            if i < oNum:
                self.oStatBoxes.append(statBox) 
                self.oStatContainer.addChild(statBox)
            else:
                self.tStatBoxes.append(statBox)
                self.tStatContainer.addChild(statBox)

    def updateStatBox(self):
        oNum = len(self.c1Bots)
        tNum = len(self.c2Bots)
        
        #update all relevant bot info
        def setTextLabels(bot,statBox):
            hp = statBox[i].child(0)
            hp.setText("Health : "+str(bot.health)+"/"+str(bot.maxHealth))

            mp = statBox[i].child(1)
            mp.setText("Mana : "+str(bot.mana)+"/"+str(bot.maxMana))
       
        #for all players bots
        for i in range(0,oNum):
            bot = self.c1Bots[i]
            statBox = self.oStatBoxes
            setTextLabels(bot,statBox)

        #for all npc bots
        for i in range(0,tNum):
            bot = self.c2Bots[i]
            statBox = self.tStatBoxes
            setTextLabels(bot,statBox)

    def drawStatBox(self,surface):
        self.oStatContainer.render(surface)
        self.tStatContainer.render(surface)

    def drawHPBar(self,surface,bot,x,y):
        bgColor = (0,0,0)
        hpColor = (255,0,0)
        adj = 20 #Horiz adjustment      
        b = 5  #Border 
        w = 40 #Width
        h = 15 #Height

        bgRect = (x+adj-b,y-b,w+b*2,h+b*2)
        hpRect = (x+adj,y,w,h)
        pygame.draw.rect(surface, bgColor, bgRect)
        pygame.draw.rect(surface, hpColor, hpRect)

    #called once in init, the return value is stored in self.grid 
    def makeGrid(self):
        color = (255,0,0)
        color2 = (0,0,255)
        lineW = 12
        nDist = 80
        fDist = nDist * 2 / 3
        h0 = 250
        h1 = 150
        h2 = 75
        h3 = 25
        eMod = 5

        grid = pygame.Surface((400,300))
        rgrid = pygame.Surface((400,300))
        rgFix = pygame.Surface((400,300))
        final = pygame.Surface((1200,900))
        
        #left Grid vertical lines
        pygame.draw.line(grid,color,(nDist,h0+eMod),(2*nDist,h3-eMod),lineW)
        pygame.draw.line(grid,color,(nDist*2,h0),(2*nDist+fDist,h3),lineW)  
        pygame.draw.line(grid,color,(nDist*3,h0),(2*nDist+2*fDist,h3),lineW)
        pygame.draw.line(grid,color,(nDist*4,h0+eMod),(nDist*4,h3-eMod),lineW)
        
        #left grid horiz lines
        pygame.draw.line(grid,color,(nDist,h0),(nDist*4,h0),lineW)
        pygame.draw.line(grid,color,(15+nDist+nDist/3,h1),(nDist*4,h1),lineW)
        pygame.draw.line(grid,color,(15+nDist+nDist/3*2,h2),(nDist*4,h2),lineW)
        pygame.draw.line(grid,color,(nDist*2,h3),(nDist*4,h3),lineW)
                
        #right Grid vertical lines
        pygame.draw.line(rgrid,color2,(nDist,h0+eMod),(2*nDist,h3-eMod),lineW)
        pygame.draw.line(rgrid,color2,(nDist*2,h0),(2*nDist+fDist,h3),lineW)  
        pygame.draw.line(rgrid,color2,(nDist*3,h0),(2*nDist+2*fDist,h3),lineW)
        pygame.draw.line(rgrid,color2,(nDist*4,h0+eMod),(nDist*4,h3-eMod),lineW)
        
        #right grid horiz lines
        pygame.draw.line(rgrid,color2,(nDist,h0),(nDist*4,h0),lineW)
        pygame.draw.line(rgrid,color2,(15+nDist+nDist/3,h1),(nDist*4,h1),lineW)
        pygame.draw.line(rgrid,color2,(15+nDist+nDist/3*2,h2),(nDist*4,h2),lineW)
        pygame.draw.line(rgrid,color2,(nDist*2,h3),(nDist*4,h3),lineW)
        
        rgFix.blit(rgrid,(-50,0))
        rgFix = pygame.transform.flip(rgFix,True,False)
        
        final.blit(rgFix,(550,200))
        final.blit(grid,(200,200))
        final.set_colorkey((0,0,0))
        
        return final
    #End makeGrid
    
    def makeToolbar(self, activity):
        toolbar = ToolbarBox()
        
        activity_button = ActivityToolbarButton(activity)
        toolbar.toolbar.insert(activity_button, -1)
        activity_button.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.toolbar.insert(separator, -1)
        separator.show()
        
        stop_button = StopButton(activity)
        toolbar.toolbar.insert(stop_button, -1)
        stop_button.show()
        
        return toolbar
    #End makeToolbar
