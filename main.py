from __future__ import print_function

from datetime import datetime
import os
import sys
import time

from tictactoe_game import TicTacToeGame
from tictactoe_human_player import TicTacToeHumanPlayer
from tictactoe_computer_player import TicTacToeCComputerPlayer
from tictactoe_computer_monte_carlo_player import TicTacToeSimpleComputerPlayer
from tictactoe_computer_tensorflow_player import TicTacToeComputerPlayer


def update_progress(progress, start_time):
        perc_progress = int(progress * 100)
        eta = ''
        if (progress > 0.1):
            end_time = datetime.now()
            delta_time = (end_time - start_time).seconds
            remaining_time = ((1 - progress) / progress) * delta_time
            eta = "ETD {} seconds".format(int(remaining_time))
            
        print('\r[{0}] {1}% {2}     '.format(('#'*perc_progress).ljust(100), perc_progress, eta), end='')

#@profile
def main(num_of_training_games=50000):
    #print(">>> TRAINING MODE (COM vs COM) <<<")
    num_of_test_games = 1000
    list_of_players = []
    #list_of_players.append({'name': 'Simple', 'instance': TicTacToeSimpleComputerPlayer(), 'win': 0 })
    list_of_players.append({'name': 'Complex', 'instance': TicTacToeCComputerPlayer(), 'win': 0 })
    list_of_players.append({'name': 'Tensor', 'instance': TicTacToeComputerPlayer(), 'win': 0 })
    #os.system('setterm -cursor off')
    try:
        start_time = datetime.now()
        for i in range(num_of_training_games):
            #update_progress(float(i)/num_of_training_games, start_time)
            list_of_players.reverse()
            TicTacToeGame(list_of_players[0]['instance'], list_of_players[1]['instance'], be_verbose=False).play()
    finally:
        os.system('setterm -cursor on')
    #print('\n\n')
    for player in list_of_players:
        player['instance'].be_verbose = False
        player['instance'].epsilon = 0.0
    for i in range(num_of_test_games):
        list_of_players.reverse()
        res = TicTacToeGame(list_of_players[0]['instance'], list_of_players[1]['instance'], be_verbose=False).play()
        if res != None:
            list_of_players[res]['win'] += 1
    names = [ x['name'] for x in list_of_players ]
    wins = [ x['win'] for x in list_of_players ]
    draws = num_of_test_games - sum(wins)
    print("{} - {}: {} - {}: {} - Draw: {}".format(num_of_training_games, names[0], wins[0], names[1], wins[1], draws))
    """
    h1 = TicTacToeHumanPlayer()
    p1 = list_of_players[0]['instance']
    p2 = list_of_players[1]['instance']
    TicTacToeGame(h1, p2).play()
    time.sleep(2)
    TicTacToeGame(p2, h1).play()
    time.sleep(2)
    TicTacToeGame(h1, p1).play()
    time.sleep(2)
    TicTacToeGame(p1, h1).play()
    time.sleep(2)
    """

if __name__ == '__main__':
    main(int(sys.argv[1]))
