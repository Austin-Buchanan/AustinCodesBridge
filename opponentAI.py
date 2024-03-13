# this file contains logic for the opponent AI

from card import Card

def findWinningHandCard(trick, hand):
    if len(trick.cardsPlayed) == 0:
        return None
    winningCard = Card('', '', '')
    for trickCard in trick.cardsPlayed:
        if winningCard.value == '':
            winningCard.copyCard(trickCard)
        elif winningCard.compareCard(trickCard, trick.suitToFollow, trick.trump) == trickCard:
            winningCard.copyCard(trickCard)
    # TO DO: use an algorithm to find the lowest value card in the hand that beats the winning card in the trick

