
def displayHand(hand):
    print('\nHere is your hand:\n')
    outputLine = ''
    for i in range(len(hand.cards)):
        if i == 0:
            outputLine = hand.cards[i].suit + ':'
        elif hand.cards[i].suit != hand.cards[i - 1].suit:
            outputLine += '\n' + hand.cards[i].suit + ':'
        outputLine += ' ' + hand.cards[i].value    
    print(outputLine)
