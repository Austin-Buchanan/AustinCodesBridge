from hand import Hand

class Player:
    gameScore = 0
    tricksWon = 0

    def __init__(self, name, isCPU, position, playerHand):
        self.name = name
        self.isCPU = isCPU
        self.position = position
        self.playerHand = playerHand
