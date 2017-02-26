"""
All Player Types for TicTacToe
"""

from players.tictactoe_computer_naive import TicTacToeComputerNaive
from players.tictactoe_computer_qlearning import TicTacToeComputerQLearning
from players.tictactoe_computer_random import TicTacToeComputerRandom
from players.tictactoe_computer_tensorflow import TicTacToeComputerTensorflow
from players.tictactoe_human import TicTacToeHuman

__all__ = ['TicTacToeComputerNaive', 'TicTacToeComputerQLearning',
           'TicTacToeComputerRandom', 'TicTacToeComputerRandom',
           'TicTacToeHuman']
