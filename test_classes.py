from card import Card
from hand import Hand
from deck import Deck
from player import Player
from table import Table
from deal import Deal
from trick import Trick

#Test Card class
def test_card_init():
    testCard = Card('S', '7', 'Tester')
    assert testCard.suit == 'S' and testCard.value == '7' and testCard.ownerName == 'Tester'

def test_card_copy():
    testCard = Card('S', '7', 'Tester')
    newCard = Card('', '', '')
    newCard.copyCard(testCard)
    assert newCard.suit == 'S' and newCard.value == '7' and newCard.ownerName == 'Tester'

def test_compare_card_same_suit_NT():
    lowSpade = Card('S', '7', 'Tester')
    highSpade = Card('S', '8', 'NotTester')
    assert highSpade.compareCard(lowSpade, highSpade.suit, 'NT') == highSpade and lowSpade.compareCard(highSpade, lowSpade.suit, 'NT') == highSpade

def test_compare_card_diff_suit_NT():
    spadeCard = Card('S', '7', 'Tester')
    heartCard = Card('H', '9', 'NotTester')
    assert spadeCard.compareCard(heartCard, spadeCard.suit, 'NT') == spadeCard and spadeCard.compareCard(heartCard, heartCard.suit, 'NT') == heartCard

def test_compare_card_trumpSuit():
    spadeCard = Card('S', '7', 'Tester')
    heartCard = Card('H', '9', 'NotTester')
    assert spadeCard.compareCard(heartCard, spadeCard.suit, heartCard.suit) == heartCard

#Test Hand class
def test_hand_init():
    testCardA = Card('S', '7', 'Tester')
    testCardB = Card('D', 'K', 'Tester')
    testHand = Hand('Tester', [testCardA, testCardB])
    assert testHand.ownerName == 'Tester' and testHand.cards == [testCardA, testCardB]

def test_hand_removeCard():
    testCardA = Card('S', '7', 'Tester')
    testCardB = Card('D', 'K', 'Tester')
    testHand = Hand('Tester', [testCardA, testCardB])
    testHand.removeCard(testCardA)
    assert testHand.cards == [testCardB]

def test_hand_addCard():
    testCardA = Card('S', '7', 'Tester')
    testCardB = Card('D', 'K', 'Tester')
    testHand = Hand('Tester', [testCardA, testCardB])
    testCardC = Card('H', 'A', 'Tester')
    testHand.addCard(testCardC)
    assert testHand.cards == [testCardA, testCardB, testCardC]        

def test_hand_countHCP():
    testHand = Hand('Tester', [])
    cardStringList = [
        'SA', 'SQ', 'SJ', 'S2', 'HA', 'HQ', 'DK', 'DQ', 'D3', 'D2', 'CA', 'C4', 'C3'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Tester'))
    assert testHand.countHCP() == 22

def test_hand_organize_all():
    testHand = Hand('Tester', [])
    cardStringList = [
        'S2', 'ST', 'S4', 'SA',
        'H5', 'H2', 'HK', 
        'DT', 'DJ', 'D8', 
        'CA', 'C5', 'CK'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Tester'))
    testHand.organizeHand()
    assert testHand.cards[0].value == 'A' and testHand.cards[7].suit == 'D' and testHand.cards[12].value == '5'

def test_hand_play_random():
    testHand = Hand('Tester', [])
    cardStringList = [
        'S2', 'ST', 'S4', 'SA',
        'H5', 'H2', 'HK', 
        'DT', 'DJ', 'D8', 
        'CA', 'C5', 'CK'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Tester'))
    assert len(testHand.cards) == 13
    testCard = testHand.playRandomCard('D')
    assert len(testHand.cards) == 12 and testCard.suit == 'D'
    leadCard = testHand.playRandomCard('')
    assert leadCard not in testHand.cards   

def test_validate_card_choice():
    testHand = Hand('Tester', [])
    cardStringList = [
        'S2', 'ST', 'S4', 'SA',
        'H5', 'H2', 'HK', 
        'DT', 'DJ', 'D8', 
        'CA', 'C5', 'CK'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Tester'))
    assert testHand.validateCardChoice('H', 'H', 'K').value == 'K'
    assert testHand.validateCardChoice('H', 'D', 'T') is None
    assert testHand.validateCardChoice('', 'S', 'A').value == 'A'
    assert testHand.validateCardChoice('H', 'H', 'A') is None
    assert testHand.validateCardChoice('H', 'D', 'A') is None
    assert testHand.validateCardChoice('', 'D', '2') is None    

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
    testHand = Hand('Tester', [])
    cardStringList = [
        'SA', 'SQ', 'SJ', 'S2', 'HA', 'HQ', 'DK', 'DQ', 'D3', 'D2', 'CA', 'C4', 'C3'
    ]
    for cardString in cardStringList:
        testHand.addCard(Card(cardString[0], cardString[1], 'Tester'))
    testPlayer = Player('Tester', False, 'north', testHand)
    assert testPlayer.playerHand.countHCP() == 22

def test_player_win_trick():
    testPlayer = Player('Tester', True, 'south', None)
    testPlayer.winTrick()
    assert testPlayer.tricksWon == 1
    testPlayer.winTrick()
    assert testPlayer.tricksWon == 2

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

def test_table_find_player_pos():
    testerNorth = Player('testerNorth', False, 'north', None)
    testerEast = Player('testerEast', True, 'east', None)
    testerSouth = Player('testerSouth', True, 'south', None)
    testerWest = Player('testerWest', True, 'west', None)
    testTable = Table([testerNorth, testerEast, testerSouth, testerWest])
    assert testTable.findPlayerPos('testerSouth') == 'south'    

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
    assert testDeal.dealTable == testTable and testDeal.dealDeck == testDeck and testDeal.leader == 'north' and len(testDeal.dealTable.positions['north'].playerHand.cards) == 13 and len(testDeal.dealTable.positions['west'].playerHand.cards) == 13

# Test Trick
def test_trick_init():
    testTrick = Trick('west', 'NT')
    assert testTrick.whoseTurn == 'west' and testTrick.trump == 'NT'
    assert len(testTrick.cardsPlayed) == 0

def test_trick_next_turn():
    testTrick = Trick('north', 'NT')
    testTrick.nextTurn()
    assert testTrick.whoseTurn == 'east'
    testTrick.nextTurn()
    assert testTrick.whoseTurn == 'south'
    testTrick.nextTurn()
    assert testTrick.whoseTurn == 'west'

def test_trick_find_winner():
    testTrick = Trick('north', 'NT')
    testTrick.cardsPlayed.append(Card('S', '8', 'Austin'))
    testTrick.cardsPlayed.append(Card('C', '7', 'Allison'))
    testTrick.cardsPlayed.append(Card('H', 'K', 'Blake'))
    testTrick.cardsPlayed.append(Card('H', '8', 'Catherine'))
    assert testTrick.findTrickWinner().suit == testTrick.cardsPlayed[0].suit
    assert testTrick.findTrickWinner().value == testTrick.cardsPlayed[0].value