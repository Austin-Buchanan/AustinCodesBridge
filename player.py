class Player:
    gameScore = 0
    tricksWon = 0
    hand = []

    def __init__(self, name, isCPU, position):
        self.name = name
        self.isCPU = isCPU
        self.position = position
