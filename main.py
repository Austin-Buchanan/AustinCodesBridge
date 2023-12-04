from player import Player 
from deck import Deck
from deal import Deal
import random

# constants
positions = ['north', 'east', 'south', 'west']

def intro():
    print("Let's play bridge!")
    username = input('Enter your name: ')
    print(f"Welcome, {username}! ")
    userPosition = input('Would you like to sit north, east, west, or south?: ')
    while userPosition not in positions:
        print('Sorry, that is not a valid position.')
        userPosition = input('Would you like to sit north, east, west, or south?: ')
    return username, userPosition

def fillEmptySeats(players):
    otherPlayerNames = ['Allison', 'Blake', 'Catherine', 'Dylan']
    usedNames = [players[0].name]
    openPositions = positions
    openPositions.remove(players[0].position)
    for i in range(3):
        newName = ''
        newPosition = openPositions[0]
        openPositions.remove(openPositions[0])
        if otherPlayerNames[i] in usedNames:
            usedNames.append(otherPlayerNames[i + 1])
            newName = otherPlayerNames[i + 1]
        else:   
            usedNames.append(otherPlayerNames[i])
            newName = otherPlayerNames[i]
        newPlayer = Player(newName, True, newPosition)
        players.append(newPlayer)
        print(f"{newPlayer.name} is playing {newPlayer.position}")        

def playDeal(players):
    # initialize and shuffle deck
    deck = Deck()
    deck.shuffle()

    # randomly determine who leads first (eventually replace with bidding)
    firstLeaderName = random.choice(players).name

    # initialize deal
    deal = Deal(players, deck, firstLeaderName)

    # play tricks


def main():
    # play intro and initialize
    players = []
    username, userPosition = intro()
    user = Player(username, False, userPosition)
    players.append(user)
    fillEmptySeats(players)
    print(f"Your partner will be {user.getPartner(players).name}")

    playing = True
    while playing:
        print('\n Playing a new deal . . . ')
        playDeal(players)
        if input("Continue? Enter 'yes' or 'no': ") == 'no':
            playing = False

if __name__ == "__main__":
    main()