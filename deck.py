from card import Card
from player import Player
import random

class Deck:
    suits = ['C', 'D', 'H', 'S']
    cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    cardList = []

    def __init__(self):
        noPlayer = Player("", False, "none")
        for suitType in self.suits:
            for cardValue in self.cardValues:
                self.cardList.append(Card(suitType, cardValue, noPlayer.name))
        self.shuffle()

    def shuffle(self):
        indexList = list(range(0, 52))
        newCardList = []
        for i in range(52):
            index = random.choice(indexList)
            indexList.pop()
            try:
                newCardList.append(self.cardList[index])
                self.cardList.remove(self.cardList[index])
            except:
                print("Error at index " + str(index))
                print("cardList length: " + str(len(self.cardList)))
                raise
        self.cardList = newCardList