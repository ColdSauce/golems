import menuscene, battlescene, intscene, codingscene, scene

class SceneManager():

    def __init__(self):
        # initialized the scene array to empty values.
        self.activity = None
        self.scenes = []
        self.toolbars = []
        for i in range(scene.Scenes.NUMSCENES):
            self.scenes.append(None)
            self.toolbars.append(None)
        self.go_to(scene.Scenes.MENU)

    def go_to(self, sNum, **specArgs):

        # create the scene the first time it is visited
        if self.scenes[sNum] is None:
            if sNum is scene.Scenes.MENU:
                self.scenes[sNum] = menuscene.MenuScene()
            elif sNum is scene.Scenes.INTERACTIVE:
                self.scenes[sNum] = intscene.InteractiveScene()
            elif sNum is scene.Scenes.BATTLE: 
                self.scenes[sNum] = battlescene.BattleScene(specArgs['c1'],specArgs['c2'])
            elif sNum is scene.Scenes.CODING:
                self.scenes[sNum] = codingscene.CodingScene(specArgs['plyr'])
            if(self.activity != None):
                self.toolbars[sNum] = self.scenes[sNum].makeToolbar(self.activity) 
        else: #scene has been created, but certain scenes still need special args.
            if sNum is scene.Scenes.BATTLE:
                self.scenes[sNum].sendToBattle(specArgs['c1'],specArgs['c2'])

        self.scenes[sNum].manager = self
        self.scene = self.scenes[sNum]
        if(self.activity != None):
            self.activity.set_toolbar_box(self.toolbars[sNum])
            self.toolbars[sNum].show()
        
    def sugarBeginEdit(self):
        if(self.scene == self.scenes[scene.Scenes.INTERACTIVE]):
            self.go_to(scene.Scenes.CODING, plyr = self.scenes[scene.Scenes.INTERACTIVE].main_player)

