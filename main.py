from player import Player 
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
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

def playDeal(tableIn, positions):
    # initialize and shuffle deck
    deck = Deck()
    deck.shuffle()

    # randomly determine who leads first (eventually replace with bidding)
    firstLeadPos = random.choice(positions)

    # initialize deal
    deal = Deal(tableIn, deck, firstLeadPos)

    # play tricks


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
        playDeal(mainTable, positions)
        if input("Continue? Enter 'yes' or 'no': ") == 'no':
            playing = False

if __name__ == "__main__":
    main()