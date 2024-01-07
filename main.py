from player import Player 
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
from trick import Trick
import random

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

def printHand(hand):
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
        print('\nHere is your current hand.')
        printHand(userHand)
        userInput = input('Enter a card from your hand: ')
        if len(userInput) > 2:
            print('Please enter your input with the format suit + value, like S7 for seven of spades or DK for king of diamonds.')
            continue
        else:
            inputSuit, inputValue = inputCardParse(userInput)
        for card in userHand.cards:
            if inputSuit == card.suit and inputValue == card.value:
                validChoice = True
                currentTrick.cardsPlayed.append(card)
                userHand.removeCard(card)
        if not validChoice:
            print('Please enter a card that is from your hand.')
                

def playDeal(tableIn, positions, userPosition):
    # initialize and shuffle deck
    deck = Deck()
    deck.shuffle()

    # randomly determine who leads first (eventually replace with bidding)
    nextLeadPos = random.choice(positions)

    # initialize deal
    deal = Deal(tableIn, deck, nextLeadPos)
    print('\nHere is your hand.')
    printHand(tableIn.positions[userPosition].playerHand)

    # play tricks
    while deal.tricksPlayed < 13:
        newTrick = Trick(nextLeadPos, 'NT')
        while len(newTrick.cardsPlayed) < 4:
            if tableIn.positions[newTrick.whoseTurn].isCPU:
                newTrick.cardsPlayed.append(tableIn.positions[newTrick.whoseTurn].playerHand.playRandomCard())
                print(f"{tableIn.positions[newTrick.whoseTurn].name} plays {newTrick.cardsPlayed[-1].suit + newTrick.cardsPlayed[-1].value}.")
            else:
                playUserCard(tableIn.positions[newTrick.whoseTurn].playerHand, newTrick)
            newTrick.nextTurn()
        
        # Determine trick winner
            
            
        deal.tricksPlayed += 1

def main():
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
        playDeal(mainTable, positions, userPosition)
        if input("Continue? Enter 'yes' or 'no': ") == 'no':
            playing = False

if __name__ == "__main__":
    main()