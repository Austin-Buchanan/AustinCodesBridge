
class Hand:
    cards = []

    def __init__(self, ownerName) -> None:
        self.ownerName = ownerName

    def organize(self, suitHierachy):
        suit = ""
        nextSuit = ""
        for k in range(len(self.cards)):
            for i in range(len(self.cards)):
                if i == len(self.cards) - 1:
                    continue

                suit = self.cards[i].suit
                nextSuit = self.cards[i + 1].suit

                if suitHierachy.index(suit) < suitHierachy.index(nextSuit):
                    self.cards[i], self.cards[i + 1] = self.cards[i + 1], self.cards[i]
                elif self.cards[i].compareCard(self.cards[i + 1], suit, 'NT') == self.cards[i + 1]:
                    self.cards[i], self.cards[i + 1] = self.cards[i + 1], self.cards[i]


