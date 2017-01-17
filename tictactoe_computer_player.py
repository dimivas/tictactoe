from __future__ import print_function

import random


class TicTacToeComputerPlayer(TicTacToePlayer):

    INITIAL_VALUE = 0.0
    
    def __init__(self, player_id, alpha=0.5, epsilon=0.05):
        self.player_id = player_id
        self.q_values = None
        self.alpha = alpha
        self.epsilon = epsilon
        self.prev_game_state = None


    def __get_free_seats(self, game_state):
        free_seats = []
        for i in range(game_state):
            for j in range(game_state):
                if not(game_state[i][j]):
                    free_seats.append((i, j))
        return tuple(free_seats)


    def __get_binary_repr(self, flatten_game_state, filter_func):
        filtered_values = map(filter_func, flatten_game_state)
        binary_repr = "".join(map(lambda x: x and '1' or '0', filtered_values))
        return int(binary_repr, 2)


    def __encode_state(self, game_state):
        flatten_list_generator = (item for sublist in board for item in sublist)
        my_seats = self.__get_binary_repr(flatten_list_generator, lambda x: x == self.player_id)
        other_seats = self.__get_binary_repr(flatten_list_generator, lambda x: x and x != self.player_id)
        return (my_seats, other_seats)


    def __init_q_values(self, game_state):
        encoded_state = self.__encode_state(game_state)
        if (encoded_state not in self.q_values):
            self.q_values[encoded_state] = self.INITIAL_VALUE
            for free_seat in self.__get_free_seats(game_state):
                self.q_values[]

    def get_next_move(self, game_state):


    def set_reward_for_last_move(self, reward):
        # V(s) <- V(s) + alpha * [ V(s') - V(s) ]
        if (self.previous_state):
            self.q_values[self.previous_state] += self.alpha * (reward - self.q_values[self.previous_state])


