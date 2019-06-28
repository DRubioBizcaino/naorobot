"""
Gym environment for NaoQi
"""

#imports for gym
import gym
from gym import error, spaces, utils
from gym.utils import seeding
#importing our classes
from webot_supervisor import WebotsSupervisor
#from controller import Controller
from model import Model

class NaoqiEnv(gym.Env):
    """This class acts as a wrapper for Naoqi to be used by gym"""
    metadata = {'render.modes': ['human']}

    webots = None
    model = None

    action_space = spaces.discrete.Discrete(4)
    observation_space = spaces.discrete.Discrete(10000)
    #amount of x values*amount of y values*amount of directions

    def __init__(self):
        #creating WebotsSupervisor
        self.webots = WebotsSupervisor()
        self.model = Model()

    def step(self, action):
        # this is the main important function
        # this gets called each delta t
        reward = self.model.step(action)
        state = self.model.get_state()
        done = self.model.is_done()
        if (done):
            reward = 100
        return (state, reward, done, None)#no dictionary rn

    def state(self):
        state = self.model.get_state()
        return (state)

    def reset(self):
        #workaround: restart webots to reset it
        self.webots.restart()
        self.model.restart()
        state = self.model.getState()
        return state

    def render(self, mode='human', close=False):#rendering happens in Webots; can still be "pass"
        pass
