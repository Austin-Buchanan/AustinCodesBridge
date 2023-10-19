import random

suits = ['C', 'D', 'H', 'S']
cardTypes = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def fillDeck(deck):
    for suit in suits: 
        for cardType in cardTypes:
            deck.append(cardType + suit)

def shuffleDeck(deck):
    indexList = list(range(1, 53))
    newDeck = []
    for i in range(1, 53):
        newDeck.append('')
    for card in deck:
        index = random.choice(indexList)
        indexList.remove(index)
        newDeck[index - 1] = card
    return newDeck   

def dealCards(deck, hand1, hand2, hand3, hand4):
    counter = 0
    for i in range(0, 13):
        hand1.append(deck[counter])
        counter += 1
        hand2.append(deck[counter])
        counter += 1
        hand3.append(deck[counter])
        counter += 1
        hand4.append(deck[counter])

def organizeHand(hand):
    cardType = ""
    nextCardType = ""
    suit = ""
    nextSuit = ""
    for i in range(0, 13):
        if i == 12:
            continue

        suit = hand[i][-1]
        nextSuit = hand[i + 1][-1]

        if len(hand[i]) == 3:
            cardType = hand[i][0:2]
        else:
            cardType = hand[i][0]

        if len(hand[i + 1]) == 3:
            nextCardType = hand[i + 1][0:2]
        else:
            nextCardType = hand[i + 1][0]        
      
        if suits.index(suit) < suits.index(nextSuit):
            hand[i], hand[i + 1] = hand[i + 1], hand[i]
        elif suits.index(suit) == suits.index(nextSuit) and cardTypes.index(cardType) < cardTypes.index(nextCardType):
            hand[i], hand[i + 1] = hand[i + 1], hand[i]

def printCards(cardList):
    stringToPrint = ""
    for card in cardList:
        stringToPrint += card + " "
    print(stringToPrint)

def displayHand(hand):
    spades = []
    hearts = []
    diamonds = []
    clubs = []    
    for card in hand:
        if card[-1] == 'S':
            spades.append(card)
        elif card[-1] == 'H':
            hearts.append(card)
        elif card[-1] == 'D':
            diamonds.append(card)
        elif card[-1] == 'C':
            clubs.append(card)
    printCards(spades)
    printCards(hearts)
    printCards(diamonds)
    printCards(clubs)

def main():
    print("Playing bridge.")
    
    # Deal cards
    deck = []
    fillDeck(deck)
    deck = shuffleDeck(deck)
    playerHand = []
    leftOpponentHand = []
    partnerHand = []
    rightOpponentHand = []
    dealCards(deck, playerHand, leftOpponentHand, partnerHand, rightOpponentHand)

    # Organize and display player hand
    for i in range(0, len(playerHand)):
        organizeHand(playerHand)
    print("Player hand:")
    displayHand(playerHand)

if __name__ == "__main__":
    main()
