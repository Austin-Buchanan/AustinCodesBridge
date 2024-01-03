from card import Card
from player import Player
import random

class Deck:
    suits = ['C', 'D', 'H', 'S']
    cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cardList = []

    def __init__(self):
        noPlayer = Player("", False, "none")
        for suitType in self.suits:
            for cardValue in self.cardValues:
                self.cardList.append(Card(suitType, cardValue, noPlayer))
        self.shuffle()

    def shuffle(self):
        indexList = list(range(1, 53))
        newCardList = []
        for cardInstance in self.cardList:
            index = random.choice(indexList)
            indexList.remove(index)
            newCardList.append(self.cardList[index])
            self.cardList.remove(cardInstance)
        self.cardList = newCardList

