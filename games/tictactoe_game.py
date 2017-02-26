"""
The implementation of the Tic-Tac-Toe game engine
"""
from __future__ import print_function

import os


class TicTacToeGame(object):

    RESULT_DRAW = None


    def __init__(self, p1, p2, board_size=3, win_size=3, player_symbol=('X', 'O'), be_verbose=True):
        """
        Constructor

        @param p1: the instance of Player 1
        @param p2: the instance of Player 2
        @board_size: the number of rows and columns of the board (>= 3)
        @win_size: the winning line size. This value should be equal or less than 
                   the number of rows and columns of the board and at least 3 
        @player_symbol: a list with the players' symbol
        @be_verbose: boolean value for verbosity
        """
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
        self.board = map(lambda x: [None] * self.board_size, range(self.board_size))


    def print_board(self):
        """
        Prints the game board with the current state
        """
        if not self.be_verbose:
            return
        os.system('clear')
        print("  {}".format(" ".join(str(x) for x in range(self.board_size))))
        for line_id in range(self.board_size):
            line_state = " ".join(map(lambda x: x and str(x) or '-', self.board[line_id]))
            print("{} {}".format(line_id, line_state))
        print()


    def __is_seat_occupied(self, seat):
        """
        Check if seat is occupied

        @param seat: a list with the x and y values of the seat  
        @return: boolean value
        """
        return self.board[seat[0]][seat[1]] is not None


    def __is_input_valid(self, row, col):
        """
        Check if input is valid

        @param row: Number of row
        @param col: Number of col
        @return: boolean value
        """
        result = True
        if not str(row).isdigit() or not str(col).isdigit():
            result = False
        else:
            row = int(row)
            col = int(col)
            if row < 0 or row >= self.board_size:
                result = False
            if col < 0 or col >= self.board_size:
                result = False
        if result:
            if self.__is_seat_occupied((row, col)):
                result = False
        return result


    def __have_we_a_winner_in_line(self, line):
        """
        Check if all seats in array are occupied by the same player

        @param line: a list with the seats of the examined line
        @return: boolean value        
        """
        result = False
        if line[0] and all(map(lambda x: x == line[0], line)):
            result = True
        return result


    def __have_we_a_winner_in_square(self, start_row, start_col):
        """
        Check if there is a winner in a specific square

        @param start_row: the starting row of the square in board
        @param start_col: the starting column of the square in board
        @return: boolean value
        """
        # Left to right cross
        left_cross = map(lambda x: self.board[start_row + x][start_col + x], range(self.win_size))
        if self.__have_we_a_winner_in_line(left_cross):
            return True
        # Right to left cross
        right_cross = map(lambda x: self.board[start_row + x][start_col + self.win_size - 1 - x], 
                          range(self.win_size))
        if self.__have_we_a_winner_in_line(right_cross):
            return True
        for i in range(self.win_size):
            offset_row = self.board[i + start_row][start_col:start_col + self.win_size]
            if self.__have_we_a_winner_in_line(offset_row):
                return True
            offset_col = map(lambda x: x[i + start_col], 
                             self.board[start_row:start_row + self.win_size])
            if self.__have_we_a_winner_in_line(offset_col):
                return True
        return False


    def __have_we_a_winner(self, last_move):
        """
        Check if there is a winner

        @param last_move: a list with the row and column number of the last move
        @return: boolean value
        """
        x_start = max(last_move[0] - (self.win_size - 1), 0)
        x_end = min(last_move[0] + (self.win_size - 1), self.board_size - 1)

        y_start = max(last_move[1] - (self.win_size - 1), 0)
        y_end = min(last_move[1] + (self.win_size - 1), self.board_size - 1)

        for i in range(x_start, x_end - (self.win_size - 2)):
            for j in range(y_start, y_end - (self.win_size - 2)):
                if self.__have_we_a_winner_in_square(i, j):
                    return True

        return False


    def __end_of_game(self, winning_player):
        """
        End of game

        @param winning_player: Either the first (0) or the second (1) player
        """
        self.print_board()
        if winning_player is not self.RESULT_DRAW:
            if self.be_verbose: 
                print("Game {}: Player {} is the winner!".format(self.game_id, winning_player + 1))
            winning_player_symbol = self.player_symbol[winning_player]
            map(lambda x: x.end_of_game(winning_player_symbol), self.players)
        else:
            if self.be_verbose:
                print("Game {}: This is a draw!".format(self.game_id))
            map(lambda x: x.end_of_game(self.RESULT_DRAW), self.players)          
        self.__init_board()


    def play(self):
        """
        Let's play ball!
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
            if turn >= self.board_size * self.board_size:
                self.__end_of_game(self.RESULT_DRAW)
                break
        return result
