from gameUtilities import cardsToStr, tablePosToScreen

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

def displayPlayerHand(key, player, window):
    window[key].update(f"{player.name} ({player.position}){cardsToStr(player.playerHand.cards)}")

def displayHiddenHand(key, player, window):
    window[key].update(f"{player.name} ({player.position})\n[{']'*len(player.playerHand.cards)}")

def displayCards(table, userPosition, window):
    positions = list(table.positions.keys())
    for position in positions:
        player = table.positions[position]
        player.playerHand.organizeHand()
        if table.findPartner(table.positions[userPosition]).position == position:
            displayPlayerHand('-TOPPLAYER-', player, window)
        elif position == userPosition:
            displayPlayerHand('-USERPLAYER-', player, window)
        else:
            screenPos = tablePosToScreen(userPosition, position)
            if screenPos == 'left':
                displayHiddenHand('-LEFTPLAYER-', player, window)
            else:
                displayHiddenHand('-RIGHTPLAYER-', player, window)

def updateScoreDisplay(window, deal):
    window['-NSSCORE-'].update('North-South Score: ' + str(deal.scoreNS))
    window['-EWSCORE-'].update('East-West Score: ' + str(deal.scoreEW))
    window.refresh()
