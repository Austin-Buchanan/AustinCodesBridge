from player import Player 
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
from trick import Trick
from displayUtilities import printDeck, printHand, printTrickScore
import random
import sys

def checkAdminMode():
    if len(sys.argv) > 1 and sys.argv[1] == 'admin':
        return True
    return False

def intro(positions):
    print("Let's play bridge!")
    username = input('Enter your name: ')
    print(f"Welcome, {username}! ")
    userPosition = input('Would you like to sit north, east, west, or south?: ')
    while userPosition not in positions:
        print('Sorry, that is not a valid position.')
        userPosition = input('Would you like to sit north, east, west, or south?: ')
    return username, userPosition

def fillEmptySeats(tableIn, username):
    otherPlayerNames = ['Allison', 'Blake', 'Catherine', 'Dylan']
    if username in otherPlayerNames:
        otherPlayerNames.remove(username)
    for i in range(3):
        emptyPosStr = ''
        if tableIn.positions['north'] is None:
            emptyPosStr = 'north'
        elif tableIn.positions['east'] is None:
            emptyPosStr = 'east'
        elif tableIn.positions['south'] is None:
            emptyPosStr = 'south'
        elif tableIn.positions['west'] is None:
            emptyPosStr = 'west'
        newPlayer = Player(otherPlayerNames[0], True, emptyPosStr, Hand(otherPlayerNames[0], []))
        otherPlayerNames.remove(newPlayer.name)
        tableIn.addPlayer(newPlayer)
        print(f"{newPlayer.name} is playing {newPlayer.position}")

def inputCardParse(cardString):
    suit = ''
    value = ''
    suit = cardString[0]
    value = cardString[1]
    return suit, value

def playUserCard(userHand, currentTrick):
    suitToFollow = ''
    if len(currentTrick.cardsPlayed) > 0:
        suitToFollow = currentTrick.cardsPlayed[0].suit
    validChoice = False
    inputSuit = ''
    inputValue = ''
    while not validChoice:
        printHand(userHand)
        userInput = input('Enter a card from your hand: ')
        if len(userInput) > 2:
            print('Please enter your input with the format suit + value, like S7 for seven of spades or DK for king of diamonds.')
            continue
        else:
            inputSuit, inputValue = inputCardParse(userInput)
        cardChosen = userHand.validateCardChoice(suitToFollow, inputSuit, inputValue)
        if cardChosen is not None:
            validChoice = True
            currentTrick.cardsPlayed.append(cardChosen)
            userHand.removeCard(cardChosen)
        if not validChoice:
            print('Please enter a valid card from your hand.')    

def playTrick(tableIn, nextLeadPos, adminMode):
    trick = Trick(nextLeadPos, 'NT')
    suitToFollow = ''
    while len(trick.cardsPlayed) < 4:
        if adminMode:
            print('\nCards played in trick:')
            outString = ''
            for card in trick.cardsPlayed:
                outString += f"{card.suit + card.value} "
            print(outString)

        if len(trick.cardsPlayed) == 1:
            suitToFollow = trick.cardsPlayed[0].suit

        if tableIn.positions[trick.whoseTurn].isCPU:
            if adminMode:
                printHand(tableIn.positions[trick.whoseTurn].playerHand)
            trick.cardsPlayed.append(tableIn.positions[trick.whoseTurn].playerHand.playRandomCard(suitToFollow))
            print(f"{tableIn.positions[trick.whoseTurn].name} plays {trick.cardsPlayed[-1].suit + trick.cardsPlayed[-1].value}.")
        else:
            print('\nIt\'s your turn to play.')
            playUserCard(tableIn.positions[trick.whoseTurn].playerHand, trick)
        trick.nextTurn()
    return trick.findTrickWinner()

def playDeal(tableIn, positions, userPosition, adminMode):
    # initialize and shuffle deck
    deck = Deck()
    if adminMode:
        printDeck(deck)
    deck.shuffle()
    if adminMode:
        printDeck(deck)

    # randomly determine who leads first (eventually replace with bidding)
    nextLeadPos = random.choice(positions)

    # initialize deal
    deal = Deal(tableIn, deck, nextLeadPos)
    print('\nHere is your hand.')
    printHand(tableIn.positions[userPosition].playerHand)

    # play tricks
    while deal.tricksPlayed < 13:
        print(f"\nPlaying a new trick. {tableIn.positions[nextLeadPos].name} ({nextLeadPos}) will lead.")
        winningCard = playTrick(tableIn, nextLeadPos, adminMode)
        print(f"{winningCard.ownerName} wins!")
        tableIn.positions[tableIn.findPlayerPos(winningCard.ownerName)].winTrick()
        tableIn.findPartner(tableIn.positions[tableIn.findPlayerPos(winningCard.ownerName)]).winTrick()
        deal.tricksPlayed += 1
        nextLeadPos = tableIn.findPlayerPos(winningCard.ownerName)
        printTrickScore(tableIn)

def main():
    # check for admin mode, which logs all hands and info to console
    adminMode = checkAdminMode()
    if adminMode:
        print('Starting program in admin mode.')

    # play intro and initialize
    mainTable = Table([])
    positions = list(mainTable.positions.keys())
    username, userPosition = intro(positions)
    user = Player(username, False, userPosition, Hand(username, []))
    mainTable.addPlayer(user)
    fillEmptySeats(mainTable, username)
    partnerName = mainTable.findPartner(user).name
    print(f"Your partner will be {partnerName}")

    playing = True
    while playing:
        print('\n Playing a new deal . . . ')
        playDeal(mainTable, positions, userPosition, adminMode)
        if input("Continue? Enter 'yes' or 'no': ") == 'no':
            playing = False

if __name__ == "__main__":
    main()