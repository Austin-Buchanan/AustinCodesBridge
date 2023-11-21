
class Deal:
    suits = ['C', 'D', 'H', 'S']
    cardTypes = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []

    def __init__(self, players):
        self.players = players
        
