from __future__ import print_function

from datetime import datetime
import logging
import os
import time


class TicTacToeGame(object):

    RESULT_DRAW = None


    def __init__(self, p1, p2, board_size=(3, 3), win_size=3, player_symbol=('X', 'O'), be_verbose=True):
        self.board_size = board_size
        self.win_size = win_size
        self.player_symbol = player_symbol
        self.be_verbose = be_verbose

        self.players = (p1, p2)
        self.game_id = 0

        map(lambda x: self.players[x].set_player_id(self.player_symbol[x]), range(len(self.players)))
        self.__init_board()


    def __init_board(self):
        """
        Initialize game board with default value
        """
        self.board = map(lambda x: [None] * self.board_size[1], range(self.board_size[0]))


    def print_board(self):
        """
        Prints the game board with the current state
        """
        if not self.be_verbose:
            return
        os.system('clear')
        print("  {}".format(" ".join(str(x) for x in range(self.board_size[1]))))
        for line_id in range(self.board_size[0]):
            line_state = " ".join(map(lambda x: x and str(x) or '-', self.board[line_id]))
            print("{} {}".format(line_id, line_state))
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
        if not str(row).isdigit() or not str(col).isdigit():
            result = False
        else:
            row = int(row)
            col = int(col)
            if row < 0 or row >= self.board_size[0]:
                result = False
            if col < 0 or col >= self.board_size[1]:
                result = False
        if result:
            if self.__is_seat_occupied(row, col):
                result = False
        return result


    def __have_we_a_winner_in_row(self, row):
        """
        """
        result = False
        if row[0] and all(map(lambda x: x == row[0], row)):
            result = True
        return result


    def __have_we_a_winner_in_square(self, start_row, start_col):
        """
        """
        # Left to right cross
        left_cross = map(lambda x: self.board[start_row + x][start_col + x], range(self.win_size))
        if self.__have_we_a_winner_in_row(left_cross):
            return True
        # Right to left cross
        right_cross = map(lambda x: self.board[start_row + x][start_col + self.win_size - 1 - x], range(self.win_size))
        if self.__have_we_a_winner_in_row(right_cross):
            return True
        for i in range(self.win_size):
            offset_row = self.board[i + start_row][start_col:start_col + self.win_size]
            if self.__have_we_a_winner_in_row(offset_row):
                return True
            offset_col = map(lambda x: x[i + start_col], self.board[start_row:start_row + self.win_size])
            if self.__have_we_a_winner_in_row(offset_col):
                return True
        return False


    def __have_we_a_winner(self, last_move):
        """
        Check if there is a winner
        @param last_move (tuple): tuple/list with row and column number of the last move (e.g. (1, 2))
        @return (bool)
        """
        x_start = max(last_move[0] - (self.win_size - 1), 0)
        x_end = min(last_move[0] + (self.win_size - 1), self.board_size[0] - 1)

        y_start = max(last_move[1] - (self.win_size - 1), 0)
        y_end = min(last_move[1] + (self.win_size - 1), self.board_size[1] - 1)

        for i in range(x_start, x_end - (self.win_size - 2)):
            for j in range(y_start, y_end - (self.win_size - 2)):
                if self.__have_we_a_winner_in_square(i, j):
                    return True

        return False


    def __end_of_game(self, winning_player):
        """
        End of game
        @param winning_player (int): Either the first (0) or the second (1) player
        """
        self.print_board()
        if winning_player is not self.RESULT_DRAW:        
            self.be_verbose and print("Game {}: Player {} is the winner!".format(self.game_id, winning_player + 1))
            winning_player_symbol = self.player_symbol[winning_player]
            map(lambda x: x.end_of_game(winning_player_symbol), self.players)
        else:
            self.be_verbose and print("Game {}: This is a draw!".format(self.game_id))
            map(lambda x: x.end_of_game(self.RESULT_DRAW), self.players)          
        self.__init_board()


    def play(self):
        """
        Let's play ball
        """
        result = self.RESULT_DRAW
        turn = 0
        self.game_id += 1
        while True:
            self.print_board()
            which_player = turn % 2
            row, col = self.players[which_player].get_next_move(self.board)
            if not self.__is_input_valid(row, col):
                continue
            row = int(row)
            col = int(col)
            self.board[row][col] = self.player_symbol[which_player]
            if self.__have_we_a_winner((row, col)):
                self.__end_of_game(which_player)
                result = which_player
                break
            turn += 1
            if turn >= self.board_size[0] * self.board_size[1]:
                self.__end_of_game(self.RESULT_DRAW)
                break
        return result
