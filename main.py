from player import Player 

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

def fillEmptySeats(username, userPosition):
    otherPlayerNames = ['Allison', 'Blake', 'Catherine', 'Dylan']
    usedNames = [username]
    usedPositions = [userPosition]
    for i in range(4):
        newName = ''
        newPosition = ''
        if otherPlayerNames[i] in usedNames:
            usedNames.append(otherPlayerNames[i + 1])
            newName = otherPlayerNames[i + 1]
        else:   
            usedNames.append(otherPlayerNames[i])
            newName = otherPlayerNames[i]


def main():
    # play intro and initialize
    username, userPosition = intro()
    user = Player(username, False, userPosition)


if __name__ == "__main__":
    main()