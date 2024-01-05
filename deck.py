from card import Card
import random

class Deck:
    suits = ['C', 'D', 'H', 'S']
    cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cardList = []

    def __init__(self):
        for suitType in self.suits:
            for cardValue in self.cardValues:
                self.cardList.append(Card(suitType, cardValue, ''))
        self.shuffle()

    def shuffle(self):
        indexList = list(range(0, 52))
        newCardList = []
        while len(indexList) > 0:
            index = random.choice(indexList)
            indexList.remove(index)
            newCardList.append(self.cardList[index])
        self.cardList = newCardList

