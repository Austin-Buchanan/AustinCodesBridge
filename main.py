from player import Player
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
from trick import Trick
import random, sys
import PySimpleGUI as sg 

def fillTable(table, username, userPosition):
    user = Player(username, False, userPosition, Hand(username, []))
    table.addPlayer(user)
    otherPlayerNames = ['Allison', 'Blake', 'Catherine', 'Dylan']
    if username in otherPlayerNames:
        otherPlayerNames.remove(username)
    for i in range(3):
        emptyPosStr = ''
        if table.positions['north'] is None:
            emptyPosStr = 'north'
        elif table.positions['east'] is None:
            emptyPosStr = 'east'
        elif table.positions['south'] is None:
            emptyPosStr = 'south'
        elif table.positions['west'] is None:
            emptyPosStr = 'west'
        newPlayer = Player(otherPlayerNames[0], True, emptyPosStr, Hand(otherPlayerNames[0], []))
        otherPlayerNames.remove(newPlayer.name)
        table.addPlayer(newPlayer)    

def positionsToText(table):
    infoText = ''
    positions = list(table.positions.keys())
    for position in positions:
        infoText += f"{table.positions[position].name} is playing {position}.\n"
    return infoText

def cardsToStr(cards):
    spadeStr = 'S: '
    heartStr = 'H: '
    diamondStr = 'D: '
    clubStr = 'C: '
    for card in cards:
        match card.suit:
            case 'S':
                spadeStr += card.value + ' '
            case 'H':
                heartStr += card.value + ' '
            case 'D':
                diamondStr += card.value + ' '
            case 'C':
                clubStr += card.value + ' '
    return '\n' + spadeStr + '\n' + heartStr + '\n' + diamondStr + '\n' + clubStr     

def tablePosToScreen(userPos, inPos):
    match userPos:
        case 'north':
            if inPos == 'east':
                return 'left'
            return 'right'
        case 'east':
            if inPos == 'south':
                return 'left'
            return 'right'
        case 'south':
            if inPos == 'west':
                return 'left'
            return 'right'
        case 'west':
            if inPos == 'north':
                return 'left'
            return 'right'
    return ''

def displayCards(table, userPosition, window):
    positions = list(table.positions.keys())
    for position in positions:
        table.positions[position].playerHand.organizeHand()
        if table.findPartner(table.positions[userPosition]).position == position:
            window['-TOPPLAYER-'].update(f"{table.positions[position].name} ({position}){cardsToStr(table.positions[position].playerHand.cards)}")
        elif position == userPosition:
            window['-USERPLAYER-'].update(f"{table.positions[position].name} ({position}){cardsToStr(table.positions[position].playerHand.cards)}")
        else:
            screenPos = tablePosToScreen(userPosition, position)
            if screenPos == 'left':
                window['-LEFTPLAYER-'].update(f"{table.positions[position].name} ({position}){cardsToStr(table.positions[position].playerHand.cards)}")
            else:
                window['-RIGHTPLAYER-'].update(f"{table.positions[position].name} ({position}){cardsToStr(table.positions[position].playerHand.cards)}")

def addCPUcard(window, key, table, trick):
    # determine card played
    trick.cardsPlayed.append(table.positions[trick.whoseTurn].playerHand.playRandomCard(trick.suitToFollow))
    print(f"{table.positions[trick.whoseTurn].name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
    previousText = window[key].get()
    window[key].update(previousText + f"\nCard Played - {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}")

def playTrick(table, nextLeadPos, window, userPosition):
    trick = Trick(nextLeadPos, 'NT')
    print(f"\nPlaying a new trick. {table.positions[nextLeadPos].name} ({nextLeadPos}) will lead.")

    if table.findPartner(table.positions[userPosition]).position == nextLeadPos:
        addCPUcard(window, '-TOPPLAYER-', table, trick)
    elif table.positions[trick.whoseTurn].isCPU:
        layoutLocation = tablePosToScreen(userPosition, table.positions[trick.whoseTurn].position)
        keyString = '-' + layoutLocation.upper() + 'PLAYER-'
        addCPUcard(window, keyString, table, trick)

def playDeal(table, userPosition, window):
    deck = Deck()
    deck.shuffle()

    positions = list(table.positions.keys())
    nextLeadPos = random.choice(positions)

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
    layout_deal = [[sg.Output(size=(40, 5))],
                   [sg.Text('Top Player', key='-TOPPLAYER-')],
                   [sg.Text('Left Player', key='-LEFTPLAYER-'), sg.Text('Right Player', key='-RIGHTPLAYER-', justification='r')],
                   [sg.Text('User', key='-USERPLAYER-')]]
    
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