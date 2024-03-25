# AustinCodesBridge

## Description
This is a desktop application to play bridge with a 52 card deck. The application was written in Python using the PySimpleGUI library to create the desktop GUI. The game runs with the user in the declarer position and their partner in the dummy position. 

See the following Wikipedia article if you need an explanation for bridge: [https://en.wikipedia.org/wiki/Contract_bridge](https://en.wikipedia.org/wiki/Contract_bridge)

Currently the application only supports trick-taking, not bidding, although I may consider adding bidding at a later date. 

Here is what the application looks like in action:

![Demo Recording](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/AustinCodesBridge_Demo.gif)

## Motivation
In my elementary school's gifted program, there was a unit to teach students how to play contract bridge. Bridge is an intellectually stimulating card game, especially when played competitively, and the unit had the end goal of readying students to compete in a youth tournament hosted by the American Contract Bridge League (ACBL). See [https://www.acbl.org/](https://www.acbl.org/) for more information on the ACBL. 

I enjoyed learning and playing bridge but didn't think I was an exceptional player. I was surprised, then, when my bridge partner and I won the tournament at the end of the unit. I returned to the tournament yearly until I was 16 or so, placing first or second each year I participated. I thought I might be good at this game after all. 

My enthusiasm for the game didn't last, unfortunately. As a teenager in high school, I found the culture surrounding adult bridge a little disagreeable for a couple reasons. First, there were very few players in adult bridge tournaments who were near my age. Second, adult partners were much more critical or condescending about mistakes I made while playing. Adult tournaments were more competitive than the youth tournaments, so I also wasn't winning like I had been before. I gave it a couple attempts after I'd aged out of the youth tournaments, but with my enthusiasm dwindling and my performance taking a hit, I decided to let bridge go. 

I took up bridge casually again in college while playing with friends--I taught the game to them one night while hanging out, playing cards. I'd tired of the card games that were luck based and wanted something where I had to think more, like bridge.

Since then, I've become interested in bridge again, and I decided that I'd make a bridge app to practice without the stress of a competitive environment or teach the game to a new group of friends. I needed a project to practice building a GUI in Python with, too, and so AustinCodesBridge was born. 

## Quick Start 
The quickest way to start the app is to clone the GitHub repository and run the main.py file from a command line. You'll need Python installed on your machine.

> git clone https://github.com/Austin-Buchanan/AustinCodesBridge

> py main.py

## Usage
After running main.py, the start screen will appear. On this screen, you will enter your name and select a position (north, south, east, or west) from a dropdown menu. Once this information is filled out, click the Start button. 

![Start Screen](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/Start_Screen.png)

If the name and position information is invalid, a warning will appear prompting you to try again. Otherwise, the start screen will be replaced with the playing screen.

![Playing Screen](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/Deal_Screen.png)

The top of the window is a PySimpleGUI output element populated with new information throughout the game. At the start of the game, it will print the names of each player and their position. Each time a new deal is played, it will state the trump suit. For each new trick within a deal, it will state the trick leader and any cards played. 

Below the output element are text fields that are updated throughout the game. The trump suit, partner pair scoring, and an indicator for whose turn is next are here. 

Beneath those text fields is the player area. Your partner will always be at the top of the area, your opponents to the sides, and you at the bottom, as if you are sitting at a bridge table. Each player has their own subarea with their name and the position (north, south, etc.) that they are sitting in. You will be able to see your cards and your partners cards, but the opponents' cards will be hidden. If the player has played a card in the current trick, additional text will appear at the bottom of the player area indicating the card they played. Furthermore, if it's the player's turn, their name and position will be surrounded by double asterisks (**).

![Hand Example](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/Hand_Example.png)

The display for a player's hand, if visible, will be divided by suit, abbreviated by the first letter of the suit. The cards will be represented either by a single digit number or the first letter of the card name. For example, in the above picture, Blake has an Ace of Diamonds represented by `D: A`. 

Below the player areas is the player input area. This consists of a text input field and three buttons: Submit, Play Low, and Play High. 

![Player Input Area](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/Player_Input.png)

When it's your turn or you're selecting which card your partner can play, type the suit abbrevioation followed by the single digit number along with the first letter of the card. This can be capitalized or lowercase. To play the Ace of Spades, for example, enter `sa` into this field. Then either hit the enter key or click Submit. 

If you're not playing the first card in a trick, you can also use the Play Low or Play High buttons to quickly play the highest or lowest card you or your partner has that follows suit. You can also type `high` or `low` in the text input field for the same operation. If there is no card that follows suit, or you are selecting the first card to play in the trick, you will have to type out the card to play. 

At the end of the deal, the output area will say which partner pair has won the deal. A Play Again button will appear at the top of the window--click on this to start a new deal and continue playing. Otherwise, click on the Exit button at the bottom of the window or close out of the program. 

![Play Again Example](https://github.com/Austin-Buchanan/AustinCodesBridge/blob/main/Images_and_Videos/Play_Again_Example.png)
