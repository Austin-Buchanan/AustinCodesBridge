from card import Card

def test_card_init():
    testCard = Card('S', '7', 'Austin')
    assert testCard.suit == 'S' and testCard.value == '7' and testCard.owner == 'Austin'

def test_card_copy():
    testCard = Card('S', '7', 'Austin')
    newCard = Card('', '', '')
    newCard.copyCard(testCard)
    assert newCard.suit == 'S' and newCard.value == '7' and newCard.owner == 'Austin'

def test_compare_card():
    lowSpade = Card('S', '7', 'Austin')
    highSpade = Card('S', '8', 'Austin')
    assert highSpade.compareCard(lowSpade, highSpade.suit, 'NT') == highSpade and lowSpade.compareCard(highSpade, lowSpade.suit, 'NT') == highSpade
