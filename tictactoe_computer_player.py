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


    def __init__(self, alpha=0.99, epsilon=1.0, epsilon_decay_step=0.999, be_verbose=False):
        self.alpha = alpha
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step
        self.be_verbose = be_verbose

        self.q_values = {}
        self.prev_game_state = None
        self.player_id = None


    def __combine_state_and_seat(self, game_state, free_seat):
        next_game_state = copy.deepcopy(game_state)
        next_game_state[free_seat[0]][free_seat[1]] = self.player_id
        return next_game_state


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


    def __get_score(self, game_state, free_seat):
        next_game_state = self.__combine_state_and_seat(game_state, free_seat)
        return self.q_values[self.__encode_state(next_game_state)]


    def __init_q_values(self, game_state):
        encoded_state = self.__encode_state(game_state)
        if (encoded_state not in self.q_values):
            self.q_values[encoded_state] = self.INITIAL_STATE_VALUE
        for free_seat in self.__get_free_seats(game_state):
            next_encoded_state = self.__encode_state(self.__combine_state_and_seat(game_state, free_seat))
            if (next_encoded_state not in self.q_values):
                self.q_values[next_encoded_state] = self.INITIAL_STATE_VALUE


    def __map_player_id(self, seat):
        internal_player_id = None
        if (seat):
            if (seat == self.player_id):
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        return internal_player_id


    def __reset_state(self):
        self.prev_game_state = None


    def __update_epsilon(self):
        self.epsilon *= self.epsilon_decay_step


    def __update_q_values(self, reward):
        if (self.prev_game_state):
            self.q_values[self.prev_game_state] += self.alpha * (reward - self.q_values[self.prev_game_state])


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
        self.__init_q_values(game_state)

        if (random.random() < self.epsilon):
            next_move = self.__get_next_random_move(game_state)
            self.__update_epsilon()
        else:
            next_move = self.__get_next_greedy_move(game_state)

        next_game_state_score = self.__get_score(game_state, next_move)
        self.__update_q_values(next_game_state_score)

        self.prev_game_state = self.__encode_state(self.__combine_state_and_seat(game_state, next_move))
        return next_move


    def get_q_values_from_other_com(self, com_player):
        assert(isinstance(com_player, TicTacToeComputerPlayer))
        for game_state in com_player.q_values:
            if game_state not in self.q_values:
                self.q_values[game_state] = com_player.q_values[game_state]


    def set_player_id(self, player_id):
        self.player_id = player_id
