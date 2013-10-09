'''
Created on 2013 2 18

@author: Tom Schaul (schaul@gmail.com)

Wrappers for games to interface them with artificial players.
These are based on the PyBrain RL framework of Environment and Task classes.
'''

from numpy import zeros
import pygame    

from pybrain.rl.environments.environment import Environment
from pybrain.rl.environments.episodic import EpisodicTask

from ontology import BASEDIRS
from core import VGDLSprite
from stateobs import StateObsHandler 

        
    

class GameEnvironment(Environment, StateObsHandler):
    """ Wrapping a VGDL game into an environment class, where state can be read out directly
    or set. Currently limited to single avatar games, with gridphysics, 
    where all other sprites are static. 
    """
    
    # If the visualization is enabled, all actions will be reflected on the screen.
    visualize = False
    
    # In that case, optionally wait a few milliseconds between actions?
    actionDelay = 0
    
    # Recording events (in slightly redundant format state-action-nextstate)
    recordingEnabled = False
        
    def __init__(self, game, actionset=BASEDIRS, **kwargs):
        StateObsHandler.__init__(self, game, **kwargs)
        self._actionset = actionset
        self._initstate = self.getState()
        ns = self._stateNeighbors(self._initstate)
        self.outdim = (len(ns) + 1) * len(self._obstypes)
        self.reset()                
    
    def reset(self):
        self._game._initScreen(self._game.screensize, not self.visualize)
        self.setState(self._initstate)
        # if no avatar starting location is specified, the default one will be to place it randomly
        self._game.randomizeAvatar()    
            
        self._game.kill_list = []
        if self.visualize:
            pygame.display.flip()    
        if self.recordingEnabled:
            self._last_state = self.getState()
            self._allEvents = []            
        self._game.keystate = pygame.key.get_pressed()  
            
    def getSensors(self, state=None):
        if state is None:
            state = self.getState()
        if self.orientedAvatar:
            pos = (state[0], state[1])
        else:
            pos = state 
        res = zeros(self.outdim)
        ns = [pos] + self._stateNeighbors(state)
        for i, n in enumerate(ns):
            os = self._rawSensor(n)
            res[i::len(ns)] = os
        return res
    
    def setState(self, state):
        if self.visualize and self._avatar is not None:
            self._avatar._clear(self._game.screen, self._game.background)        
        StateObsHandler.setState(self, state)        
        self._game._clearAll(self.visualize)  
        assert len(self._game.kill_list) ==0          
        
    def performAction(self, action, onlyavatar=False):
        """ Action is an index for the actionset.  """
        if action is None:
            return   
        # if actions are given as a vector, pick the argmax
        import numpy
        from scipy import argmax
        from pybrain.utilities import drawIndex
        if isinstance(action, numpy.ndarray):
            if abs(sum(action) -1) < 1e5:
                # vector represents probabilities
                action = drawIndex(action)
            else:
                action = argmax(action) 
    
        
        # take action and compute consequences
        self._avatar._readMultiActions = lambda *x: [self._actionset[action]]        
        self._game._clearAll(self.visualize)
        
        # update sprites 
        if onlyavatar:
            self._avatar.update(self._game)
        else:
            for s in self._game:
                s.update(self._game)
        
        # handle collision effects                
        self._game._eventHandling()
        self._game._clearAll(self.visualize)
        
        # update screen
        if self.visualize:
            self._game._drawAll()                            
            pygame.display.update(VGDLSprite.dirtyrects)
            VGDLSprite.dirtyrects = []
            pygame.time.wait(self.actionDelay)       
                       

        if self.recordingEnabled:
            self._previous_state = self._last_state
            self._last_state = self.getState()
            self._allEvents.append((self._previous_state, action, self._last_state))
            
    def _isDone(self):
        # remember reward if the final state ends the game
        for t in self._game.terminations[1:]: 
            # Convention: the first criterion is for keyboard-interrupt termination
            ended, win = t.isDone(self._game)
            if ended:
                return ended, win
        return False, False

    def rollOut(self, action_sequence, init_state=None, callback=lambda * _:None):
        """ Take a sequence of actions. """
        if init_state is not None:
            self.setState(init_state)
        for a in action_sequence:
            print a, self.getState()
            if self._isDone()[0]:
                break
            self.performAction(a)
            callback(self)
        

