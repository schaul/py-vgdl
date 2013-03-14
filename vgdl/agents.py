'''
Created on 2013 3 12

@author: Tom Schaul (schaul@gmail.com)

Wrappers for agent classes that interface to games.
These are based on the PyBrain RL framework of Agent classes.
'''


import pygame
from pybrain.rl.agents.agent import Agent
from pybrain.rl.learners.modelbased import policyIteration
from pybrain.utilities import drawIndex

from ontology import BASEDIRS

class UserTiredException(Exception):
    """ Raised when the player is fed up of the game. """
    

class InteractiveAgent(Agent):
    """ Reading key commands from the user. """
       
    def getAction(self):
        from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
        from pygame.locals import K_ESCAPE, QUIT        
        from ontology import RIGHT, LEFT, UP, DOWN
        pygame.event.pump()
        keystate = pygame.key.get_pressed()    
        res = None
        if   keystate[K_RIGHT]: res = BASEDIRS.index(RIGHT)
        elif keystate[K_LEFT]:  res = BASEDIRS.index(LEFT)
        elif keystate[K_UP]:    res = BASEDIRS.index(UP)
        elif keystate[K_DOWN]:  res = BASEDIRS.index(DOWN)        
        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            raise UserTiredException('Pressed ESC')
        return res
    

class PolicyDrivenAgent(Agent):
    """ Taking actions according to a (possibly stochastic) policy that has 
    full state information (state index). """
    
    def __init__(self, policy, stateIndexFun):
        self.policy = policy
        self.stateIndexFun = stateIndexFun
    
    def getAction(self):
        return drawIndex(self.policy[self.stateIndexFun()])
            
    @staticmethod
    def buildOptimal(game_env, discountFactor=0.99):
        """ Given a game, find the optimal (state-based) policy and 
        return an agent that is playing accordingly. """
        from mdpmap import MDPconverter
        C = MDPconverter(env=game_env)
        Ts, R, _ = C.convert()
        policy, _ = policyIteration(Ts, R, discountFactor=discountFactor)
        game_env.reset()

        def x(*_):
            s = game_env.getState()
            #print s
            i = C.states.index(s)
            return i
        #return PolicyDrivenAgent(policy, lambda *_: C.states.index(game_env.getState()))
        return PolicyDrivenAgent(policy, x)