class Card:
    valueHierarchy = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, value, ownerName):
        self.suit = suit
        self.value = value
        self.ownerName = ownerName
        match value:
            case 'A':
                self.HCPvalue = 4
            case 'K':
                self.HCPvalue = 3
            case 'Q':
                self.HCPvalue = 2
            case 'J':
                self.HCPvalue = 1
            case _:
                self.HCPvalue = 0

    def copyCard(self, otherCard):
        self.suit = otherCard.suit
        self.value = otherCard.value
        self.owner = otherCard.owner

    def compareCard(self, otherCard, suitToFollow, trump):
        if self.suit != trump and otherCard.suit == trump:
            return otherCard
        elif self.suit == trump and otherCard.suit != trump:
            return self
        elif self.suit != suitToFollow and otherCard.suit == suitToFollow:
            return otherCard
        elif self.suit == suitToFollow and otherCard.suit != suitToFollow:
            return self
        elif self.valueHierarchy.index(self.value) < self.valueHierarchy.index(otherCard.value):
            return otherCard
        elif self.valueHierarchy.index(self.value) > self.valueHierarchy.index(otherCard.value):
            return self

