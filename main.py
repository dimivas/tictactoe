from __future__ import print_function

from datetime import datetime
import os
import time

from tictactoe_game import TicTacToeGame
from tictactoe_human_player import TicTacToeHumanPlayer
from tictactoe_computer_player import TicTacToeComputerPlayer


def update_progress(progress, start_time):
        perc_progress = int(progress * 100)
        eta = ''
        if (progress > 0.1):
            end_time = datetime.now()
            delta_time = (end_time - start_time).seconds
            remaining_time = ((1 - progress) / progress) * delta_time
            eta = "ETD {} seconds".format(int(remaining_time))
            
        print('\r[{0}] {1}% {2}     '.format(('#'*perc_progress).ljust(100), perc_progress, eta), end='')


print(">>> TRAINING MODE (COM vs COM) <<<")
num_of_training_games = 50000
p1 = TicTacToeComputerPlayer('X')
p2 = TicTacToeComputerPlayer('O')
os.system('setterm -cursor off')
try:
    start_time = datetime.now()
    for i in range(num_of_training_games):
        update_progress(float(i)/num_of_training_games, start_time)
        TicTacToeGame(p1, p2).play(be_verbose=False)
finally:
    os.system('setterm -cursor on')
print('\n\n')
p2.be_verbose = True
h1 = TicTacToeHumanPlayer('X')
while(True):
    time.sleep(2)
    TicTacToeGame(h1, p2).play()
    time.sleep(2)
    TicTacToeGame(p1, h1).play()
