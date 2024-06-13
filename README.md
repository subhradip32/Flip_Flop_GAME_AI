# Flappy Bird AI
This is a flappy bird game created using python only, which train and use the trained neural network in the Game itself using the NEAT aqlgorithm. 

## Flappy Bird 
Flappy Bird is a 2013 casual game developed by Vietnamese video game artist and programmer Dong Nguyen (Vietnamese: Nguyễn Hà Đông), under his game development company .Gears.[1] The game is a side-scroller where the player controls a bird attempting to fly between columns of green pipes without hitting them. The player's score is determined by the number of pipes they pass. Nguyen created the game over a period of several days, using the bird from a cancelled game made in 2012.
The game was released in May 2013 but received a sudden spike in popularity in early 2014, becoming a sleeper hit. Flappy Bird received poor reviews from some critics, who criticized its high level of difficulty and alleged plagiarism in graphics and game mechanics, while other reviewers found it addictive. At the end of January 2014, it was the most downloaded free game in the App Store for iOS. During this period, its developer said that Flappy Bird was earning $50,000 a day from in-app advertisements as well as sales.
Flappy Bird was removed from both the App Store and Google Play on February 10, 2014, with Nguyen claiming that he felt guilty over what he considered to be the game's addictive nature and overusage. Its popularity and sudden removal caused phones with the game installed before its removal to be put up for sale for high prices over the Internet.[2][3] Clones of Flappy Bird became popular on the App Store after the original app's removal, and both Apple and Google have removed games from their app stores for being too identical.
![image](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/8dd42df2-3006-4ad2-a302-8185a1a863d6)

## NEAT Algorithm
NEAT (NeuroEvolution of Augmenting Topologies) is an evolutionary algorithm that creates artificial neural networks. For a detailed description of the algorithm, you should probably go read some of Stanley’s papers on his website.
Even if you just want to get the gist of the algorithm, reading at least a couple of the early NEAT papers is a good idea. Most of them are pretty short, and do a good job of explaining concepts (or at least pointing you to other references that will). The initial NEAT paper is only 6 pages long, and Section II should be enough if you just want a high-level overview.
In the current implementation of NEAT-Python, a population of individual genomes is maintained. Each genome contains two sets of genes that describe how to build an artificial neural network:
Node genes, each of which specifies a single neuron.
Connection genes, each of which specifies a single connection between neurons.
To evolve a solution to a problem, the user must provide a fitness function which computes a single real number indicating the quality of an individual genome: better ability to solve the problem means a higher score. The algorithm progresses through a user-specified number of generations, with each generation being produced by reproduction (either sexual or asexual) and mutation of the most fit individuals of the previous generation.
![image](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/fba6a963-b8b6-4eef-b01b-37e9cef70b07)

# Module Used
I had tried to use the most of the famous modules to create this game to help me and the user understand how the neat-ai works. 
```
import neat.population
import neat.reproduction
import pygame 
import neat 
import pickle
import os 
import random
```
To install these modules in your device you can install it seperately or can use the below command on your terminal to install it using the **PIP command** .
```
pip install neat-python pygame
```

# Terminal Output
This below screenshot help us to visualise how the AI works using the custom INPUT and OUTPUT. 
![Screenshot 2024-06-13 221502](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/2498f9a6-9708-4577-ad32-74d995f11daf)

# OUTPUTS
![Screenshot 2024-06-13 221330](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/79fee747-0787-42bd-bb34-14dc5207b7e7)
![Screenshot 2024-06-13 221320](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/3081a8ab-a0e1-453b-9f1b-62e1d2916baa)
![Screenshot 2024-06-13 221428](https://github.com/subhradip32/Flip_Flop_GAME_AI/assets/83198378/dc93b8a0-c984-4863-b0ed-18d6d77e8d65)
