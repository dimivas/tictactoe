from __future__ import print_function

from tictactoe_player import TicTacToePlayer


class TicTacToeHumanPlayer(TicTacToePlayer):

    def __init__(self, player_id):
        self.player_id = player_id
        return

    def get_next_move(self, game_state):
        print("Player {}: ".format(self.player_id), end="")
        player_input = raw_input()
        row, col = map(lambda x: str(x).strip(), player_input.split(','))
        return (row, col)


