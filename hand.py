from card import Card
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

def buildSubList(cardList, suitToFollow):
    subList = []
    if suitToFollow != '':
        for card in cardList:
            if card.suit == suitToFollow:
                subList.append(card)
    return subList    

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
        
    def playRandomCard(self, suitToFollow):
        subList = []
        subList = buildSubList(self.cards, suitToFollow)
        playCard = Card('', '', '')
        if len(subList) > 0:
            playCard = random.choice(subList)
        else:
            playCard = random.choice(self.cards)
        self.cards.remove(playCard)
        return playCard

    def validateCardChoice(self, suitToFollow, inputSuit, inputValue):
        subList = []
        subList = buildSubList(self.cards, suitToFollow)
        if len(subList) > 0:
            for card in subList:
                if card.suit == inputSuit and card.value == inputValue:
                    return card
            return None
        for card in self.cards:
            if card.suit == inputSuit and card.value == inputValue:
                return card
        return None

    def playCard(self, suitIn, valueIn):
        for card in self.cards:
            if card.suit == suitIn and card.value == valueIn:
                self.cards.remove(card)
                return card
        return None
    
    def lowCard(self, suitIn):
        lowestCard = Card('', '', '')
        for card in self.cards:
            if card.suit == suitIn and lowestCard.value == '':
                lowestCard.copyCard(card)
            elif card.suit == suitIn and card.compareCard(lowestCard, suitIn, 'NT') == lowestCard:
                lowestCard.copyCard(card)
        if lowestCard.value != '':
            return lowestCard
        return None
                
    def highCard(self, suitIn):
        highestCard = Card('', '', '')
        for card in self.cards:
            if card.suit == suitIn and highestCard.value == '':
                highestCard.copyCard(card)
            elif card.suit == suitIn and highestCard.compareCard(card, suitIn, 'NT') == card:
                highestCard.copyCard(card)
        if highestCard.value != '':
            return highestCard
        return None