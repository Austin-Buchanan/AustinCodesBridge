from player import Player
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
from trick import Trick
import random, sys
import PySimpleGUI as sg 

# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
# window = sg.Window("Demo", layout)

# while True:
#     event, values = window.read()
#     if event == "OK" or event ==sg.WIN_CLOSED:
#         break

# window.close()

def intro(positions):
    layout = [
        [sg.Text("Let's play bridge!\nEnter you name: ")],
        [sg.Input('', enable_events=True, key='-InputName-', expand_x=True)]
    ]
    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break

def main():
    mainTable = Table([])
    positions = list(mainTable.positions.keys())
    username, userPosition = intro(positions)

if __name__ == "__main__":
    main()