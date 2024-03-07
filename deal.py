from player import Player

class Deal:
    tricksPlayed = 0
    scoreNS = 0
    scoreEW = 0

    def __init__(self, dealTable, dealDeck, firstLeadPos):
        self.dealTable = dealTable
        self.dealDeck = dealDeck
        self.leader = firstLeadPos
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

    def findDealWinners(self):
        if self.scoreNS > self.scoreEW:
            return 'North-South'
        elif self.scoreNS < self.scoreEW:
            return 'East-West'
        else:
            return 'tie'
    
#    def setNewLeader(self, leadPos)