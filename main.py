from deck import Deck
from deal import Deal
from table import Table
from trick import Trick
from gameUtilities import fillTable, positionsToText, tablePosToScreen, readUserInput, checkHasSuit
from displayUtilities import displayCards
import random
import PySimpleGUI as sg 

def handleCPUturn(window, key, player, trick):
    trick.cardsPlayed.append(player.playerHand.playRandomCard(trick.suitToFollow))
    print(f"{player.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    previousText = window[key].get()
    window[key].update(previousText + f"\nCard Played - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")

def resolveUserPlay(userPlayer, userInput, trick, window):
    trick.cardsPlayed.append(userPlayer.playerHand.playCard(userInput[0], userInput[1]))
    print(f"{userPlayer.name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    previousText = window['-USERPLAYER-'].get()
    window['-USERPLAYER-'].update(previousText + f"\nCardPlayed - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")   

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
        
def playTrick(table, nextLeadPos, window, userPosition):
    trick = Trick(nextLeadPos, 'NT')
    print(f"Playing a new trick. {table.positions[nextLeadPos].name} ({nextLeadPos}) will lead.")

    userPlayer = table.positions[userPosition]
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

def playDeal(table, userPosition, window):
    deck = Deck()
    deck.shuffle()

    positions = list(table.positions.keys())
#    nextLeadPos = random.choice(positions)
    nextLeadPos = userPosition # remove after testing user leading

    deal = Deal(table, deck, nextLeadPos)
    displayCards(table, userPosition, window)

    playTrick(table, nextLeadPos, window, userPosition)

def main():
    mainTable = Table([])
    positions = list(mainTable.positions.keys())

    sg.theme('BluePurple')
    layout_intro = [[sg.Text("Let's play bridge!\nEnter your name: ", key='-INTRO-')],
              [sg.Input(key='-NAME-')],
              [sg.Text('Where would you like to sit?', key='-QPOSITION-')],
              [sg.Combo(positions, key='-POSITION-')],
              [sg.Button('Start')],
              [sg.Text('', key='-ERRORTEXT-')]]
    layout_deal = [[sg.Output(size=(50, 5))],
                   [sg.Text('Top Player', key='-TOPPLAYER-')],
                   [sg.Text('Left Player', key='-LEFTPLAYER-'), sg.Text('Right Player', key='-RIGHTPLAYER-', justification='r')],
                   [sg.Text('User', key='-USERPLAYER-')],
                   [sg.Text('Player Input: ', key='-USERINPUTTEXT-')],
                   [sg.Input(key='-USERINPUT-'), sg.Button('Submit')]]
    
    layout = [[sg.Column(layout_intro, key='-COLINTRO-'), sg.Column(layout_deal, visible=False, key='-COLDEAL-')],
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
                print('Playing a new deal...')
                playDeal(mainTable, values['-POSITION-'], window)
            else:
                window['-ERRORTEXT-'].update('Please enter your name and select a position from the dropdown before clicking Start.')


if __name__ == "__main__":
    main()