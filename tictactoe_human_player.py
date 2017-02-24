from __future__ import print_function

from tictactoe_player import TicTacToePlayer


class TicTacToeHumanPlayer(TicTacToePlayer):

    def __init__(self):
        self.player_id = None


    def __get_next_move(self, game_state):
        print("Player {}: ".format(self.player_id), end="")
        player_input = raw_input()
        row, col = map(lambda x: str(x).strip(), player_input.split(','))
        return (row, col)


    def get_next_move(self, game_state):
        next_move = None
        while(True):
            try:
                next_move = self.__get_next_move(game_state)
                break
            except ValueError, ve:
                print("Invalid input (x,y)")
        return next_move


    def end_of_game(self, winning_player_id):
        self.player_id = None


    def set_player_id(self, player_id):
        self.player_id = player_id
