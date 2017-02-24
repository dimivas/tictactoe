from __future__ import print_function

import copy
import random
import numpy as np
import tensorflow as tf

from tictactoe_player import TicTacToePlayer
from tensorflow.contrib import layers
from tensorflow.python.ops import nn


class TicTacToeComputerPlayer(TicTacToePlayer):

    COM_WIN_REWARD = 1.0
    COM_LOSS_PENALTY = 0.0
    DRAW_REWARD = 0.5

    EMPTY_SEAT = 0
    COM_PLAYER_ID = 1
    OPPONENT_PLAYER_ID = 2


    def __init__(self, epsilon=1.0, epsilon_decay_step=10e-5, board_size=3, hidden_layer_size=50):
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step

        self.player_id = None
        self.prev_game_state = None

        self.board_size = board_size
        self.hidden_layer_size = hidden_layer_size

        self.session = tf.Session()
        self.__build_graph()


    def __get_q_values(self, splitted_states):
        res = self.q_values_nn.eval(session=self.session, feed_dict={self.s: [splitted_states]})[0]
        return res


    def __update_q_values(self, s_t, a_t, y_t):
        self.session.run(self.q_updater, feed_dict={self.s: s_t, self.a: a_t, self.y: y_t})


    def __build_graph(self):
        self.s = tf.placeholder(tf.float32, [None, 2, self.board_size, self.board_size], name="s")
        net = tf.transpose(self.s, [0, 2, 3, 1])
        net = tf.reshape(net, [-1, int(np.prod(net.get_shape().as_list()[1:]))])
        net = layers.fully_connected(net, self.hidden_layer_size, activation_fn=nn.relu)
        net = layers.fully_connected(net, self.board_size*self.board_size, activation_fn=None)
        self.q_values_nn = tf.reshape(net, [-1, self.board_size, self.board_size])
        self.a = tf.placeholder(tf.float32, [None, self.board_size, self.board_size], name="a")
        self.y = tf.placeholder(tf.float32, [None], name="y")
        action_q_values = tf.reduce_sum(tf.mul(self.q_values_nn, self.a), reduction_indices=[1, 2])
        self.loss = tf.reduce_mean(tf.square(self.y - action_q_values))
        optimizer = tf.train.AdamOptimizer(0.001)
        self.q_updater = optimizer.minimize(self.loss, var_list=tf.trainable_variables())

        self.session.run(tf.initialize_all_variables())


    def __update_epsilon(self):
        self.epsilon *= (1 - self.epsilon_decay_step)


    def __reset_state(self):
        self.player_id = None
        self.prev_game_state = None


    def __map_player_id(self, seat):
        internal_player_id = None
        if (seat):
            if (seat == self.player_id):
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        else:
            internal_player_id = self.EMPTY_SEAT
        return internal_player_id


    def end_of_game(self, winning_player_id):
        reward = self.DRAW_REWARD
        if winning_player_id == self.player_id:
            reward = self.COM_WIN_REWARD
        elif winning_player_id:
            reward = self.COM_LOSS_PENALTY

        prev_splitted_states, prev_move_t = self.prev_game_state
        prev_splitted_states = [prev_splitted_states]
        prev_move_t = [prev_move_t]
        self.__update_q_values(prev_splitted_states, prev_move_t, [reward] * len(prev_splitted_states))
        
        self.__reset_state()


    def __encode_state(self, game_state):
        encoded_state = map(self.__map_player_id, np.array(game_state).flatten())
        encoded_state = np.array(encoded_state, float).reshape(3, 3)
        return encoded_state


    def __split_states(self, encoded_state):
        com_state = np.copy(encoded_state)
        com_state[com_state != self.COM_PLAYER_ID] = 0

        opponent_state = np.copy(encoded_state)
        opponent_state[opponent_state != self.OPPONENT_PLAYER_ID] = 0
        opponent_state[opponent_state == self.OPPONENT_PLAYER_ID] = 1

        return [com_state, opponent_state]


    def get_next_move(self, game_state):
        encoded_state = self.__encode_state(game_state)

        free_seats = np.where(encoded_state == self.EMPTY_SEAT)
        free_seats_t = np.transpose(free_seats)

        splitted_states = self.__split_states(encoded_state)
        q_values = self.__get_q_values(splitted_states)

        best_next_move = tuple(free_seats_t[np.argmax(q_values[free_seats])])

        if np.random.random() < self.epsilon:
            next_move = tuple(free_seats_t[np.random.randint(len(free_seats_t))])
            self.__update_epsilon()
        else:
            next_move = best_next_move

        if self.prev_game_state:
            prev_splitted_states, prev_move_t = self.prev_game_state
            y_t_prev = 0. + 0.8 * q_values[best_next_move]
            prev_splitted_states = [prev_splitted_states]
            prev_move_t = [prev_move_t]
            self.__update_q_values(prev_splitted_states, prev_move_t, [y_t_prev] * len(prev_splitted_states))


        next_move_t = np.zeros_like(encoded_state, dtype=np.float32)
        next_move_t[next_move] = 1.
	
        self.prev_game_state = (splitted_states, next_move_t) 
        return next_move


    def set_player_id(self, player_id):
        self.player_id = player_id
