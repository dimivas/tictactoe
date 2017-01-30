from __future__ import print_function

import copy
import random
import time

from tictactoe_player import TicTacToePlayer


class TicTacToeComputerPlayer(TicTacToePlayer):

    INITIAL_STATE_VALUE = 0.5
    COM_WINNING_STAKE = 1.0
    OPPONENT_WINNING_STAKE = 0.0
    DRAW_WINNING_STAKE = 0.5

    COM_PLAYER_ID = 1
    OPPONENT_PLAYER_ID = 2


    def __init__(self, epsilon=1.0, epsilon_decay_step=0.999, be_verbose=False):
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step
        self.be_verbose = be_verbose

        self.q_values = {}
        self.game_moves_history = []
        self.player_id = None


    def __encode_state(self, game_state):
        flatten_list = list(item for sublist in game_state for item in sublist)
        encoded_state = tuple(map(self.__map_player_id, flatten_list))
        return encoded_state


    def __get_free_seats(self, game_state):
        free_seats = []
        for i in range(len(game_state)):
            for j in range(len(game_state)):
                if not(game_state[i][j]):
                    free_seats.append((i, j))
        return tuple(free_seats)


    def __get_next_greedy_move(self, game_state):
        best_move = None
        best_score = None
        for free_seat in self.__get_free_seats(game_state):
            next_game_state_score = self.__get_score(game_state, free_seat)
            if (best_score is None):
                best_score = next_game_state_score
                best_move = free_seat
                continue
            if (next_game_state_score > best_score):
                best_score = next_game_state_score
                best_move = free_seat
        return best_move


    def __get_next_random_move(self, game_state):
        return random.choice(self.__get_free_seats(game_state))


    def __get_score(self, game_state, move):
        return self.q_values[self.__encode_state(game_state)][move][0]


    def __init_q_values(self, game_state):
        encoded_game_state = self.__encode_state(game_state)
        if (encoded_game_state in self.q_values):
            return
        self.q_values[encoded_game_state] = {}
        for free_seat in self.__get_free_seats(game_state):
            self.q_values[encoded_game_state][free_seat] = (self.INITIAL_STATE_VALUE, 0)


    def __map_player_id(self, seat):
        internal_player_id = None
        if (seat):
            if (seat == self.player_id):
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        return internal_player_id


    def __reset_state(self):
        self.game_moves_history = []
        self.set_player_id = None


    def __update_epsilon(self):
        self.epsilon *= self.epsilon_decay_step


    def __update_q_values(self, reward):
        for encoded_game_state, move in self.game_moves_history:
            value, times_passed = self.q_values[encoded_game_state][move]
            new_value = (value * times_passed + float(reward)) / (times_passed + 1)
            self.q_values[encoded_game_state][move] = (new_value, times_passed + 1)


    def end_of_game(self, winning_player_id):
        reward = self.DRAW_WINNING_STAKE
        if (winning_player_id == self.player_id):
            reward = self.COM_WINNING_STAKE
        elif (winning_player_id):
            reward = self.OPPONENT_WINNING_STAKE
        self.__update_q_values(reward)
        self.__reset_state()


    def get_next_move(self, game_state):
        next_move = None
        encoded_game_state = self.__encode_state(game_state)

        self.__init_q_values(game_state)

        if (random.random() < self.epsilon):
            next_move = self.__get_next_random_move(game_state)
            self.__update_epsilon()
        else:
            next_move = self.__get_next_greedy_move(game_state)

        self.game_moves_history.append((encoded_game_state, next_move))

        return next_move


    def get_q_values_from_other_com(self, other_player):
        assert(isinstance(other_player, TicTacToeComputerPlayer))
        for game_state in other_player.q_values:
            if game_state not in self.q_values:
                self.q_values[game_state] = other_player.q_values[game_state]


    def set_player_id(self, player_id):
        self.player_id = player_id
