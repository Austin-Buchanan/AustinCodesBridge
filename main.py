from deck import Deck
from deal import Deal
from table import Table
from trick import Trick
from card import Card
import gameUtilities as gu
import displayUtilities as du
import opponentAI as ai 
import time
import PySimpleGUI as sg 

def handleCPUturn(window, key, player, trick, table):
    cardToPlay = Card('','','')

    isPartnerWinning = False
    winningCard = trick.findCurrentWinner()
    if winningCard is not None and table.findPartner(player).name == winningCard.ownerName:
        isPartnerWinning = True

    if isPartnerWinning:
        cardToPlay.copyCard(ai.findThrowAwayCard(player.playerHand, trick.trump))
    else:
        winningHandCard = ai.findWinningHandCard(trick, player, table)
        if winningHandCard is None:
            cardToPlay.copyCard(ai.findThrowAwayCard(player.playerHand, trick.trump))
        else:
            cardToPlay.copyCard(winningHandCard)

    trick.cardsPlayed.append(player.playerHand.playCard(cardToPlay.suit, cardToPlay.value))
    du.displayHiddenHand(key, player, window)
    previousText = window[key].get()
    window[key].update(previousText + f"\nCard Played - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")
    print(f"{player.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    window.refresh()
    time.sleep(1)

def resolveUserPlay(player, trick, window):
    print(f"{player.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    key = ''
    if player.isCPU:
        key = '-TOPPLAYERCARDS-'
    else:
        key = '-USERPLAYERCARDS-'
    du.displayPlayerHand(key, player, window)
    previousText = window[key].get()
    window[key].update(previousText + f"\nCardPlayed - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")
    window.refresh()
    time.sleep(1)   

def handleUserTurn(window, userPlayer, trick):
    userInput = gu.readUserInput(window)
    if userInput == 'play-low' or userInput == 'LOW':
        lowOutcome = gu.playLow(userPlayer.playerHand, trick)
        if lowOutcome != 'success':
            print('A low card of the same suit could not be found. Please enter the card to play.')
            handleUserTurn(window, userPlayer, trick)
        else:
            resolveUserPlay(userPlayer, trick, window)
    elif userInput == 'play-high' or userInput == 'HIGH':
        highOutcome = gu.playHigh(userPlayer.playerHand, trick)
        if highOutcome != 'success':
            print('A high card of the same suit could not be found. Please enter the card to play.')
            handleUserTurn(window, userPlayer, trick)
        else:
            resolveUserPlay(userPlayer, trick, window)
    else:
        inHand = False
        for card in userPlayer.playerHand.cards:
            if card.suit == userInput[0] and card.value == userInput[1]:
                inHand = True
        if not inHand:
            print('The card you entered is not in your hand. Please try again.')
            handleUserTurn(window, userPlayer, trick)
        elif len(trick.cardsPlayed) > 0 and userInput[0] != trick.suitToFollow:
            if gu.checkHasSuit(userPlayer.playerHand, trick.suitToFollow):
                print('You must play a card that follows suit. Please try again.')
                handleUserTurn(window, userPlayer, trick)
            else:
                trick.cardsPlayed.append(userPlayer.playerHand.playCard(userInput[0], userInput[1]))
                resolveUserPlay(userPlayer, trick, window)         
        else:
            trick.cardsPlayed.append(userPlayer.playerHand.playCard(userInput[0], userInput[1]))
            resolveUserPlay(userPlayer, trick, window)
        
def playTrick(table, nextLeadPos, window, userPosition, trumpType):
    trick = Trick(nextLeadPos, trumpType)
    print(f"Playing a new trick. {table.positions[nextLeadPos].name} ({nextLeadPos}) will lead.")

    userPlayer = table.positions[userPosition]

    while len(trick.cardsPlayed) < 4:
        nextPlayer = table.positions[trick.whoseTurn]
        layoutLocation = gu.tablePosToScreen(userPosition, nextPlayer.position)
        du.updateTurnDisplay(layoutLocation, nextPlayer, window, table)

        if table.findPartner(userPlayer).position == nextPlayer.position:
            print("It's your partner's turn. What card should your partner play?")
            handleUserTurn(window, nextPlayer, trick)
        elif nextPlayer.isCPU:
            keyString = '-' + layoutLocation.upper() + 'PLAYERCARDS-'
            handleCPUturn(window, keyString, nextPlayer, trick, table)
        else:
            print("It's your turn. Enter a card from your hand in the player input box.")
            handleUserTurn(window, userPlayer, trick)

        if len(trick.cardsPlayed) == 1:
            trick.suitToFollow = trick.cardsPlayed[0].suit

        trick.nextTurn()

    # End trick and determine winner
    print('The trick has ended.')
    winningCard = trick.findTrickWinner()
    print(f"The winner is {winningCard.ownerName}.")
    window.refresh()
    time.sleep(1)
    return winningCard.ownerName

def playDeal(table, userPosition, window):
    deck = Deck()
    deck.shuffle()

    nextLeadPos = gu.findLeaderPosition(userPosition) # replace if bidding is introduced in the future so other players can be the declarer, not just the user

    deal = Deal(table, deck, nextLeadPos)

    trumpType = gu.determineTrump(table, userPosition)
    print(f"The trump suit is {trumpType}.")
    window['-TRUMPTEXT-'].update(f"Trump Suit: {trumpType}")
    window.refresh()

    while deal.tricksPlayed < 13:
        du.displayCards(table, userPosition, window)
        window.refresh()
        winnerName = playTrick(table, nextLeadPos, window, userPosition, trumpType)
        nextLeadPos = table.findPlayerPos(winnerName)
        deal.tricksPlayed += 1
        gu.incrementScore(nextLeadPos, deal)
        du.updateScoreDisplay(window, deal)
    
    winners = deal.findDealWinners()
    if winners == 'tie':
        print('The deal ended in a tie.')
    else:
        print(f"{winners} win!")
    window.refresh()

def checkPlayAgain(window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Play Again':
            window['-NSSCORE-'].update('North-South Score: ')
            window['-EWSCORE-'].update('East-West Score: ')
            window['-COLPLAYAGAIN-'].hide_row()
            return True
    return False

def main():
    mainTable = Table([])
    positions = list(mainTable.positions.keys())
    playing = True

    sg.theme('BluePurple')
    layout_intro = [[sg.Text("Let's play bridge!\nEnter your name: ", key='-INTRO-')],
              [sg.Input(key='-NAME-')],
              [sg.Text('Where would you like to sit?', key='-QPOSITION-')],
              [sg.Combo(positions, key='-POSITION-')],
              [sg.Button('Start')],
              [sg.Text('', key='-ERRORTEXT-')]]
    layout_play_again = [[sg.Text('Do you want to play again?', key='-PLAYAGAINTEXT-'), sg.Button('Play Again')]]
    layout_deal_header = [[sg.Output(size=(50, 10))],
                   [sg.Text('Trump Suit: ', key='-TRUMPTEXT-')],
                   [sg.Text('North-South Score: ', key='-NSSCORE-')],
                   [sg.Text('East-West Score: ', key='-EWSCORE-')],
                   [sg.Text('Whose Turn: ', key='-TURNTEXT-')]]
    layout_partner = [[sg.Text('', key='-TOPPLAYERHDR-', justification='left')],
                      [sg.Text('', key='-TOPPLAYERCARDS-', justification='left')]]
    layout_left_player = [[sg.Text('', key='-LEFTPLAYERHDR-', justification='left')],
                          [sg.Text('', key='-LEFTPLAYERCARDS-', justification='left')]]
    layout_right_player = [[sg.Text('', key='-RIGHTPLAYERHDR-',justification='right')],
                           [sg.Text('', key='-RIGHTPLAYERCARDS-', justification='left')]]
    layout_user = [[sg.Text('', key='-USERPLAYERHDR-', justification='left')],
                   [sg.Text('', key='-USERPLAYERCARDS-', justification='left')]]
    layout_user_input = [[sg.Text('Player Input: ', key='-USERINPUTTEXT-', justification='left')],
                   [sg.Input(key='-USERINPUT-'), sg.Button('Submit')],
                   [sg.Button('Play Low'), sg.Button('Play High')]]    
    layout = [[sg.Column(layout_intro, key='-COLINTRO-', element_justification='left')],
              [sg.Column(layout_play_again, visible=False, key='-COLPLAYAGAIN-', size=(None, None), pad=(0,0), element_justification='center')],
              [sg.Column(layout_deal_header, visible=False, key='-COLDEALHDR-', size=(None, None), pad=(0,0))],
              [sg.Column(layout_partner, visible=False, key='-COLPARTNER-', size=(None, None), pad=(0,0), element_justification='center')],
              [sg.Column(layout_left_player, visible=False, key='-COLLEFTPLAYER-', element_justification='left'), sg.Column(layout_right_player, visible=False, key='-COLRIGHTPLAYER-', element_justification='right')],
              [sg.Column(layout_user, visible=False, key='-COLUSER-', element_justification='center')],
              [sg.Column(layout_user_input, visible=False, key='-COLUSERINPUT-')],
              [sg.Button('Exit')]]
    
    window = sg.Window('Austin Codes Bridge', layout, finalize=True)
    window['-USERINPUT-'].bind("<Return>", "Enter")

    while True: 
        event, values = window.read()
#        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Start':
            if values['-NAME-'] != '' and values['-POSITION-'] in positions:
                gu.fillTable(mainTable, values['-NAME-'], values['-POSITION-'])
                partner = mainTable.findPartner(mainTable.positions[values['-POSITION-']])
                print(gu.positionsToText(mainTable) + f"Your partner will be {partner.name}.")
                du.fillHeaders(window, mainTable)
                window['-COLINTRO-'].hide_row()
                window['-COLDEALHDR-'].update(visible=True)
                window['-COLPARTNER-'].update(visible=True)
                window['-COLPARTNER-'].expand(expand_x=True, expand_y=False)
                window['-COLLEFTPLAYER-'].update(visible=True)
                window['-COLLEFTPLAYER-'].expand(expand_x=True, expand_y=False)
                window['-COLRIGHTPLAYER-'].update(visible=True)
                window['-COLRIGHTPLAYER-'].expand(expand_x=True, expand_y=False)
                window['-COLUSER-'].update(visible=True)
                window['-COLUSER-'].expand(expand_x=True, expand_y=False)
                window['-COLUSERINPUT-'].update(visible=True)
                while(playing):
                    print('Playing a new deal...')
                    playDeal(mainTable, values['-POSITION-'], window)
                    window['-COLPLAYAGAIN-'].update(visible=True)
                    window.refresh()
                    playing = checkPlayAgain(window)
            else:
                window['-ERRORTEXT-'].update('Please enter your name and select a position from the dropdown before clicking Start.')


if __name__ == "__main__":
    main()