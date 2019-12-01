import sys

import PySimpleGUI as sg
import numpy as np

import probability as pb


def chooseStrat():
    strat = {"aveugle": pb.max_esp}

    sg.change_look_and_feel('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('What strat do you want ?')],
              [sg.Text('strat : '), sg.Listbox(values=list(strat.keys()),
                                               key='strat', enable_events=True)],
              [sg.Button('Exit')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):  # if user closes window or clicks cancel
            sys.exit(1)
        if len(values["strat"]) != 0:
            break

    window.close()
    return strat[values["strat"][0]]


def humainStrat(D):
    layout = [[sg.Text('How many dice do you want to play ?')],
              [sg.Listbox(values=range(D + 1),
                          key='d', enable_events=True)],
              [sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            sys.exit(1)
        if len(values["d"]) != 0:
            break

    window.close()
    return values["d"][0]


def dice(d):
    r = np.random.randint(1, 7, size=(d,))

    if 1 in r:
        return 1
    else:
        return np.sum(r)


def mainloopSeq(player1, player2, M, D):
    p1 = 0
    p2 = 0
    n = 0

    while p1 < M and p2 < M:

        print('Turn ' + str(n))
        n += 1
        p1 += dice(player1(D))
        print("p1 : " + str(p1))
        if p1 >= M:
            sg.popup("Player 1 won")
            sys.exit(1)
        p2 += dice(player2(D))
        print("p2 : " + str(p2))
        if p2 >= M:
            sg.popup("Player 2 won")
            sys.exit(1)

        layout = [[sg.Text('Turn ' + str(n))],
                  [sg.Text("p1 : " + str(p1))],
                  [sg.Text("p2 : " + str(p2))],
                  [sg.Button('Next Turn'), sg.Button('Exit')]]

        window = sg.Window('Window Title', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event in (None, 'Exit'):  # if user closes window or clicks cancel
                sys.exit(1)
            elif event in (None, 'Next Turn'):  # if user closes window or clicks cancel
                break


def start_game(M, D, simultane=False):
    type = ["humain", "bot"]
    strat = {"humain": humainStrat, "bot": chooseStrat}

    sg.change_look_and_feel('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('What type of game do you want to play ?')],
              [sg.Text('Player1 : '), sg.Listbox(values=type,
                                                 key='player1', enable_events=True)],
              [sg.Text('Player2 : '), sg.Listbox(values=type,
                                                 key='player2', enable_events=True)],
              [sg.Button('Exit')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):  # if user closes window or clicks cancel
            sys.exit(1)
        if len(values["player1"]) != 0 and len(values["player2"]) != 0:
            break

    window.close()
    mainloopSeq(strat[values["player1"][0]], strat[values["player2"][0]], M, D)


def main():
    sg.change_look_and_feel('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Start a new game')],
              [sg.Text('M : '), sg.InputText()],
              [sg.Text('D : '), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            sys.exit(1)
        elif event in (None, 'Ok'):  # if user closes window or clicks cancel
            break

    window.close()
    start_game(int(values[0]), int(values[1]))


main()
