from card import Card

class Trick:
    suitToFollow = ''

    def __init__(self, leadPos, trump):
        self.whoseTurn = leadPos
        self.trump = trump
        self.cardsPlayed = []

    def nextTurn(self):
        match self.whoseTurn:
            case 'north':
                self.whoseTurn = 'east'
            case 'east':
                self.whoseTurn = 'south'
            case 'south':
                self.whoseTurn = 'west'
            case 'west':
                self.whoseTurn = 'north'

    def setSuit(self):
        if len(self.cardsPlayed) < 1:
            return "Error - no cards played in trick"
        self.suitToFollow = self.cardsPlayed[0].suit
        return self.suitToFollow
    
    def findTrickWinner(self):
        if len(self.cardsPlayed) < 4:
            return "Error - less than 4 cards played in trick"
        winningCard = Card('', '', '')
        for i in range(4):
            if i == 0:
                winningCard.copyCard(self.cardsPlayed[0])
                self.suitToFollow = self.cardsPlayed[0].suit
            elif winningCard.compareCard(self.cardsPlayed[i], self.suitToFollow, self.trump) != winningCard:
                winningCard.copyCard(self.cardsPlayed[i])
        return winningCard
    
    def findCurrentWinner(self):
        if len(self.cardsPlayed) == 0:
            return None
        winningCard = Card('', '', '')
        for card in self.cardsPlayed:
            if winningCard.value == '':
                winningCard.copyCard(card)
                continue
            if winningCard.compareCard(card, self.suitToFollow, self.trump) == card:
                winningCard.copyCard(card)
        return winningCard

