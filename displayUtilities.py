
def printDeck(deck):
    print('Printing deck...')
    outString = ''
    for card in deck.cardList:
        outString += f"{card.suit + card.value} "
    print(outString)

def printHand(hand):
    print(f"Showing {hand.ownerName}\'s hand...")
    hand.organizeHand()
    spadeStr = 'S: '
    heartStr = 'H: '
    diamondStr = 'D: '
    clubStr = 'C: '
    for card in hand.cards:
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