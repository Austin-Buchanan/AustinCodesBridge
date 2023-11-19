import random, time

# global constants
suits = ['C', 'D', 'H', 'S']
cardTypes = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
players = ["user", "LO", "partner", "RO"]

def fillDeck(deck):
    for suit in suits: 
        for cardType in cardTypes:
            deck.append(cardType + suit)

def shuffleDeck(deck):
    indexList = list(range(1, 53))
    newDeck = []
    for i in range(1, 53):
        newDeck.append('')
    for card in deck:
        index = random.choice(indexList)
        indexList.remove(index)
        newDeck[index - 1] = card
    return newDeck   

def dealCards(deck, hand1, hand2, hand3, hand4):
    counter = 0
    for i in range(0, 13):
        hand1.append(deck[counter])
        counter += 1
        hand2.append(deck[counter])
        counter += 1
        hand3.append(deck[counter])
        counter += 1
        hand4.append(deck[counter])
        counter += 1

def organizeHand(hand):
    cardType = ""
    nextCardType = ""
    suit = ""
    nextSuit = ""
    for i in range(0, 13):
        if i == 12:
            continue

        suit = hand[i][-1]
        nextSuit = hand[i + 1][-1]

        if len(hand[i]) == 3:
            cardType = hand[i][0:2]
        else:
            cardType = hand[i][0]

        if len(hand[i + 1]) == 3:
            nextCardType = hand[i + 1][0:2]
        else:
            nextCardType = hand[i + 1][0]        
      
        if suits.index(suit) < suits.index(nextSuit):
            hand[i], hand[i + 1] = hand[i + 1], hand[i]
        elif suits.index(suit) == suits.index(nextSuit) and cardTypes.index(cardType) < cardTypes.index(nextCardType):
            hand[i], hand[i + 1] = hand[i + 1], hand[i]

def printCards(cardList):
    stringToPrint = ""
    for card in cardList:
        stringToPrint += card + " "
    print(stringToPrint)

def displayHand(hand):
    print("\nYour hand:")
    spades = []
    hearts = []
    diamonds = []
    clubs = []    
    for card in hand:
        if card[-1] == 'S':
            spades.append(card)
        elif card[-1] == 'H':
            hearts.append(card)
        elif card[-1] == 'D':
            diamonds.append(card)
        elif card[-1] == 'C':
            clubs.append(card)
    printCards(spades)
    printCards(hearts)
    printCards(diamonds)
    printCards(clubs)
    print('\n')
    time.sleep(0.5)

def findWhoLeads(tricksPlayed, lastTrickWinner, declarer):
    if tricksPlayed > 0:
        return lastTrickWinner
    elif declarer == players[3]:
        return players[0]
    else:
        return players[players.index(declarer) + 1]

def cpuLeads(cpuHand, cardsPlayedInTrick):
    cardToPlay = random.choice(cpuHand)
    cpuHand.remove(cardToPlay)
    cardsPlayedInTrick.append(cardToPlay)
    return cardToPlay

def userLeads(userHand, cardsPlayedInTrick):
    displayHand(userHand)
    cardToPlay = input("Which card do you want to play?")
    if cardToPlay in userHand:
        userHand.remove(cardToPlay)
        cardsPlayedInTrick.append(cardToPlay)
    return cardToPlay

def verifyCardToPlay(cardToPlay, cardsPlayedInTrick, playerHand):
    suitLead = cardsPlayedInTrick[0][-1]
    if cardToPlay[-1] == suitLead:
        return True
    else:
        for card in playerHand:
            if card[-1] == suitLead:
                return False
    return True

def playCard(player, playerHand, cardsPlayedInTrick):
    validChoice = False
    if player == players[0]:
        displayHand(playerHand)
        while not validChoice:
            cardToPlay = input("Which card do you want to play? ")
            validChoice = verifyCardToPlay(cardToPlay, cardsPlayedInTrick, playerHand)
            if not validChoice:
                print("Please follow suit.")
                time.sleep(0.5)
    else:
        while not validChoice:
            cardToPlay = random.choice(playerHand)
            validChoice = verifyCardToPlay(cardToPlay, cardsPlayedInTrick, playerHand)
    playerHand.remove(cardToPlay)
    cardsPlayedInTrick.append(cardToPlay)
    return cardToPlay    

