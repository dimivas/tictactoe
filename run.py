from __future__ import print_function

from datetime import datetime
import argparse
import sys
import time

from games import TicTacToeGame
from players import *

all_players = {}
all_players['Naive'] = {'class': TicTacToeComputerNaive, 'instance': None, 'win': 0 }
all_players['Random'] = {'class': TicTacToeComputerRandom, 'instance': None, 'win': 0 }
all_players['Q-Learning'] = {'class': TicTacToeComputerQLearning, 'instance': None, 'win': 0 }
all_players['Tensorflow'] = {'class': TicTacToeComputerTensorflow, 'instance': None, 'win': 0 }

   
def main(p1_class, p2_class, num_of_training_games, num_of_test_games, play_after_train=False):
    start_time = datetime.now()
    all_players[p1_class]['instance'] = all_players[p1_class]['class']()
    all_players[p2_class]['instance'] = all_players[p2_class]['class']()
    plist = [all_players[p1_class], all_players[p2_class]]

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

    if play_after_train:
        time.sleep(5)
        hlist = [TicTacToeHuman(), plist[0]['instance']]
        while (True):
            TicTacToeGame(*hlist, be_verbose=True).play()
            time.sleep(5)
            hlist.reverse()

parser = argparse.ArgumentParser(description='Implementation of Tic-Tac-Toe Agents using Reinforcement Learning techniques')
parser.add_argument('-1', '--p1',
                      action='store',
                      dest='p1',
                      choices=all_players.keys(),
                      required=True,
                      help='Type of Player 1',)
parser.add_argument('-2', '--p2',
                      action='store',
                      dest='p2',
                      choices=all_players.keys(),
                      required=True,
                      help='Type of Player 2',)
parser.add_argument('-n', '--number-of-training-games',
                      type=int,
                      action='store',
                      dest='number_of_training_games',
                      default=5000,
                      help='Number of training games',)
parser.add_argument('-t', '--number-of-test-games',
                      type=int,
                      action='store',
                      dest='number_of_test_games',
                      default=1000,
                      help='Number of test games',)
parser.add_argument('-p', '--play-after-train',
                      action='store_true',
                      dest='play_after_train',
                      help='Play after training with com player 1')
args = parser.parse_args()
main(args.p1, args.p2, 
     args.number_of_training_games,
     args.number_of_test_games,
     play_after_train=args.play_after_train)
