from __future__ import print_function

import random
import time

from tictactoe_player import TicTacToePlayer


class TicTacToeCComputerPlayer(TicTacToePlayer):

    INITIAL_STATE_VALUE = 0.5
    COM_WIN_REWARD = 1.0
    COM_LOSS_PENALTY = 0.0
    DRAW_REWARD = 0.5

    COM_PLAYER_ID = 1
    OPPONENT_PLAYER_ID = 2


    def __init__(self, alpha=0.99, epsilon=1.0, epsilon_decay_step=10e-5):
        self.alpha = alpha
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step

        self.q_values = {}
        self.prev_game_state = None
        self.player_id = None


    def __apply_move_on_state(self, game_state, move):
        next_game_state = [x[:] for x in game_state]
        next_game_state[move[0]][move[1]] = self.player_id
        return next_game_state


    def __encode_state(self, game_state):
        flatten_list = list(item for sublist in game_state for item in sublist)
        encoded_state = tuple(map(self.__map_player_id, flatten_list))
        return encoded_state


    def __get_free_seats(self, game_state):
        free_seats = []
        for i in range(len(game_state)):
            for j in range(len(game_state[i])):
                if not game_state[i][j]:
                    free_seats.append((i, j))
        return tuple(free_seats)


    def __get_next_greedy_move(self, game_state):
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
        return random.choice(self.__get_free_seats(game_state))


    def __get_score(self, game_state, move):
        next_game_state = self.__apply_move_on_state(game_state, move)
        return self.q_values[self.__encode_state(next_game_state)]


    def __init_q_values(self, game_state):
        encoded_state = self.__encode_state(game_state)
        if encoded_state not in self.q_values:
            self.q_values[encoded_state] = self.INITIAL_STATE_VALUE
        for free_seat in self.__get_free_seats(game_state):
            next_state = self.__apply_move_on_state(game_state, free_seat)
            next_encoded_state = self.__encode_state(next_state)
            if next_encoded_state not in self.q_values:
                self.q_values[next_encoded_state] = self.INITIAL_STATE_VALUE


    def __map_player_id(self, seat):
        internal_player_id = None
        if seat:
            if seat == self.player_id:
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        return internal_player_id


    def __reset_state(self):
        self.prev_game_state = None


    def __update_epsilon(self):
        self.epsilon *= (1 - self.epsilon_decay_step)


    def __update_q_values(self, reward):
        if self.prev_game_state:
            learned_value = self.alpha * (reward - self.q_values[self.prev_game_state])
            self.q_values[self.prev_game_state] += learned_value


    def end_of_game(self, winning_player_id):
        reward = self.DRAW_REWARD
        if winning_player_id == self.player_id:
            reward = self.COM_WIN_REWARD
        elif winning_player_id:
            reward = self.COM_LOSS_PENALTY
        self.__update_q_values(reward)
        self.__reset_state()


    def get_next_move(self, game_state):
        next_move = None
        self.__init_q_values(game_state)

        if random.random() < self.epsilon:
            next_move = self.__get_next_random_move(game_state)
            self.__update_epsilon()
        else:
            next_move = self.__get_next_greedy_move(game_state)

        next_game_state_score = self.__get_score(game_state, next_move)
        self.__update_q_values(next_game_state_score)

        tmp_prev_game_state = self.__apply_move_on_state(game_state, next_move)
        self.prev_game_state = self.__encode_state(tmp_prev_game_state)
        return next_move


    def get_q_values_from_other_com(self, com_player):
        for game_state in com_player.q_values:
            if game_state not in self.q_values:
                self.q_values[game_state] = com_player.q_values[game_state]


    def set_player_id(self, player_id):
        self.player_id = player_id