def findCardValue(card):
    if len(card) > 2:
        return card[0:2]
    else:
        return card[0]

def compareCards(cardA, cardB):
    valCardA = findCardValue(cardA)
    valCardB = findCardValue(cardB)
    if valCardA > valCardB:
        return cardA
    else: 
        return cardB

def findTrickWinner(cardsPlayedInTrick):
    suitLead = cardsPlayedInTrick[0][-1]
    winningCard = ""
    for i in range(len(cardsPlayedInTrick)):
        if i == 0:
            winningCard = cardsPlayedInTrick[0]
        elif cardsPlayedInTrick[i][-1] != suitLead:
            continue
        else:
            winningCard = compareCards(winningCard, cardsPlayedInTrick[i])
    return winningCard

def playTrick(userHand, loHand, partnerHand, roHand, whoLeads):
    cardPlayed = ""
    cardsPlayedInTrick = []
    
    # Handle leading
    if whoLeads == players[0]:
        cardPlayed = userLeads(userHand, cardsPlayedInTrick)
    elif whoLeads == players[1]:
        cardPlayed = cpuLeads(loHand, cardsPlayedInTrick)
    elif whoLeads == players[2]:
        cardPlayed = cpuLeads(partnerHand, cardsPlayedInTrick)
    elif whoLeads == players[3]:
        cardPlayed = cpuLeads(roHand, cardsPlayedInTrick)
    print(f"{whoLeads} leads with {cardPlayed}.")
    time.sleep(0.5)

    # Other players play
    leadIndex = players.index(whoLeads)
    for i in range(3):
        # Determine whose turn it is
        turnIndex = leadIndex + len(cardsPlayedInTrick)
        if turnIndex > 3:
            turnIndex = turnIndex - 4

        # player whose turn it is plays
        if turnIndex == 0:
            cardPlayed = playCard(players[0], userHand, cardsPlayedInTrick)
        elif turnIndex == 1:
            cardPlayed = playCard(players[1], loHand, cardsPlayedInTrick)
        elif turnIndex == 2:
            cardPlayed = playCard(players[2], partnerHand, cardsPlayedInTrick)
        elif turnIndex == 3:
            cardPlayed = playCard(players[3], roHand, cardsPlayedInTrick)
        print(f"{players[turnIndex]} plays {cardPlayed}")
        time.sleep(0.5)

    # Determine trick winner 
    winningCard = findTrickWinner(cardsPlayedInTrick)
    winnerIndex = leadIndex + cardsPlayedInTrick.index(winningCard)
    if winnerIndex > 3:
        winnerIndex = winnerIndex - 4
    whoWon = players[winnerIndex]

    print(f"{whoWon} wins with {winningCard}")
    time.sleep(0.5)
    return whoWon

def main():
    # variables
    deck = []
    userHand = []
    loHand = []
    partnerHand = []
    roHand = []
    tricksPlayed = 0
    whoLeads = ""

    print("Playing bridge.")
    time.sleep(0.5)
    
    # Deal cards
    print("Dealing cards.")
    time.sleep(0.5)
    fillDeck(deck)
    deck = shuffleDeck(deck)
    dealCards(deck, userHand, loHand, partnerHand, roHand)

    # Organize and display user hand
    print("Organizing your hand.")
    time.sleep(0.5)
    for i in range(0, len(userHand)):
        organizeHand(userHand)
    displayHand(userHand)

    # randomly pick a declarer. Change to non-random after bidding is introduced.
    declarer = random.choice(players)
    print(f"{declarer} is the declarer.")
    time.sleep(0.5)

    # start playing
    while tricksPlayed < 13:
        # play trick
        if whoLeads == "":
            # get index of declarer in players
            declarerIndex = players.index(declarer)
            # add 1 to that index to get whoLeads, wrapping the end of the list to the front
            if declarerIndex == 3:
                whoLeads = players[0]
            else:
                whoLeads = players[declarerIndex + 1]
        whoLeads = playTrick(userHand, loHand, partnerHand, roHand, whoLeads)

        tricksPlayed += 1


if __name__ == "__main__":
    main()
