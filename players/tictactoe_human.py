"""
The implementation of the Tic-Tac-Toe human interface.
This component receives the next move as an input from a human player.
"""
from __future__ import print_function
import sys

from .abstract_tictactoe_player import AbstractTicTacToePlayer


class TicTacToeHuman(AbstractTicTacToePlayer):
    """
    The implementation of the Tic-Tac-Toe human interface.
    This component receives the next move as an input from a human player.
    """


    def __init__(self):
        """
        Constructor
        """
        self.player_id = None
        if sys.version_info.major == 2:
            self.__input_func = raw_input
        else:
            self.__input_func = input


    def __get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
        print("Player {}: ".format(self.player_id), end="")
        player_input = self.__input_func()
        row, col = [str(x).strip() for x in player_input.split(',')]
        return (row, col)


    def get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
        next_move = None
        while True:
            try:
                next_move = self.__get_next_move(game_state)
                break
            except ValueError:
                print("Invalid input (x,y)")
        return next_move


    def end_of_game(self, winning_player_id):
        """
        End of game.

        @param winning_player_id: the winning player ID (symbol), given by the game engine
        """
        self.player_id = None


    def set_player_id(self, player_id):
        """
        Set the player's symbol in game

        @param player_id: the symbol used by the player
        """
        self.player_id = player_id
