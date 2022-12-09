import numpy as np
from gym import Env

MAP_SIZE = 6
SLIPPING_PROBABILITY = 0.94
BREAKING_PROBABILITY = 0.0001
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
X = 0
Y = 1

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
    move = np.zeros((MAP_SIZE-1)*2)  # Minimum moves for start to the end point in a 6*6 grid graph
    idx = np.random.choice(range((MAP_SIZE-1)*2),size=(MAP_SIZE-1),replace=False)
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
    map = np.ones((MAP_SIZE,MAP_SIZE))
    map[idx[:,0],idx[:,1]] = BREAKING_PROBABILITY  
    
    map[0,0] = 0.0   # Start point
    map[MAP_SIZE-1,MAP_SIZE-1] = 0.0   # End point

    return map

class FrozenLake(Env):
    def __init__(self, studentNum):
        """
        Add whatever paramether you need :!

        - Student Number
        - action_space: All available actions the agent can perform.(LEFT = 0,DOWN = 1,RIGHT = 2,UP = 3)
        - observation_space: Structure of the observation.(map of environment)

        Dont forget to reset the environment :)
        """
        self.map = make_map(studentNum)
        self.reset()

    def reset(self):
        """
        Reset the state of the environment

        :return: Return the initial state
        """
        self.state = (0,0)
        self.is_finished = False
        return self.state

    def find_next_states(self, action, current_state=None):
        if current_state == None:
            current_state = self.state
        states = np.array([[current_state[X],current_state[Y]-1], [current_state[X]+1,current_state[Y]], [current_state[X],current_state[Y]+1], [current_state[X]-1 ,current_state[Y]]])
        next_states = np.minimum(np.maximum(states, [[0,0]]*4), [[(MAP_SIZE-1),(MAP_SIZE-1)]]*4)
        next_states, counts = np.unique(next_states, axis=0, return_counts=True)
        breaking_possibility = self.map[(np.array(next_states)[:,0]),(np.array(next_states)[:,1])]
        states_probability = counts*((1-SLIPPING_PROBABILITY)/3)
        states_probability[next_states.tolist().index((np.minimum(np.maximum(states[action], [0,0]),[(MAP_SIZE-1),(MAP_SIZE-1)])).tolist())] += (SLIPPING_PROBABILITY-((1-SLIPPING_PROBABILITY)/3)) 
        is_end = [True if state == [(MAP_SIZE-1),(MAP_SIZE-1)] else False for state in next_states.tolist()]
        return next_states, states_probability, breaking_possibility, is_end
    
    def step(self, action): 
        """
        Perform an action to the environment, provide observation for the new state and provide a reward
        
        :param 1:selected action 

        :return: the next state of the env, the reward of the action, and whether the episode is finished
        """
        states, states_probability, breaking_possibility, is_end = self.find_next_states(action)
        random_state = np.random.choice(np.arange(len(states)), p = states_probability)
        is_fall = np.random.rand() < breaking_possibility[random_state]
        reward = -1 + int(is_end[random_state])*100 + int((not is_end[random_state]) and is_fall)*(-10)
        self.is_finished = is_end[random_state] or is_fall
        self.state = tuple(states[random_state])
        return self.state, reward, self.is_finished
        

    def render(self):
        """
        (Optional)
        Render the environment for visualization.
        
        :param 1 = instant state 

        :return: map of environment
        """
        environment_map = ""
        for i in range(MAP_SIZE):
            environment_map += ("\n"+ int(9.33*MAP_SIZE)*"-" + "\n| ")
            for j in range(MAP_SIZE):
                if (i,j) == (0,0):
                    environment_map += "\033[44m{:.4f}\033[0m | ".format(self.map[i,j])
                elif (i,j) == (MAP_SIZE-1,MAP_SIZE-1):
                    environment_map += "\033[42m{:.4f}\033[0m | ".format(self.map[i,j])
                elif self.map[i,j] == BREAKING_PROBABILITY:
                    environment_map += "\033[43m{:.4f}\033[0m | ".format(self.map[i,j])
                else :
                    environment_map += "{:.4f} | ".format(self.map[i,j])           
        environment_map += ("\n" + int(9.33*MAP_SIZE)*"-")
        print(environment_map) 

    def close(self): 
        """
        (Optional) : Perform cleanup

        """