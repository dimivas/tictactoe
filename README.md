# Implementation of Tic-Tac-Toe Agents using Reinforcement Learning techniques 
 
## Project Overview 
 
The goal of this project is to make the machine learn how to play Tic-Tac-Toe, in a board of varying sizes and number of winning seats (winning line size). 
 
The project's domain background is Reinforcement Learning, which is an area of Machine Learning. Reinforcement Learning techniques aim at enabling machines to determine the ideal behavior within an environment, in order to maximize some notion of cumulative reward. 
 
The strategy to achieve the project’s goal was to initially implement the game engine component, a fully functional Tic-Tac-Toe game, and then to implement simple player components, such as the Human Interaction component and the Random Move Selection component. The last and most important part of the project was the implementation of the player components with Reinforcement Learning algorithms. 
 
The algorithms created in this project are mostly based on Q-Learning techniques, which can be used to determine an optimal action-selection policy for a given Markov decision process. 
 
 
## Requirements 

 - python 2.7 or 3
 - tensorflow 1.0 or later
 - numpy 1.11.0 or later
 - argparse
 
 
This project was presented as the Capstone Project for the Machine Learning Engineer Nanodegree. You may find a full report in [docs/ProjectReport.pdf](docs/ProjectReport.pdf)


## Docker image

Give it a try:
'''
docker run -i -t dimivas/tictactoe
'''
