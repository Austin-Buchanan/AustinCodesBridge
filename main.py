from player import Player 

def main():
    playerNames = ['user', 'leftOpponent', 'partner', 'rightOpponent']

    # initialize players and deck
    players = []
    for name in playerNames:
        if name == 'user':
            players.append(Player('user', False))
        else:
            players.append(Player(name, True))

if __name__ == "__main__":
    main()