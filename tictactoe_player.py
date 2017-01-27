import abc

class TicTacToePlayer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def end_of_game(self, winning_player_id):
        return


    @abc.abstractmethod
    def get_next_move(self, game_state):
        return


    def set_player_id(self, player_id):
        self.player_id = player_id
