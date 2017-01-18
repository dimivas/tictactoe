from __future__ import print_function

import os

from tictactoe_human_player import TicTacToeHumanPlayer
from tictactoe_computer_player import TicTacToeComputerPlayer

class TicTacToeGame(object):

    RESULT_DRAW = None


    def __init__(self, p1, p2, board_size=3, player_symbol=('X', 'O')):
        self.board_size = board_size
        self.player_symbol = player_symbol
        self.players = (p1, p2)

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
        print("  0 1 2")
        for line in range(self.board_size):
            print("{} ".format(line), end='')
            print(" ".join(map(lambda x: x and str(x) or '-', self.board[line])))
        print()


    """
    Validation methods
    """

    def __is_seat_occupied(self, row, col):
        return self.board[row][col] is not None


    def __is_input_valid(self, row, col):
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
        @param last_move: tuple/list with row and column number of the last move (e.g. (1, 2))
        @return None in case noone wins or the character of the player that wins
        """
        result = None
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


    def play(self):
        round = 0
        while(True):
            self.print_board()
            if (round > 8):
                print("This is a draw!")
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
                self.print_board()
                print("Player {} is the winner!".format(which_player + 1))

                winning_player_symbol = self.player_symbol[which_player]
                map(lambda x: x.end_of_game(winning_player_symbol), self.players)
                break
            round += 1
        print()

if __name__ == '__main__':
   TicTacToeGame(TicTacToeHumanPlayer('X'), TicTacToeComputerPlayer('O')).play()
