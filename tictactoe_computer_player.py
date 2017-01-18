from __future__ import print_function

import copy
import random

from tictactoe_player import TicTacToePlayer


class TicTacToeComputerPlayer(TicTacToePlayer):

    INITIAL_STATE_VALUE = 0.0
    COM_WINNING_STAKE = 10.0
    OTHER_WINNING_STAKE = -10.0
    DRAW_WINNING_STAKE = 5.0


    def __init__(self, player_id, alpha=0.5, epsilon=0.05):
        self.player_id = player_id
        self.q_values = {}
        self.alpha = alpha
        self.epsilon = epsilon
        self.prev_game_state = None


    def __combine_state_and_seat(self, game_state, free_seat):
        print("GAME STATE: {}".format(game_state))
        print("FREE SEAT: {}".format(free_seat))
        next_game_state = copy.deepcopy(game_state)
        next_game_state[free_seat[0]][free_seat[1]] = self.player_id
        return next_game_state


    def __convert_nested_list_to_tuple(self, nested_list):
        return tuple(map(lambda x: tuple(x), nested_list))


    def __encode_state(self, game_state):
        print("GAME STATE: {}".format(game_state))
        flatten_list = list(item for sublist in game_state for item in sublist)
        print("FLATTEN LIST: {}".format(flatten_list))
        my_seats = self.__get_binary_repr(flatten_list, lambda x: x == self.player_id)
        print("MY SEATS: {}".format(my_seats))
        other_seats = self.__get_binary_repr(flatten_list, lambda x: x and x != self.player_id)
        print("OTHER SEATS: {}".format(other_seats))
        return (my_seats, other_seats)


    def __get_binary_repr(self, flatten_game_state, filter_func):
        filtered_values = map(filter_func, flatten_game_state)
        print("FILTERED_VALUES: {}".format(filtered_values))
        binary_repr = "".join(map(lambda x: x and '1' or '0', filtered_values))
        print("BINARY REPR: {}".format(binary_repr))
        return int(binary_repr, 2)


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


    def __init_q_values(self, game_state, be_recursive=True):
        encoded_state = self.__encode_state(game_state)
        if (encoded_state not in self.q_values):
            self.q_values[encoded_state] = self.INITIAL_STATE_VALUE
            if (be_recursive):
                for free_seat in self.__get_free_seats(game_state):
                    next_encoded_game_state = self.__combine_state_and_seat(game_state, free_seat)
                    #TODO: Must not be encoded
                    self.__init_q_values(next_encoded_game_state, be_recursive=False)


    def __reset_game(self):
        self.prev_game_state = None


    def __update_q_values(self, reward):
        # V(s) <- V(s) + alpha * [ V(s') - V(s) ]
        if (self.prev_game_state):
            self.q_values[self.prev_game_state] += self.alpha * (reward - self.q_values[self.prev_game_state])


    def end_of_game(self, winning_player_id):
        reward = self.DRAW_WINNING_STAKE
        if (winning_player_id == self.player_id):
            reward = self.COM_WINNING_STAKE
        elif (winning_player_id):
            reward = self.OTHER_WINNING_STAKE
        self.__update_q_values(reward)
        self.__reset_game()


    def get_next_move(self, game_state):
        next_move = None
        self.__init_q_values(game_state)
        if (random.random() < self.epsilon):
            next_move = self.__get_next_random_move(game_state)
        else:
            next_move = self.__get_next_greedy_move(game_state)

        next_game_state_score = self.__get_score(game_state, next_move)
        self.__update_q_values(next_game_state_score)

        self.prev_game_state = self.__encode_state(game_state)
        return next_move



