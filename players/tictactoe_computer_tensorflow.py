"""
The neural network implementation of the Tic-Tac-Toe player component
using Q-Learning and Tensorflow
"""
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.contrib import layers
from tensorflow.python.ops import nn

from .abstract_tictactoe_player import AbstractTicTacToePlayer


class TicTacToeComputerTensorflow(AbstractTicTacToePlayer):
    """
    The neural network implementation of the Tic-Tac-Toe player component
    using Q-Learning and Tensorflow
    """

    COM_WIN_REWARD = 1.0
    COM_LOSS_PENALTY = 0.0
    DRAW_REWARD = 0.5

    EMPTY_SEAT = 0
    SEAT_OCCUPIED = 1

    COM_PLAYER_ID = 1
    OPPONENT_PLAYER_ID = 2


    def __init__(self, epsilon=1.0, epsilon_decay_step=10e-5, board_size=3, hidden_layer_size=20,
                 learning_rate=0.001, gamma=0.999):
        """
        Constructor

        @param epsilon: the epsilon paramater (randomness of the next move)
                        of Q-Learning algorithm [0, 1]
        @param epsilon_decay_step: the decay factor for updating the epsilon parameter [0, 1]
        @param board_size: a list with the number of rows and columns of the game board
        @param hidden_layer_size: the number of nodes in the hidden layer
        @param learning_rate:
        @param gamma: the gamma parameter (discount factor) of Q-Learning algorithm [0, 1] 
        """
        self.epsilon = epsilon
        self.epsilon_decay_step = epsilon_decay_step

        self.board_size = board_size
        self.hidden_layer_size = hidden_layer_size
        self.learning_rate = learning_rate
        self.gamma = gamma

        self.player_id = None
        self.prev_game_state = None

        self.session = tf.Session()
        self.__init_graph()


    def __init_graph(self):
        """
        Initialize graph
        """
        self.splitted_states = tf.placeholder(tf.float32, 
                                              [None, 2, self.board_size, self.board_size], 
                                              name="splitted_states")

        net = tf.transpose(self.splitted_states, [0, 2, 3, 1])
        net = tf.reshape(net, [-1, int(np.prod(net.get_shape().as_list()[1:]))])
        net = layers.fully_connected(net, self.hidden_layer_size, activation_fn=nn.relu)
        net = layers.fully_connected(net, self.board_size*self.board_size, activation_fn=None)

        self.q_values_nn = tf.reshape(net, [-1, self.board_size, self.board_size])

        self.move = tf.placeholder(tf.float32, [None, self.board_size, self.board_size], name="move")

        self.learned_value = tf.placeholder(tf.float32, [None], name="learned_value")

        action_q_values = tf.reduce_sum(tf.multiply(self.q_values_nn, self.move), reduction_indices=[1, 2])

        loss = tf.reduce_mean(tf.square(self.learned_value - action_q_values))
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        #optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        self.q_updater = optimizer.minimize(loss, var_list=tf.trainable_variables())

        self.session.run(tf.global_variables_initializer())


    def __encode_state(self, game_state):
        """
        Transforms the 2D list game state into an internal representation using numpy array

        @param game_state: a 2D list with the game state given by the game engine
        @return: a 2D numpy array with the internal representation of the game state
        """
        encoded_state = tuple(map(self.__map_player_id, np.array(game_state).flatten()))
        encoded_state = np.array(encoded_state, float).reshape(self.board_size, self.board_size)
        return encoded_state


    def __get_q_values(self, splitted_states):
        """
        Get current Q values for specific state

        @param splitted_states: a numpy array with the splitted game states
        @return: a 2D numpy array with the Q values
        """
        return self.q_values_nn.eval(session=self.session, 
                                     feed_dict={self.splitted_states: [splitted_states]})[0]


    def __map_player_id(self, value):
        """
        Maps the symbol given by the game engine to an internal notation

        @param value: the value of the seat (symbol)
        @return: the mapped value
        """ 
        internal_player_id = None
        if value:
            if value == self.player_id:
                internal_player_id = self.COM_PLAYER_ID
            else:
                internal_player_id = self.OPPONENT_PLAYER_ID
        else:
            internal_player_id = self.EMPTY_SEAT
        return internal_player_id


    def __reset(self):
        """
        Reset state of object
        """
        self.player_id = None
        self.prev_game_state = None


    def __split_states(self, encoded_state):
        """
        Splitting the game state into two states, one for each player.
        The first state refers to seats occuppied by the player itself, 
        while the second represents the opponent's state.

        @param encoded_state: the current game state in a 2D numpy array 
        @return: a list that contains two 2D numpy arrays
        """
        com_state = np.copy(encoded_state)
        com_state[com_state != self.COM_PLAYER_ID] = self.EMPTY_SEAT

        opponent_state = np.copy(encoded_state)
        opponent_state[opponent_state != self.OPPONENT_PLAYER_ID] = self.EMPTY_SEAT
        opponent_state[opponent_state == self.OPPONENT_PLAYER_ID] = self.SEAT_OCCUPIED

        return [com_state, opponent_state]


    def __update_epsilon(self):
        """
        Update epsilon parameter
        """
        self.epsilon *= (1. - self.epsilon_decay_step)


    def __update_q_values(self, splitted_state_t, move_t, learned_value_t):
        """
        Update Q-Values

        @param splitted_state_t: splitted game state tensor
        @param move_t: previous move tensor
        @param learned_value_t: learned_value tensor
        """
        self.session.run(self.q_updater, 
                         feed_dict={self.splitted_states: splitted_state_t, 
                                    self.move: move_t, 
                                    self.learned_value: learned_value_t})


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

        prev_splitted_states, prev_move_t = self.prev_game_state
        prev_splitted_states = [prev_splitted_states]
        prev_move_t = [prev_move_t]
        reward_t = [reward] * len(prev_splitted_states)
        self.__update_q_values(prev_splitted_states, prev_move_t, reward_t)
        
        self.__reset()


    def get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
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
            learned_value = self.gamma * q_values[best_next_move]
            prev_splitted_states = [prev_splitted_states]
            prev_move_t = [prev_move_t]
            learned_value_t = [learned_value] * len(prev_splitted_states)
            self.__update_q_values(prev_splitted_states, prev_move_t, learned_value_t)

        next_move_t = np.zeros_like(encoded_state, dtype=np.float32)
        next_move_t[next_move] = 1.
	
        self.prev_game_state = (splitted_states, next_move_t) 
        return next_move


    def set_player_id(self, player_id):
        """
        Set the player's symbol in game

        @param player_id: the symbol used by the player
        """
        self.player_id = player_id
