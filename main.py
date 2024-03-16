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
    if table.findPartner(player).name == winningCard.ownerName:
        isPartnerWinning = True

    if isPartnerWinning:
        cardToPlay.copyCard(ai.findThrowAwayCard(player.hand, trick.trump))
    else:
        winningHandCard = ai.findWinningHandCard(trick, player, table)
        if winningHandCard is None:
            cardToPlay.copyCard(ai.findThrowAwayCard(player.hand, trick.trump))
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
        key = '-TOPPLAYER-'
    else:
        key = '-USERPLAYER-'
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

        if table.findPartner(userPlayer).position == nextPlayer.position:
            print("It's your partner's turn. What card should your partner play?")
            handleUserTurn(window, nextPlayer, trick)
        elif nextPlayer.isCPU:
            layoutLocation = gu.tablePosToScreen(userPosition, nextPlayer.position)
            keyString = '-' + layoutLocation.upper() + 'PLAYER-'
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

    nextLeadPos = userPosition # replace if bidding is introduced in the future so other players can be the declarer, not just the user

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
    layout_deal_header = [[sg.Output(size=(50, 10))],
                   [sg.Text('Trump Suit: ', key='-TRUMPTEXT-')],
                   [sg.Text('North-South Score: ', key='-NSSCORE-')],
                   [sg.Text('East-West Score: ', key='-EWSCORE-')]]
    layout_partner = [[sg.Text('Top Player', key='-TOPPLAYER-', justification='left')]]
    layout_opponents = [[sg.Text('Left Player', key='-LEFTPLAYER-', justification='left'), sg.Text('Right Player', key='-RIGHTPLAYER-', justification='right')]]
    layout_user = [[sg.Text('User', key='-USERPLAYER-')],
                   [sg.Text('Player Input: ', key='-USERINPUTTEXT-')],
                   [sg.Input(key='-USERINPUT-'), sg.Button('Submit')],
                   [sg.Button('Play Low'), sg.Button('Play High')]]    
    layout = [[sg.Column(layout_intro, key='-COLINTRO-'),
               sg.Column(layout_play_again, visible=False, key='-COLPLAYAGAIN-'),
               sg.Column(layout_deal_header, visible=False, key='-COLDEALHDR-', expand_x=True),
               sg.Column(layout_partner, visible=False, key='-COLPARTNER-', expand_x=True),
               sg.Column(layout_opponents, visible=False, key='-COLOPPONENTS-', expand_x=True),
               sg.Column(layout_user, visible=False, key='-COLUSER-', expand_x=True)],
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
                print(gu.positionsToText(mainTable) + f"Your partner will be {mainTable.findPartner(mainTable.positions[values['-POSITION-']]).name}.")
                window['-COLINTRO-'].update(visible=False)
                window['-COLDEALHDR-'].update(visible=True)
                window['-COLPARTNER-'].update(visible=True)
                window['-COLOPPONENTS-'].update(visible=True)
                window['-COLUSER-'].update(visible=True)
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