from card import Card
from hand import Hand
from deck import Deck
from player import Player
from table import Table
from deal import Deal

#Test Card class
def test_card_init():
    testCard = Card('S', '7', 'Austin')
    assert testCard.suit == 'S' and testCard.value == '7' and testCard.ownerName == 'Austin'

def test_card_copy():
    testCard = Card('S', '7', 'Austin')
    newCard = Card('', '', '')
    newCard.copyCard(testCard)
    assert newCard.suit == 'S' and newCard.value == '7' and newCard.ownerName == 'Austin'

def test_compare_card_same_suit_NT():
    lowSpade = Card('S', '7', 'Austin')
    highSpade = Card('S', '8', 'NotAustin')
    assert highSpade.compareCard(lowSpade, highSpade.suit, 'NT') == highSpade and lowSpade.compareCard(highSpade, lowSpade.suit, 'NT') == highSpade

def test_compare_card_diff_suit_NT():
    spadeCard = Card('S', '7', 'Austin')
    heartCard = Card('H', '9', 'NotAustin')
    assert spadeCard.compareCard(heartCard, spadeCard.suit, 'NT') == spadeCard and spadeCard.compareCard(heartCard, heartCard.suit, 'NT') == heartCard

def test_compare_card_trumpSuit():
    spadeCard = Card('S', '7', 'Austin')
    heartCard = Card('H', '9', 'NotAustin')
    assert spadeCard.compareCard(heartCard, spadeCard.suit, heartCard.suit) == heartCard

#Test Hand class
def test_hand_init():
    testCardA = Card('S', '7', 'Austin')
    testCardB = Card('D', 'K', 'Austin')
    testHand = Hand('Austin', [testCardA, testCardB])
    assert testHand.ownerName == 'Austin' and testHand.cards == [testCardA, testCardB]

def test_hand_removeCard():
    testCardA = Card('S', '7', 'Austin')
    testCardB = Card('D', 'K', 'Austin')
    testHand = Hand('Austin', [testCardA, testCardB])
    testHand.removeCard(testCardA)
    assert testHand.cards == [testCardB]

def test_hand_addCard():
    testCardA = Card('S', '7', 'Austin')
    testCardB = Card('D', 'K', 'Austin')
    testHand = Hand('Austin', [testCardA, testCardB])
    testCardC = Card('H', 'A', 'Austin')
    testHand.addCard(testCardC)
    assert testHand.cards == [testCardA, testCardB, testCardC]        

def test_hand_countHCP():
    testHand = Hand('Austin', [])
    cardStringList = [
        'SA', 'SQ', 'SJ', 'S2', 'HA', 'HQ', 'DK', 'DQ', 'D3', 'D2', 'CA', 'C4', 'C3'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Austin'))
    assert testHand.countHCP() == 22

#Test Deck class
def test_deck_init():
    testCard = Card('H', 'A', '')
    testDeck = Deck()
    foundCard = False
    for deckCard in testDeck.cardList:
        if deckCard.suit == testCard.suit and deckCard.value == testCard.value:
            foundCard = True
            break
    assert foundCard

def test_deck_shuffle():
    testDeck = Deck()
    firstShuffle = testDeck.cardList
    testDeck.shuffle()
    secondShuffle = testDeck.cardList
    assert firstShuffle != secondShuffle

#Test Player
def test_player_init_empty_hand():
    testPlayer = Player('Tester', True, 'south', None)
    assert testPlayer.name == 'Tester' and testPlayer.isCPU and testPlayer.position == 'south' and testPlayer.gameScore == 0 and testPlayer.tricksWon == 0 and testPlayer.playerHand == None

def test_player_init_full_hand():
    testHand = Hand('Austin', [])
    cardStringList = [
        'SA', 'SQ', 'SJ', 'S2', 'HA', 'HQ', 'DK', 'DQ', 'D3', 'D2', 'CA', 'C4', 'C3'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Austin'))
    testPlayer = Player('Austin', False, 'north', testHand)
    assert testPlayer.playerHand.countHCP() == 22

#Test Table
def test_table_init_empty():
    testTable = Table([])
    assert testTable.positions['north'] == None and testTable.positions['west'] == None

def test_table_init_full():
    testerNorth = Player('testerNorth', False, 'north', None)
    testerEast = Player('testerEast', True, 'east', None)
    testerSouth = Player('testerSouth', True, 'south', None)
    testerWest = Player('testerWest', True, 'west', None)
    testTable = Table([testerNorth, testerEast, testerSouth, testerWest])
    assert testTable.positions['north'].isCPU == False and testTable.positions['west'].name == 'testerWest'

def test_table_find_partner():
    testerNorth = Player('testerNorth', False, 'north', None)
    testerEast = Player('testerEast', True, 'east', None)
    testerSouth = Player('testerSouth', True, 'south', None)
    testerWest = Player('testerWest', True, 'west', None)
    testTable = Table([testerNorth, testerEast, testerSouth, testerWest])
    assert testTable.findPartner(testerEast) == testerWest

# Test Deal
def test_deal_init():
    northHand = Hand('testerNorth', [])
    testerNorth = Player('testerNorth', False, 'north', northHand)
    eastHand = Hand('testerEast', [])
    testerEast = Player('testerEast', True, 'east', eastHand)
    southHand = Hand('testerSouth', [])
    testerSouth = Player('testerSouth', True, 'south', southHand)
    westHand = Hand('testerWest', [])
    testerWest = Player('testerWest', True, 'west', westHand)
    testTable = Table([testerNorth, testerEast, testerSouth, testerWest])
    testDeck = Deck()
    testDeal = Deal(testTable, testDeck, 'north')
    assert testDeal.dealTable == testTable and testDeal.dealDeck == testDeck and testDeal.firstLeadPos == 'north' and len(testDeal.dealTable.positions['north'].playerHand.cards) == 13 and len(testDeal.dealTable.positions['west'].playerHand.cards) == 13