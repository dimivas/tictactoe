"""
All Player Types for TicTacToe
"""

from .tictactoe_computer_naive import TicTacToeComputerNaive
from .tictactoe_computer_qlearning import TicTacToeComputerQLearning
from .tictactoe_computer_random import TicTacToeComputerRandom
from .tictactoe_computer_tensorflow import TicTacToeComputerTensorflow
from .tictactoe_human import TicTacToeHuman

__all__ = ['TicTacToeComputerNaive', 'TicTacToeComputerQLearning',
           'TicTacToeComputerRandom', 'TicTacToeComputerTensorflow',
           'TicTacToeHuman']
