
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

def printTrickScore(tableIn):
    print('Here are the number of tricks won in the current deal.')
    for player in tableIn.positions.values():
        print(f"{player.name} ({player.position}) - {player.tricksWon}")