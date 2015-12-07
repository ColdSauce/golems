import menuscene, battlescene, intscene, codingscene, scene

class SceneManager():

    def __init__(self):
        # initialized the scene array to empty values.
        self.scenes = []
        for i in range(scene.Scenes.NUMSCENES) : self.scenes.append(None)
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
                self.scenes[sNum] = codingscene.CodingScene()

        self.scenes[sNum].manager = self
        self.scene = self.scenes[sNum]
        


