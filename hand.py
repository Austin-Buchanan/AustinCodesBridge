import random

def organizeInSuit(cardList):
    if len(cardList) == 1:
        return cardList
    for k in range(len(cardList) - 1):
        for i in range(len(cardList)):
            if i == len(cardList) - 1:
                continue
            elif cardList[i].compareCard(cardList[i + 1], cardList[i].suit, None) == cardList[i + 1]:
                cardList[i], cardList[i + 1] = cardList[i + 1], cardList[i]
    return cardList

class Hand:
    cards = []

    def __init__(self, ownerName, cards) -> None:
        self.ownerName = ownerName
        if len(cards) > 1:
            self.cards = cards
        else:
            self.cards = []

    def removeCard(self, cardToRemove):
        if cardToRemove in self.cards:
            self.cards.remove(cardToRemove)

    def addCard(self, cardToAdd):
        self.cards.append(cardToAdd)

    def countHCP(self):
        points = 0
        for card in self.cards:
            match card.value:
                case 'A':
                    points += 4
                case 'K': 
                    points += 3
                case 'Q':
                    points += 2
                case 'J':
                    points += 1
        return points

    def organizeHand(self):
        spades = []
        hearts = []
        diamonds = []
        clubs = []
        for card in self.cards:
            match card.suit:
                case 'S':
                    spades.append(card)
                case 'H':
                    hearts.append(card)
                case 'D':
                    diamonds.append(card)
                case 'C':
                    clubs.append(card)
        spades = organizeInSuit(spades)
        hearts = organizeInSuit(hearts)
        diamonds = organizeInSuit(diamonds)
        clubs = organizeInSuit(clubs)
        self.cards = spades + hearts + diamonds + clubs

    def printHand(self):
        self.organizeHand()
        spadeStr = 'S: '
        heartStr = 'H: '
        diamondStr = 'D: '
        clubStr = 'C: '
        for card in self.cards:
            match card.suit:
                case 'S':
                    spadeStr += card.value + ' '
                case 'H':
                    heartStr += card.value + ' '
                case 'D':
                    diamondStr += card.value + ' '
                case 'C':
                    clubStr += card.value + ' '
        print(spadeStr)
        print(heartStr)
        print(diamondStr)
        print(clubStr)
        
    def playCardCPU(self):
        playCard = random.choice(self.cards)
        self.cards.remove(playCard)
        return playCard