class GameTask(EpisodicTask):
    """ A minimal Task wrapper that only considers win/loss information. """
    _ended = False
    
    maxSteps = None
    
    def reset(self):
        EpisodicTask.reset(self)
        self.env.reset()
        self._ended = False
        
    def getReward(self):
        self._ended, win = self.env._isDone()
        if self._ended:
            if win:
                return 1
            else:
                return -1
        return 0
        
    def isFinished(self):
        if self.maxSteps is not None:
            if self.samples >= self.maxSteps:
                return True
        return self._ended


   
   
   
# ==========================================================
# some small tests
# ==========================================================
   
    

def testRollout(actions=[0, 0, 2, 2, 0, 3] * 20):        
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1
    from core import VGDLParser
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)    
    env = GameEnvironment(g, visualize=True, actionDelay=100)
    env.rollOut(actions)
        
    
def testRolloutVideo(actions=[0, 0, 2, 2, 0, 3] * 2):        
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1
    from core import VGDLParser
    from tools import makeGifVideo
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    makeGifVideo(GameEnvironment(g, visualize=True), actions)
    
    
def testInteractions():
    from random import randint
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from core import VGDLParser
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1    
    from pybrain.rl.agents.agent import Agent
    
    class DummyAgent(Agent):
        total = 4
        def getAction(self):
            res = randint(0, self.total - 1)
            return res    
        
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    
    env = GameEnvironment(g, visualize=True, actionDelay=100)
    task = GameTask(env)
    agent = DummyAgent()
    exper = EpisodicExperiment(task, agent)
    res = exper.doEpisodes(2)
    print res

def testPolicyAgent():
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from core import VGDLParser
    from examples.gridphysics.mazes import polarmaze_game, maze_level_2
    from agents import PolicyDrivenAgent
    game_str, map_str = polarmaze_game, maze_level_2
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    
    env = GameEnvironment(g, visualize=False, actionDelay=100)
    task = GameTask(env)
    agent = PolicyDrivenAgent.buildOptimal(env)
    env.visualize = True
    env.reset()
    exper = EpisodicExperiment(task, agent)
    res = exper.doEpisodes(2)
    print res
    
def testRecordingToGif(human=False):
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from core import VGDLParser
    from examples.gridphysics.mazes import polarmaze_game, maze_level_2
    from agents import PolicyDrivenAgent, InteractiveAgent    
    from tools import makeGifVideo
    
    game_str, map_str = polarmaze_game, maze_level_2
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    env = GameEnvironment(g, visualize=human, recordingEnabled=True, actionDelay=200)
    task = GameTask(env)
    if human:
        agent = InteractiveAgent()
    else:
        agent = PolicyDrivenAgent.buildOptimal(env)
    exper = EpisodicExperiment(task, agent)
    res = exper.doEpisodes(1)
    print res
    
    actions = [a for _, a, _ in env._allEvents]
    print actions
    makeGifVideo(env, actions, initstate=env._initstate)
    
def testAugmented():
    from core import VGDLParser
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from mdpmap import MDPconverter
    from agents import PolicyDrivenAgent    
    
    
    zelda_level2 = """
wwwwwwwwwwwww
wA wwk1ww   w
ww  ww    1 w
ww     wwww+w
wwwww1ww  www
wwwww  0  Gww
wwwwwwwwwwwww
"""

    
    from examples.gridphysics.mazes.rigidzelda import rigidzelda_game
    g = VGDLParser().parseGame(rigidzelda_game)
    g.buildLevel(zelda_level2)
    env = GameEnvironment(g, visualize=False,
                          recordingEnabled=True, actionDelay=150)
    C = MDPconverter(g, env=env, verbose=True)
    Ts, R, _ = C.convert()
    print C.states
    print Ts[0]
    print R
    env.reset()
    agent = PolicyDrivenAgent.buildOptimal(env)
    env.visualize = True
    env.reset()
    task = GameTask(env)    
    exper = EpisodicExperiment(task, agent)
    exper.doEpisodes(1)
    
    
if __name__ == "__main__":
    #testRollout()
    #testInteractions()
    #testRolloutVideo()
    #testPolicyAgent()
    #testRecordingToGif(human=True)
    testRecordingToGif(human=False)
    #testAugmented()
