import sys
import os

import PySimpleGUI as sg
import numpy as np

import probability as pb

Eg_table_which_play_p1, Eg_table_which_play_p2 = None, None

def humainStrat(D):
    layout = [[sg.Text('How many dice do you want to play ?')],
              [sg.Combo(values=list(range(1,D + 1)),
                          key='d', enable_events=True)],
              [sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Dice', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            sys.exit(1)
        if values["d"] != None:
            break

    window.close()
    return values["d"]

def load_table(M,D):

    global Eg_table_which_play_p1
    global Eg_table_which_play_p2

    if os.path.isfile("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M) + ".npy") and os.path.isfile(
            "tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M) + ".npy"):
        Eg_table_which_play_p1 = np.load("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M) + ".npy")
        Eg_table_which_play_p2 = np.load("tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M) + ".npy")

    else:
        _, _, _, Eg_table_which_play_p1, Eg_table_which_play_p2 = pb.eg(D, M, 0, 0, True)
        np.save("tables_tpt/npy/which_play_p1_" + str(D) + "_" + str(M), Eg_table_which_play_p1)
        np.save("tables_tpt/npy/which_play_p2_" + str(D) + "_" + str(M), Eg_table_which_play_p2)
        df = pd.DataFrame(Eg_table_which_play_p1)
        f = open("tables_tpt/txt/which_play_p1_" + str(D) + "_" + str(M)+".html", "w")
        f.write(df.to_html())
        df = pd.DataFrame(Eg_table_which_play_p2)
        f = open("tables_tpt/txt/which_play_p2_" + str(D) + "_" + str(M)+".html", "w")
        f.write(df.to_html())

def choose_aveugle(D,truc,i,j):
    return pb.max_esp(D)

def choose_optimale(D,Eg_table_which_play, i, j):
    return int(Eg_table_which_play[i, j])


def choose_aleatoire(D,truc,i,j):
    return np.random.randint(1, D + 1)

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

    global Eg_table_which_play_p1
    global Eg_table_which_play_p2

    while p1 < M and p2 < M:

        print('Turn ' + str(n))
        n += 1
        p1 += dice(player1(D,Eg_table_which_play_p1,p1,p2))
        print("p1 : " + str(p1))
        if p1 >= M:
            sg.popup("Player 1 won")
            sys.exit(1)
        p2 += dice(player2(D,Eg_table_which_play_p2,p1,p2))
        print("p2 : " + str(p2))
        if p2 >= M:
            sg.popup("Player 2 won")
            sys.exit(1)

        layout = [[sg.Text('Turn ' + str(n))],
                  [sg.Text("p1 : " + str(p1))],
                  [sg.Text("p2 : " + str(p2))],
                  [sg.Button('Next Turn'), sg.Button('Exit')]]

        window = sg.Window('Dice', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event in (None, 'Exit'):  # if user closes window or clicks cancel
                sys.exit(1)
            elif event in (None, 'Next Turn'):  # if user closes window or clicks cancel
                break

def start_game(M, D, simultane=False):
    type = ["humain", "bot"]
    strat = {"humain": humainStrat, "IA aveugle": choose_aveugle, "IA optimal" : choose_optimale, "IA aleatoire":choose_aleatoire}

    load_table(M,D)

    sg.change_look_and_feel('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('What type of game do you want to play ?')],
              [sg.Text('Player1 : '), sg.Combo(values=list(strat.keys()),
                                                 key='player1', enable_events=True)],
              [sg.Text('Player2 : '), sg.Combo(values=list(strat.keys()),
                                                 key='player2', enable_events=True)],
              [sg.Button('Exit')]]

    # Create the Window
    window = sg.Window('Dice', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):  # if user closes window or clicks cancel
            sys.exit(1)
        if len(values["player1"]) != 0 and len(values["player2"]) != 0:
            break

    window.close()
    mainloopSeq(strat[values["player1"]], strat[values["player2"]], M, D)


def main():
    sg.change_look_and_feel('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Start a new game')],
              [sg.Text('M : '), sg.InputText()],
              [sg.Text('D : '), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Dice', layout)
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
