
import gym
import gym_naoqi

import numpy as np
import random
#from IPython.display import clear_output
import os

"""
    The Nao Q learning for finding most efficient way to move toward an object
    from "Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition"
    by Tom Dietterich
    Description:
    There are 4 designated actions the robot can do. (G) Go forward, (L) Turn Left, (R) Turn Right, (N) Do nothing. 
	When the episode starts, the robot starts off at a random position xy, Nao_rotation and the object is at a random location x'y'. 
	The robot runs sequences of 5 action (ZZZZZ) where Z = (G, L, R, N) 
	Once the object is reached, the episode ends.
    Observations: 
    There are 5 observations needed to be calculated [(xy), Nao_rotation, (x'y')]. the surface need to be desriticized
	
    Actions: 
    There are 4 discrete deterministic actions:
    - 0: Do nothing
    - 1: Go forward
    - 2: Turn Left
    - 3: Turn Right

    
    Rewards: 
    There are reward :
	+100 when reaching the square where object is located, 
	+10 for making move to square closer to object,
	-1 for not changing anyhing,
	-10 for making move to square further from the object,
	
   
    state space:
	xy Nao location
	x'y' Object location
        ((xy), Nao_rotation (x'y'))
    """

# Import and initialize Nao Gym Environment
env = gym.make('naoqi-v0')

# You need to open Webots mannually first and connect it to naoqi controller.

space_obs = env.observation_space
space_act = env.action_space

n_obs = space_obs.n
n_act =  space_act.n

q_table = np.zeros([n_obs, n_act])


import time
"""Training the agent"""

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1


# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, 100001):

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    while not done:
        state = 1
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
#			state = env.action_space.sample()
			action = np.argmax(q_table[state]) # Exploit learned values

        next_state, reward, done, x = env.step(action) 
        next_state = 2
		
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1
        
    if i % 100 == 0:
        clear_output(wait=True)
        print("Episode: {}".format(i))

print("Training finished.\n")

os.mkdir('tempDir')