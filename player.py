class Player:
    gameScore = 0
    tricksWon = 0
    hand = []

    def __init__(self, name, isCPU, position):
        self.name = name
        self.isCPU = isCPU
        self.position = position

    def getPartner(self, players):
        partnerPosition = ''
        match self.position:
            case 'north':
                partnerPosition = 'south'
            case 'east':
                partnerPosition = 'west'
            case 'south':
                partnerPosition = 'north'
            case 'west':
                partnerPosition = 'east'
        for player in players:
            if player.position == partnerPosition:
                return player
        return 'Error - no partner found'