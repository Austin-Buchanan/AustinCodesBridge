# this file contains logic for the opponent AI

from card import Card

def findWinningHandCard(trick, player, table):
    winningCard = trick.findCurrentWinner()
    if winningCard is None:
        return None
    partner = table.findPartner(player)
    if partner.name == winningCard.ownerName:
        return None
    winningHandCard = Card('', '', '')
    for card in player.hand.cards:
        if winningHandCard.value == '' and (card.suit == trick.suitToFollow or card.suit == trick.trump):
            winningHandCard.copyCard(card)
        elif winningCard.compareCard(card, trick.suitToFollow, trick.trump) == card and card.compareCard(winningHandCard, trick.suitToFollow, trick.trump) == winningHandCard:
            winningHandCard.copyCard(card)
    if winningHandCard.value == '':
        return None
    return winningHandCard

def findThrowAwayCard(hand):
    throwCard = Card('', '', '')
    for card in hand.cards:
        if throwCard.value == '':
            throwCard.copyCard(card)
        elif throwCard.valueHierarchy.index(throwCard.value) > card.valueHierarchy.index(card.value):
            throwCard.copyCard(card)
    return throwCard
        