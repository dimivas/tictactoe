from __future__ import print_function

from datetime import datetime
from optparse import OptionParser
import sys
import time

from games import TicTacToeGame
from players import *

all_players = {}
all_players['Naive'] = {'class': TicTacToeComputerNaive, 'instance': None, 'win': 0 }
all_players['Random'] = {'class': TicTacToeComputerRandom, 'instance': None, 'win': 0 }
all_players['Q-Learning'] = {'class': TicTacToeComputerQLearning, 'instance': None, 'win': 0 }
all_players['Tensorflow'] = {'class': TicTacToeComputerTensorflow, 'instance': None, 'win': 0 }

   
def main(p1_class, p2_class, num_of_training_games, num_of_test_games, play_after_test=False):
    start_time = datetime.now()
    all_players[p1_class]['instance'] = all_players[p1_class]['class']()
    all_players[p2_class]['instance'] = all_players[p2_class]['class']()
    plist=[all_players[p1_class], all_players[p2_class]]

    # TRAINING GAMES
    for i in range(num_of_training_games):
        plist.reverse()
        TicTacToeGame(plist[0]['instance'], plist[1]['instance'], be_verbose=False).play()

    # DISABLE RANDOM MOVES
    for player in plist:
        player['instance'].epsilon = 0.0

    # TEST GAMES
    for i in range(num_of_test_games):
        plist.reverse()
        res = TicTacToeGame(plist[0]['instance'], plist[1]['instance'], be_verbose=False).play()
        if res != None:
            plist[res]['win'] += 1

    wins = [ x['win'] for x in plist ]
    draws = num_of_test_games - sum(wins)
    print("{}: {} - {}: {} - Draw: {}".format(p1_class, wins[0], p2_class, wins[1], draws))
   
    if (play_after_test): 
        human = TicTacToeHuman()


parser = OptionParser()
parser.add_option('-1', '--p1',
                      type='choice',
                      action='store',
                      dest='p1',
                      choices=all_players.keys(),
                      help='Type of Player 1',)
parser.add_option('-2', '--p2',
                      type='choice',
                      action='store',
                      dest='p2',
                      choices=all_players.keys(),
                      help='Type of Player 2',)
parser.add_option('-n', '--number-of-training-games',
                      type='int',
                      action='store',
                      dest='number_of_training_games',
                      default=5000,
                      help='Number of training games',)
parser.add_option('-t', '--number-of-test-games',
                      type='int',
                      action='store',
                      dest='number_of_test_games',
                      default=1000,
                      help='Number of test games',)

(options, args) = parser.parse_args()
if not options.p1:
    parser.error('P1 not given')
if not options.p2:
    parser.error('P2 not given')
main(options.p1, options.p2, 
     options.number_of_training_games,
     options.number_of_test_games)
