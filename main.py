from player import Player
from deck import Deck
from deal import Deal
from table import Table
from hand import Hand
from trick import Trick
import random, sys
import PySimpleGUI as sg 

def main():
    mainTable = Table([])
    positions = list(mainTable.positions.keys())

    sg.theme('BluePurple')
    layout_intro = [[sg.Text("Let's play bridge!\nEnter your name: "), sg.Text(key='-INTRO-')],
              [sg.Input(key='-NAME-')],
              [sg.Text('Where would you like to sit?'), sg.Text(key='-QPOSITION-')],
              [sg.Combo(positions, key='-POSITION-')],
              [sg.Button('Start')],
              [sg.Text(''), sg.Text( key='-ERRORTEXT-')]]
    
    layout = [[sg.Column(layout_intro, key='-COLINTRO-')],
               [sg.Button('Exit')]]
    
    window = sg.Window('Austin Codes Bridge', layout)

    while True: 
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Start':
            if values['-NAME-'] != '' and values['-POSITION-'] in positions:
                window['-COLINTRO-'].update(visible=False)
            else:
                window['-ERRORTEXT-'].update('Please enter your name and select a position from the dropdown before clicking Start.')


if __name__ == "__main__":
    main()