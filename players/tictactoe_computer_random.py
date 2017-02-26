"""
The implementation of the Tic-Tac-Toe player component
that always selects a random move. The specific component
is used only for training and/or evaluation of other components.
"""

from __future__ import print_function

import random

from abstract_tictactoe_player import AbstractTicTacToePlayer


class TicTacToeComputerRandom(AbstractTicTacToePlayer):
    """
    The implementation of the Tic-Tac-Toe player component
    that always selects a random move. The specific component
    is used only for training and/or evaluation of other components.
    """

    def __init__(self):
        """
        Constructor
        """
        self.player_id = None


    def __get_free_seats(self, game_state):
        """
        Get the available (free) seats

        @param game_state: a 2D list with the game state
        @return: a list with the set of the available seats.
                 Each seat is a tuple with the x and y values.
        """
        free_seats = []
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if not game_state[i][j]:
                    free_seats.append((i, j))
        return tuple(free_seats)


    def __get_next_random_move(self, game_state):
        """
        Get the next move based on a random selection

        @param game_state: a 2D list with the game state
        @return: a list with the x and y values of the selected seat
        """
        return random.choice(self.__get_free_seats(game_state))


    def end_of_game(self, winning_player_id):
        """
        End of game.
        """
        pass


    def get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
        return self.__get_next_random_move(game_state)


    def set_player_id(self, player_id):
        """
        Set the player's symbol in game

        @param player_id: the symbol used by the player
        """
        self.player_id = player_id
