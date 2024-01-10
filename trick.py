from card import Card
from player import Player

class Trick:
    cardsPlayed = [] 
    suitToFollow = ""

    def __init__(self, leadPos, trump):
        self.leadPos = leadPos
        self.whoseTurn = leadPos
        self.trump = trump

    def nextTurn(self):
        match self.whoseTurn:
            case 'north':
                self.whoseTurn = 'east'
            case 'east':
                self.whoseTurn = 'south'
            case 'south':
                self.whoseTurn = 'west'
            case 'west':
                self.whoseturn = 'north'

    def setSuit(self):
        if len(self.cardsPlayed) < 1:
            return "Error - no cards played in trick"
        self.suitToFollow = self.cardsPlayed[0].suit
        return self.suitToFollow
    
    def findTrickWinner(self):
        if len(self.cardsPlayed) < 4:
            return "Error - less than 4 cards played in trick"
        noPlayer = Player("", False, "none")
        winningCard = Card("", "", noPlayer)
        for i in range(4):
            if i == 0:
                winningCard.copyCard(self.cardsPlayed[0])
            elif winningCard.compareCard(self.cardsPlayed[i]) != winningCard:
                winningCard.copyCard(self.cardsPlayed[i])
        return winningCard

