# These are functions used by the GUI version of the app. 
# They are operations used while running the game but do not directly relate to game flow. 

from player import Player
from hand import Hand
from deck import Deck
import PySimpleGUI as sg
import random

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
    return spadeStr + '\n' + heartStr + '\n' + diamondStr + '\n' + clubStr     

def tablePosToScreen(userPos, inPos):
    match userPos:
        case 'north':
            if inPos == 'east':
                return 'left'
            elif inPos == 'south':
                return 'top'
            elif inPos == 'west':
                return 'right'
            return 'user'
        case 'east':
            if inPos == 'south':
                return 'left'
            elif inPos == 'west':
                return 'top'
            elif inPos == 'north':
                return 'right'
            return 'user'
        case 'south':
            if inPos == 'west':
                return 'left'
            elif inPos == 'north':
                return 'top'
            elif inPos == 'east':
                return 'right'
            return 'user'
        case 'west':
            if inPos == 'north':
                return 'left'
            elif inPos == 'east':
                return 'top'
            elif inPos == 'south':
                return 'right'
            return 'user'
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
        elif event == 'Submit' or event == '-USERINPUT-Enter':
            print('Reading your input.')
            userInput = values['-USERINPUT-'].strip().upper()
            print('Your input was ' + userInput)
            if userInput == 'LOW':
                print('Following suit and playing low.')
                validSubmission = True
                break
            elif userInput == 'HIGH':
                print('Following suit and playing high.')
                validSubmission = True
                break
            elif len(userInput) != 2:
                print('Your submission was poorly formatted. Please enter the character for the suit followed by the character for the card value. For example, to submit the ace of spades, enter SA')
                readUserInput(window)
                break
            elif not checkIfCard(userInput):
                print('Your submission was not a valid card. Please try again.')
                readUserInput()
                break
            else:
                validSubmission = True
                break
        elif event == 'Play Low':
            print('Following suit and playing low.')
            userInput = 'play-low'
            validSubmission = True
            break
        elif event == 'Play High':
            print('Following suit and playing high.')
            userInput = 'play-high'
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

def determineTrump(table, userPosition):
    # create a collection of cards by suit composed of the user's hand and their partners
    combinedHands = {
        'S': [],
        'H': [],
        'D': [],
        'C': []  
    }
    userPlayer = table.positions[userPosition]
    for card in userPlayer.playerHand.cards:
        combinedHands[card.suit].append(card)
    partner = table.findPartner(userPlayer)
    for card in partner.playerHand.cards:
        combinedHands[card.suit].append(card)
    suits = combinedHands.keys()
    suitMajorities = []
    for suit in suits:
        if len(combinedHands[suit]) >= 8:
            suitMajorities.append(suit)
    suitMajorityCount = len(suitMajorities)
    match suitMajorityCount:
        case 0:
            return 'NT'
        case 1:
            return suitMajorities[0]
        case 2 | 3:
            suitLengths = []
            for i in range(suitMajorityCount):
                suitLengths.append(len(combinedHands[suitMajorities[i]]))
            largestLength = max(suitLengths)
            largestFrequency = suitLengths.count(largestLength)
            if largestFrequency == 1:
                return suitMajorities[suitLengths.index(largestLength)]
            candidateIndices = [i for i, x in enumerate(suitLengths) if x == largestLength]
            for index in candidateIndices:
                if suitMajorities[index] == 'S' or suitMajorities[index] == 'H':
                    return suitMajorities[index]
            return random.choice(suitMajorities)

def playLow(hand, trick):
    lowCard = hand.lowCard(trick.suitToFollow)
    if lowCard is None:
        return None
    trick.cardsPlayed.append(hand.playCard(lowCard.suit, lowCard.value))
    return 'success'

def playHigh(hand, trick):
    highCard = hand.highCard(trick.suitToFollow)
    if highCard is None:
        return None
    trick.cardsPlayed.append(hand.playCard(highCard.suit, highCard.value))
    return 'success'

def findLeaderPosition(userPosition):
    positions = ['north', 'east', 'south', 'west']
    userIndex = positions.index(userPosition)
    if userIndex == 3:
        return positions[0]
    else:
        return positions[userIndex + 1]