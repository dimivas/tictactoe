"""
Abstract class for Tic-Tac-Toe player component
"""
import abc

class AbstractTicTacToePlayer(object):
    """
    Abstract class for Tic-Tac-Toe player component
    """
    __metaclass__ = abc.ABCMeta

    player_id = None

    @abc.abstractmethod
    def end_of_game(self, winning_player_id):
        """
        End of game. Update Q-Values and reset the game state

        @param winning_player_id: the winning player ID (symbol), given by the game engine
        """
        return


    @abc.abstractmethod
    def get_next_move(self, game_state):
        """
        Get the next move

        @param game_state: the current game state given by the game engine
        @return: a list with the x and y values of the selected seat
        """
        return


    def set_player_id(self, player_id):
        """
        Set the player's symbol in game

        @param player_id: the symbol used by the player
        """
        self.player_id = player_id
