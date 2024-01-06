class Table:
    positions = {
        'north': None, 
        'east': None,
        'south': None,
        'west': None
    }

    def __init__(self, playersIn) -> None:
        for playerIn in playersIn:
            self.addPlayer(playerIn)

    def addPlayer(self, playerIn):
        self.positions[playerIn.position] = playerIn

    def findPartner(self, playerIn):
        match playerIn.position:
            case 'north':
                return self.positions['south']
            case 'east':
                return self.positions['west']
            case 'south':
                return self.positions['north']
            case 'west':
                return self.positions['east']
            
    def promptToPlay(self, position):
        if self.positions[position].isCPU:
            self.positions[position].playCPUcard()
        else
            self.positions[position].playUserCard()