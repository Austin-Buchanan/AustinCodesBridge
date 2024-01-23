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

# def intro(positions):
#     layout = [
#         [sg.Text("Let's play bridge!\nEnter you name: ")],
#         [sg.Input('', enable_events=True, key='-InputName-', expand_x=True)]
#     ]
#     window = sg.Window("Demo", layout)

#     while True:
#         event, values = window.read()
#         if event == "OK" or event == sg.WIN_CLOSED:
#             break

def main():
    mainTable = Table([])
    positions = list(mainTable.positions.keys())
    # username, userPosition = intro(positions)

    sg.theme('BluePurple')
    layout = [[sg.Text("Let's play bridge!\nEnter your name: "), sg.Text(size=(15,1), key='-INTRO-')],
              [sg.Input(key='-NAME-')],
              [sg.Text('Where would you like to sit?'), sg.Text(size=(15,1), key='-QPOSITION-')],
              [sg.Combo(positions, key='-POSITION-')],
              [sg.Button('Start')],
              [sg.Text(''), sg.Text( key='-ERRORTEXT-')],
              [sg.Button('Exit')]]
    
    window = sg.Window('Austin Codes Bridge', layout)

    while True: 
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Start':
            if values['-NAME-'] != '' and values['-POSITION-'] != '':
                window['-ERRORTEXT-'].update('No error detected.')
            else:
                window['-ERRORTEXT-'].update('Please enter your name and select a position before clicking Start.')


if __name__ == "__main__":
    main()