from player import Player

class Deal:
    tricksPlayed = 0

    def __init__(self, playerList, dealDeck, firstLeader):
        self.playerList = playerList
        self.dealDeck = dealDeck
        self.firstLeader = firstLeader
        self.dealToPlayers()

    def dealToPlayers(self):
        playerIndex = 0
        for cardInstance in self.dealDeck:
            cardInstance.owner = self.playerList[playerIndex]
            playerIndex += 1
            if playerIndex == 4:
                playerIndex = 0

    def findDealWinner(self):
        winner = Player("", False, "none")
        for playerInstance in self.playerList:
            if playerInstance.tricksWon > winner.tricksWon:
                winner = playerInstance
        return winner