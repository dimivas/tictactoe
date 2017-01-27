from __future__ import print_function

from datetime import datetime
import logging
import os
import time


class TicTacToeGame(object):

    RESULT_DRAW = None


    def __init__(self, p1, p2, board_size=3, player_symbol=('X', 'O')):
        self.board_size = board_size
        self.player_symbol = player_symbol
        self.players = (p1, p2)
        self.game_id = 0

        self.__init_board()


    def __init_board(self):
        """
        Initialize game board with default value
        """
        self.board = map(lambda x: [None] * self.board_size, range(self.board_size))


    def print_board(self):
        """
        Prints the game board with the current state
        """
        os.system('clear')
        print("  {}".format(" ".join(str(x) for x in range(self.board_size))))
        for line_id in range(self.board_size):
            line_state = " ".join(map(lambda x: x and str(x) or '-', self.board[line_id])))
            print("{} {}".format(line_id, line_state)
        print()


    """
    Validation methods
    """

    def __is_seat_occupied(self, row, col):
        """
        Is seat occupied
        @param row (int): Number of row
        @param col (int): Number of col
        @return (bool)
        """
        return self.board[row][col] is not None


    def __is_input_valid(self, row, col):
        """
        Is input valid
        @param row (int): Number of row
        @param col (int): Number of col
        @return (bool) 
        """
        result = True
        if not(str(row).isdigit()) or not(str(col).isdigit()):
            result = False
        else:
            row = int(row)
            col = int(col)
            if (row < 0 or row >= self.board_size):
                result = False
            if (col < 0 or col >= self.board_size):
                result = False
        if (result == True):
            if self.__is_seat_occupied(row, col):
                result = False
        return result


    def __have_we_a_winner(self, last_move):
        """
        Check if there is a winner
        @param last_move (tuple): tuple/list with row and column number of the last move (e.g. (1, 2))
        @return (bool)
        """
        result = False
        row, col = last_move
        for i in range(self.board_size):
            if (self.board[i][0] and self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2]):
                result = True
            if (self.board[0][i] and self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i]):
                result = True
        if (self.board[0][0] and self.board[0][0] == self.board[1][1] and self.board[0][0] ==self. board[2][2]):
            result = True
        if (self.board[2][0] and self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2]):
            result = True
        return result


    def __end_of_game(self, winning_player, be_verbose=True):
        """
        End of game
        @param winning_player (int): Either the first (0) or the second (1) player
        @param be_verbose (bool): Boolean for being verbose or not
        """
        be_verbose and self.print_board()
        be_verbose and print("Game {}: Player {} is the winner!".format(self.game_id, winning_player + 1))
        winning_player_symbol = self.player_symbol[winning_player]
        map(lambda x: x.end_of_game(winning_player_symbol), self.players)


    def play(self, be_verbose=True):
        """
        Play
        @param be_verbose (bool): Boolean for being verbose or not
        """
        map(lambda x: self.players[x].set_player_id(self.player_symbol[x]), range(len(self.players)))
        round = 0
        while(True):
            be_verbose and self.print_board()
            if (round > 8):
                be_verbose and print("Game {}: This is a draw!".format(self.game_id))
                map(lambda x: x.end_of_game(self.RESULT_DRAW), self.players)
                break
            which_player = round % 2
            row, col = self.players[which_player].get_next_move(self.board)
            if not(self.__is_input_valid(row, col)):
                continue
            row = int(row)
            col = int(col)
            self.board[row][col] = self.player_symbol[which_player]
            if (self.__have_we_a_winner((row, col))):
                self.__end_of_game(which_player, be_verbose=be_verbose)
                break
            round += 1

