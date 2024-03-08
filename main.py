from deck import Deck
from deal import Deal
from table import Table
from trick import Trick
from gameUtilities import fillTable, positionsToText, tablePosToScreen, readUserInput, checkHasSuit, incrementScore
from displayUtilities import displayCards, displayPlayerHand, updateScoreDisplay
import random, time
import PySimpleGUI as sg 

def handleCPUturn(window, key, player, trick):
    trick.cardsPlayed.append(player.playerHand.playRandomCard(trick.suitToFollow))
    displayPlayerHand(key, player, window)
    previousText = window[key].get()
    window[key].update(previousText + f"\nCard Played - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")
    print(f"{player.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    window.refresh()
    time.sleep(1)

def resolveUserPlay(userPlayer, userInput, trick, window):
    trick.cardsPlayed.append(userPlayer.playerHand.playCard(userInput[0], userInput[1]))
    print(f"{userPlayer.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    displayPlayerHand('-USERPLAYER-', userPlayer, window)
    previousText = window['-USERPLAYER-'].get()
    window['-USERPLAYER-'].update(previousText + f"\nCardPlayed - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")
    window.refresh()
    time.sleep(1)   

def handleUserTurn(window, userPlayer, trick):
    userInput = readUserInput(window)
    inHand = False
    for card in userPlayer.playerHand.cards:
        if card.suit == userInput[0] and card.value == userInput[1]:
            inHand = True
    if not inHand:
        print('The card you entered is not in your hand. Please try again.')
        handleUserTurn(window, userPlayer, trick)
    elif len(trick.cardsPlayed) > 0 and userInput[0] != trick.suitToFollow:
        # check if the user has any cards matching suitToFollow in their hand
        if checkHasSuit(userPlayer.playerHand, trick.suitToFollow):
            print('You must play a card that follows suit. Please try again.')
            handleUserTurn(window, userPlayer, trick)
        else:
            resolveUserPlay(userPlayer, userInput, trick, window)         
    else:
        resolveUserPlay(userPlayer, userInput, trick, window)
        
def playTrick(table, nextLeadPos, window, userPosition, trumpType):
    trick = Trick(nextLeadPos, trumpType)
    print(f"Playing a new trick. {table.positions[nextLeadPos].name} ({nextLeadPos}) will lead.")

    userPlayer = table.positions[userPosition]

    while len(trick.cardsPlayed) < 4:
        nextPlayer = table.positions[trick.whoseTurn]

        if table.findPartner(userPlayer).position == nextPlayer.position:
            handleCPUturn(window, '-TOPPLAYER-', nextPlayer, trick)
        elif nextPlayer.isCPU:
            layoutLocation = tablePosToScreen(userPosition, nextPlayer.position)
            keyString = '-' + layoutLocation.upper() + 'PLAYER-'
            handleCPUturn(window, keyString, nextPlayer, trick)
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

    nextLeadPos = userPosition # replace if bidding is introduced in the future so other players can be the declarer, not just the user

    deal = Deal(table, deck, nextLeadPos)

    trumpTypes = ['S', 'H', 'D', 'C', 'NT']
    trumpType = random.choice(trumpTypes)
    print(f"The trump suit is {trumpType}.")
    window['-TRUMPTEXT-'].update(f"Trump Suit: {trumpType}")
    window.refresh()

    while deal.tricksPlayed < 13:
        displayCards(table, userPosition, window)
        window.refresh()
        winnerName = playTrick(table, nextLeadPos, window, userPosition, trumpType)
        nextLeadPos = table.findPlayerPos(winnerName)
        deal.tricksPlayed += 1
        incrementScore(nextLeadPos, deal)
        updateScoreDisplay(window, deal)
    
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
            window['-COLPLAYAGAIN-'].update(visible=False)
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
    layout_deal = [[sg.Output(size=(50, 10))],
                   [sg.Text('Trump Suit: ', key='-TRUMPTEXT-')],
                   [sg.Text('North-South Score: ', key='-NSSCORE-')],
                   [sg.Text('East-West Score: ', key='-EWSCORE-')],
                   [sg.Text('Top Player', key='-TOPPLAYER-')],
                   [sg.Text('Left Player', key='-LEFTPLAYER-'), sg.Text('Right Player', key='-RIGHTPLAYER-', justification='r')],
                   [sg.Text('User', key='-USERPLAYER-')],
                   [sg.Text('Player Input: ', key='-USERINPUTTEXT-')],
                   [sg.Input(key='-USERINPUT-'), sg.Button('Submit')]]
    
    layout = [[sg.Column(layout_intro, key='-COLINTRO-'),
               sg.Column(layout_play_again, visible=False, key='-COLPLAYAGAIN-'),
               sg.Column(layout_deal, visible=False, key='-COLDEAL-')],
              [sg.Button('Exit')]]
    
    window = sg.Window('Austin Codes Bridge', layout)

    while True: 
        event, values = window.read()
#        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Start':
            if values['-NAME-'] != '' and values['-POSITION-'] in positions:
                fillTable(mainTable, values['-NAME-'], values['-POSITION-'])
                print(positionsToText(mainTable) + f"Your partner will be {mainTable.findPartner(mainTable.positions[values['-POSITION-']]).name}.")
                window['-COLINTRO-'].update(visible=False)
                window['-COLDEAL-'].update(visible=True)
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