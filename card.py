class Card:
    valueHierarchy = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    def __init__(self, suit, value, owner):
        self.suit = suit
        self.value = value
        self.owner = owner

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

