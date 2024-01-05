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

