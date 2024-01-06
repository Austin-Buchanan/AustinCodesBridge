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

    def printHand(self):
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
        print('\n')
