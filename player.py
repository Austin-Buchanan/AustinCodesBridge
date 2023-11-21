class Player:
    gameScore = 0

    def __init__(self, name, isCPU):
        self.name = name
        self.isCPU = isCPU

    def getGameScore(self):
        return self.gameScore
    
    def updateGameScore(self, increment):
        self.gameScore = self.gameScore + increment