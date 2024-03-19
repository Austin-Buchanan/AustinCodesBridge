from gameUtilities import cardsToStr, tablePosToScreen
import PySimpleGUI as sg

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
    window[key].update(f"{cardsToStr(player.playerHand.cards)}")

def displayHiddenHand(key, player, window):
    if len(player.playerHand.cards) > 0:
        window[key].update(f"[{']'*len(player.playerHand.cards)}")
    else:
        window[key].update('')

def displayCards(table, userPosition, window):
    positions = list(table.positions.keys())
    for position in positions:
        player = table.positions[position]
        player.playerHand.organizeHand()
        if table.findPartner(table.positions[userPosition]).position == position:
            displayPlayerHand('-TOPPLAYERCARDS-', player, window)
        elif position == userPosition:
            displayPlayerHand('-USERPLAYERCARDS-', player, window)
        else:
            screenPos = tablePosToScreen(userPosition, position)
            if screenPos == 'left':
                displayHiddenHand('-LEFTPLAYERCARDS-', player, window)
            else:
                displayHiddenHand('-RIGHTPLAYERCARDS-', player, window)
    centerWindowVert(window)

def updateScoreDisplay(window, deal):
    window['-NSSCORE-'].update('North-South Score: ' + str(deal.scoreNS))
    window['-EWSCORE-'].update('East-West Score: ' + str(deal.scoreEW))
    window.refresh()

def centerWindowVert(window):
    screenSize = window.get_screen_size()
    windowSize = window.size
    y = (screenSize[1] - windowSize[1]) // 2
    window.move(window.CurrentLocation()[0], y)
    window.refresh()

def updateTurnDisplay(location, player, window, table):
    window['-TURNTEXT-'].update(f"Whose Turn: {player.name}")
    fillHeaders(window, table, location)
    window.refresh()

def fillHeaders(window, table, turnSeat=None):
    user = table.findUser()
    partner = table.findPartner(user)
    positions = list(table.positions.keys())
    for position in positions:
        if position == partner.position:
            window['-TOPPLAYERHDR-'].update(f"{partner.name} ({partner.position})")
            continue
        if position == user.position:
            window['-USERPLAYERHDR-'].update(f"{user.name} ({user.position})")
            continue
        seat = tablePosToScreen(user.position, position)
        key = '-' + seat.upper() + 'PLAYERHDR-'
        player = table.positions[position]
        window[key].update(f"{player.name} ({player.position})")
    if turnSeat is not None:
        key = '-' + turnSeat.upper() + 'PLAYERHDR-'
        currentText = window[key].get()
        window[key].update(f"**{currentText}**")


