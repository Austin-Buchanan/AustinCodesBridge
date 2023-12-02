from card import Card
from player import Player

class Trick:
    cardsPlayed = [] 
    suitToFollow = ""

    def __init__(self, leader, trump):
        self.leader = leader
        self.trump = trump

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
                

