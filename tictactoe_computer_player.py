from __future__ import print_function

import copy
import random

from tictactoe_player import TicTacToePlayer


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


    def __combine_state_seat_and_encode(self, game_state, free_seat):
        next_game_state = copy.deepcopy(game_state)
        next_game_state[free_seat[0]][free_seat[1]] = self.player_id
        next_encoded_game_state = self.__encode_state(next_game_state)
        return next_game_state


    def __init_q_values(self, game_state, be_recursive=True):
        encoded_state = self.__encode_state(game_state)
        if (encoded_state not in self.q_values):
            self.q_values[encoded_state] = self.INITIAL_VALUE
            if (be_recursive):
                for free_seat in self.__get_free_seats(game_state):
                    next_encoded_game_state = self.__combine_state_seat_and_encode(game_state, free_seat)
                    self.__init_q_values(next_encoded_game_state, be_recursive=False)


    def __get_next_greedy_move(self, game_state):
        best_move = None
        best_score = None
        for free_seat in self.__get_free_seats(game_state):
            next_game_state = self.__combine_state_seat_and_encode(game_state, free_seat)
            next_game_state_score = self.q_values[next_game_state]
            if (best_score is None):
                best_score = next_game_state_score
                best_move = free_seat
                continue
            if (next_game_state_score > best_score):
                best_score = next_game_state_score
                best_move = free_seat
        return best_move


    def _get_next_random_move(self, game_state):
        return random.choice(self.__get_free_seats(game_state))


    def get_next_move(self, game_state):
        next_move = None
        self.__init_q_values(game_state)
        if (random.random() > self.epsilon):
            next_move = self.__get_next_random_move(game_state)
        else:
            next_move = self.__get_next_greedy_move(game_state)
        self.prev_game_state = game_state
        return next_move


    def set_reward_for_last_move(self, reward):
        # V(s) <- V(s) + alpha * [ V(s') - V(s) ]
        if (self.previous_state):
            self.q_values[self.previous_state] += self.alpha * (reward - self.q_values[self.previous_state])


