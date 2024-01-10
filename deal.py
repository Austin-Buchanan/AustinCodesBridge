from player import Player

class Deal:
    tricksPlayed = 0

    def __init__(self, dealTable, dealDeck, firstLeadPos):
        self.dealTable = dealTable
        self.dealDeck = dealDeck
        self.firstLeadPos = firstLeadPos
        self.dealToPlayers()

    def dealToPlayers(self):
        playerIndex = 0
        positionString = ''
        for cardInstance in self.dealDeck.cardList:
            positionString = ''
            match playerIndex:
                case 0:
                    positionString = 'north'
                    playerIndex += 1
                case 1:
                    positionString = 'east'
                    playerIndex += 1
                case 2:
                    positionString = 'south'
                    playerIndex += 1
                case 3:
                    positionString = 'west'
                    playerIndex = 0
            cardInstance.ownerName = self.dealTable.positions[positionString].name
            self.dealTable.positions[positionString].playerHand.addCard(cardInstance)

    def findDealWinner(self):
        winner = Player("", False, "none")
        for playerInstance in self.playerList:
            if playerInstance.tricksWon > winner.tricksWon:
                winner = playerInstance
        return winner