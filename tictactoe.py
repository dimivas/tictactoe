from __future__ import print_function

import os
import sys


board_size = 3
board = None
player_symbol = ('X', 'O')
q_values = {}
gamma = 0.2
alpha = 0.3
epsilon = 0.05

def initialize_board():
    global board
    board = map(lambda x: [None] * board_size, range(board_size))

def print_board():
    os.system('clear')
    print("  1 2 3")
    for line in range(len(board)):
        print("{} ".format(line + 1), end='')
        print(" ".join(map(lambda x: x and str(x) or '-', board[line])))
    print()

def have_we_a_winner():
    result = False
    for i in range(len(board)):
        if (board[i][0] and board[i][0] == board[i][1] and board[i][0] == board[i][2]):
            result = True
        if (board[0][i] and board[0][i] == board[1][i] and board[0][i] == board[2][i]):
            result = True
    if (board[0][0] and board[0][0] == board[1][1] and board[0][0] == board[2][2]):
        result = True
    if (board[2][0] and board[2][0] == board[1][1] and board[2][0] == board[0][2]):
        result = True
    return result

def is_valid_input(player_input):
    result = True
    try:
        row, col = map(lambda x: int(x) - 1, player_input)

        if row < 0 or row > 2:
            result = False
        if col < 0 or col > 2:
            result = False
    except:
        result = False

    if (result == True):
        if (board[row][col]):
            result = False
    return result

initialize_board()

round = 0

while(True):
    print_board()
    if (round > 8):
        print("This is a draw!")
        break

    which_player = round % 2
    print("Player {}: ".format(which_player + 1), end="")
    player_input = raw_input()
    if not(is_valid_input(player_input)):
        continue
    row, col = map(lambda x: int(x) - 1, player_input)
    board[row][col] = player_symbol[which_player]
    if (have_we_a_winner()):
        print_board()
        print("Player {} is the winner!".format(which_player + 1))
        break
    round += 1
    print()
