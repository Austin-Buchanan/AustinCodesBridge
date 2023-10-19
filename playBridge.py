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

def organizeBySuit(hand):
    for i in range(0, 13):
        # if i != 12:
        #     print(f"Comparing {hand[i]} and {hand[i + 1]}")        
        if i != 12 and suits.index(hand[i][-1]) > suits.index(hand[i + 1][-1]):
            hand[i], hand[i + 1] = hand[i + 1], hand[i]
            # print("Swapped.")
        # elif i != 12:
        #     print("Did not swap.")

def main():
    print("Playing bridge.")
    
    deck = []
    fillDeck(deck)
    # print("Here is the deck:")
    # print(deck)
    # print(len(deck))

    deck = shuffleDeck(deck)
    # print("Here is the shuffled deck:")
    # print(deck)
    # print(len(deck))

    playerHand = []
    leftOpponentHand = []
    partnerHand = []
    rightOpponentHand = []
    dealCards(deck, playerHand, leftOpponentHand, partnerHand, rightOpponentHand)
    # print("Player hand:")
    # print(playerHand)
    # print("Left opponent hand:")
    # print(leftOpponentHand)
    # print("Partner hand:")
    # print(partnerHand)
    # print("Right opponent hand:")
    # print(rightOpponentHand)

    for i in range(0, len(playerHand)):
        organizeBySuit(playerHand)
    print("Player hand:")
    print(playerHand)

if __name__ == "__main__":
    main()
