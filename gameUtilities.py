# These are functions used by the GUI version of the app. 
# They are operations used while running the game but do not directly relate to game flow. 

from player import Player
from hand import Hand
from deck import Deck
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

def checkIfCard(strIn):
    if strIn[0] not in Deck.suits:
        return False
    if strIn[1] not in Deck.cardValues:
        return False
    return True

def readUserInput(window):
    validSubmission = False
    userInput = ''
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Submit':
            print('Reading your input.')
            userInput = values['-USERINPUT-'].strip().upper()
            print('Your input was ' + userInput)
            if len(userInput) != 2:
                print('Your submission was poorly formatted. Please enter the character for the suit followed by the character for the card value. For example, to submit the ace of spades, enter SA')
                break
            elif not checkIfCard(userInput):
                print('Your submission was not a valid card. Please try again.')
                break
            else:
                validSubmission = True
                break
    window['-USERINPUT-'].update('')
    if not validSubmission:
        readUserInput(window)
    return userInput

def checkHasSuit(hand, suitIn):
    for card in hand.cards:
        if card.suit == suitIn:
            return True
    return False

def incrementScore(position, deal):
    match position:
        case 'east' | 'west':
            deal.scoreEW += 1
        case 'north' | 'south':
            deal.scoreNS += 1