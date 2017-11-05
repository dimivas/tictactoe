"""
The implementation of the Tic-Tac-Toe player component 
using a naive version of Q-Learning
"""
from __future__ import print_function

import random

from .abstract_tictactoe_player import AbstractTicTacToePlayer


class TicTacToeComputerNaive(AbstractTicTacToePlayer):
    """
    The implementation of the Tic-Tac-Toe player component 
    using a naive version of Q-Learning
    """

    INITIAL_STATE_VALUE = 0.5
    COM_WIN_REWARD = 1.0
    COM_LOSS_PENALTY = 0.0
    DRAW_REWARD = 0.5

    COM_PLAYER_ID = 1
    OPPONENT_PLAYER_ID = 2


    def __init__(self, epsilon=1.0, epsilon_decay_step=10e-5):
        """
        Constructor

        @param epsilon: the epsilon parameter (randomness of the next move)
                        of Q-Learning algorithm [0, 1]
        @param epsilon_decay_step: the decay factor for updating the epsilon parameter [0, 1]
        """
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step

        self.q_values = {}
        self.game_moves_history = []
        self.player_id = None


    def __encode_state(self, game_state):
        """
        Transforms the 2D list game state into an internal representation

        @param game_state: a 2D list with the game state given by the game engine
        @return: a (flatten) list with the internal representation of the game engine
        """
        flatten_list = list(item for sublist in game_state for item in sublist)
        encoded_state = tuple(map(self.__map_player_id, flatten_list))
        return encoded_state


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


    def __get_next_greedy_move(self, game_state):
        """
        Get the next move based on a greedy algorithm and the Q-Values

        @param game_state: a 2D list with the game state
        @return: a list with the x and y values of the selected seat
        """ 
        best_move = None
        best_score = None
        for free_seat in self.__get_free_seats(game_state):
            next_game_state_score = self.__get_score(game_state, free_seat)
            if best_score is None:
                best_score = next_game_state_score
                best_move = free_seat
                continue
            if next_game_state_score > best_score:
                best_score = next_game_state_score
                best_move = free_seat
        return best_move


    def __get_next_random_move(self, game_state):
        """
        Get the next move based on a random selection

        @param game_state: a 2D list with the game state
        @return: a list with the x and y values of the selected seat
        """
        return random.choice(self.__get_free_seats(game_state))


    def __get_score(self, game_state, move):
        """
        Get the Q-Value of the move

        @param game_state: a 2D list with the game state
        @move: a list with the x and y values of the selected move
        @return: the Q-Value
        """
        return self.q_values[self.__encode_state(game_state)][move][0]


    def __init_q_values(self, game_state):
        """
        Initialize the Q-Values for the current game state and 
        the next possible game states, based on the available seats
        
        @param game_state: a 2D list with the game state
        """
        encoded_game_state = self.__encode_state(game_state)
        if encoded_game_state in self.q_values:
            return
        self.q_values[encoded_game_state] = {}
        for free_seat in self.__get_free_seats(game_state):
            self.q_values[encoded_game_state][free_seat] = (self.INITIAL_STATE_VALUE, 0)


    def __map_player_id(self, seat):
        """
        Maps the symbol given by the game engine to an internal notation

        @param value: the value of the seat (symbol)
        @return: the mapped value
        """ 
        internal_player_id = None
        if seat:
            if seat == self.player_id:
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        return internal_player_id


    def __reset(self):
        """
        Reset state of the object
        """
        self.game_moves_history = []
        self.player_id = None


    def __update_epsilon(self):
        """
        Update epsilon parameter
        """
        self.epsilon *= (1 - self.epsilon_decay_step)


    def __update_q_values(self, reward):
        """
        Update Q-Values

        @param reward: the reward for all moves taken during the game
        """
        for encoded_game_state, move in self.game_moves_history:
            value, times_passed = self.q_values[encoded_game_state][move]
            new_value = (value * times_passed + float(reward)) / (times_passed + 1)
            self.q_values[encoded_game_state][move] = (new_value, times_passed + 1)


    def end_of_game(self, winning_player_id):
        """
        End of game. Update Q-Values and reset the game state

        @param winning_player_id: the winning player ID (symbol), given by the game engine
        """
        reward = self.DRAW_REWARD
        if winning_player_id == self.player_id:
            reward = self.COM_WIN_REWARD
        elif winning_player_id:
            reward = self.COM_LOSS_PENALTY
        self.__update_q_values(reward)
        self.__reset()


    def get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
        next_move = None
        encoded_game_state = self.__encode_state(game_state)

        self.__init_q_values(game_state)

        if random.random() < self.epsilon:
            next_move = self.__get_next_random_move(game_state)
            self.__update_epsilon()
        else:
            next_move = self.__get_next_greedy_move(game_state)

        self.game_moves_history.append((encoded_game_state, next_move))

        return next_move


    def get_q_values_from_other_com(self, other_player):
        """
        Merges the learned Q-Values taken by an other instance of the player

        @param com_player: instance of the other player
        """
        for game_state in other_player.q_values:
            if game_state not in self.q_values:
                self.q_values[game_state] = other_player.q_values[game_state]


    def set_player_id(self, player_id):
        """
        Set the player's symbol in game

        @param player_id: the symbol used by the player
        """
        self.player_id = player_id
