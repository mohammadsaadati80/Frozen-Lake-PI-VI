import numpy as np
from gym import Env



def make_map(studentNum): 
    """
    Observation Space : map of environment 
    A 6*6 Grid Graph
    Start point = (0,0)
    End point = (5,5)
    Just one safe path for each Student number
    The probability of falling in each state:
    in safe path = 0.0001 and for other states = 1

    :param 1: Student number 
    
    :return : The Created Map 
    """

    np.random.seed(studentNum)  
    move = np.zeros(10)  # Minimum moves for start to the end point in a 6*6 grid graph
    idx = np.random.choice(range(10),size=5,replace=False)
    move[idx] = 1

    point = [0,0]
    lowprobs = [tuple(point)]

    for m in move:
        if m:
            point[0] += 1
        else:
            point[1] += 1
        lowprobs.append(tuple(point))

    idx = np.array(lowprobs)
    map = np.ones(6,6)
    map[idx[:,0],idx[:,1]] = 0.0001  
    
    map[0,0] = 0.0   # Start point
    map[5,5] = 0.0   # End point

    return map

class FrozenLake(Env):
    def __init__(self):
        """
        Add whatever paramether you need :!

        - Student Number
        - action_space: All available actions the agent can perform.(LEFT = 0,DOWN = 1,RIGHT = 2,UP = 3)
        - observation_space: Structure of the observation.(map of environment)

        Dont forget to reset the environment :)
        """

    def reset(self):
        """
        Reset the state of the environment

        :return: Return the initial state
        """
        pass

    def step(self):
        """
        Perform an action to the environment, provide observation for the new state and provide a reward
        
        :param 1:selected action 

        :return: the next state of the env, the reward of the action, and whether the episode is finished
        """
        pass
        

    def render(self):
        """
        (Optional)
        Render the environment for visualization.
        
        :param 1 = instant state 

        :return: map of environment
        """
        pass

    def close(self): 
        """
        (Optional) : Perform cleanup

        """
    