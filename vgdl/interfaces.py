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
from pybrain.rl.agents.agent import Agent
    
from ontology import MovingAvatar, RotatingAvatar, BASEDIRS, GridPhysics
from core import VGDLSprite
from tools import listRotate


class GameEnvironment(Environment):
    """ Wrapping a VGDL game into an environment class, where state can be read out directly
    or set. Currently limited to single avatar games, with gridphysics, where all other sprites are static. 
    
    If the visualization is enabled, all actions will be reflected on the screen."""
    def __init__(self, game, actionset=BASEDIRS, visualize=False, actionDelay=0):
        self.visualize = visualize
        self._actionDelay = actionDelay
        self._game = game
        self._actionset = actionset
        self._obstypes = {}
        self._obscols = {}
        for skey, ss in sorted(game.sprite_groups.items())[::-1]:
            if len(ss) == 0:
                continue
            if isinstance(ss[0], MovingAvatar):
                # find avatar
                assert len(ss) == 1, 'Not supported: Only a single avatar can be used.'
                self._avatar = ss[0]
                assert issubclass(self._avatar.physicstype, GridPhysics), \
                                    'Not supported: Game must have grid physics, has %s'\
                                    % (self._avatar.physicstype.__name__)   
                if isinstance(self._avatar, RotatingAvatar):
                    self._oriented = True
                else:
                    self._oriented = False                
            else:
                # retain observable features
                tmp = [self._sprite2state(sprite, oriented=False) for sprite in ss if sprite.is_static]
                self._obstypes[skey] = tmp
                self._obscols[skey] = ss[0].color
                assert ss[0].is_static, "not supported: all non-avatar sprites must be static. "
        self._initstate = self.getState()
        ns = self._stateNeighbors(self._initstate)
        self.outdim = (len(ns) + 1) * len(self._obstypes)
        self.reset()        
    
    def reset(self):
        self.setState(self._initstate)
        self._game.kill_list = []
        if self.visualize:
            self._game._initScreen(self._game.screensize)
            pygame.display.flip()    
    
    def _sprite2state(self, s, oriented=None):
        pos = self._rect2pos(s.rect)
        if oriented is None and self._oriented:
            return (pos[0], pos[1], s.orientation)
        else:
            return pos
        
    def _rect2pos(self, r):
        return (r.left / self._game.block_size, r.top / self._game.block_size)
    
    def _setRectPos(self, rect, pos):
        rect.left = pos[0] * self._game.block_size
        rect.top = pos[1] * self._game.block_size
        
    def _setSpriteState(self, s, state):
        if self._oriented:
            s.orientation = state[2]
            self._setRectPos(s.rect, (state[0], state[1]))
        else:
            self._setRectPos(s.rect, state)
            

    def _stateNeighbors(self, state):
        """ Can be different in subclasses... 
        
        By default: current position and four neighbors. """
        if self._oriented:
            pos = (state[0], state[1])
        else:
            pos = state
        ns = [(a[0] + pos[0], a[1] + pos[1]) for a in BASEDIRS]
        if self._oriented:
            # subjective perspective, so we rotate the view according to the current orientation
            ns = listRotate(ns, BASEDIRS.index(state[2]))
            return ns
        else:
            return ns
        
    def setState(self, state):
        self._setSpriteState(self._avatar, state)
        self._game.kill_list = []   
        VGDLSprite.update(self._avatar, self._game)           
        
    def getState(self):
        return self._sprite2state(self._avatar)
    
    def allStates(self):
        if self._oriented:
            return [(col, row, dir_) for row in range(self._game.height) 
                          for col in range(self._game.width)
                          for dir_ in BASEDIRS]
        else:
            return [(col, row) for row in range(self._game.height) 
                          for col in range(self._game.width)]  
    
    def getSensors(self, state=None):
        if state is None:
            state = self.getState()
        if self._oriented:
            pos = (state[0], state[1])
        else:
            pos = state 
        res = zeros(self.outdim)
        ns = [pos] + self._stateNeighbors(state)
        for i, n in enumerate(ns):
            os = self._rawSensor(n)
            res[i::len(ns)] = os
        return res
    
    def _rawSensor(self, state):
        return [(state in ostates) for _, ostates in sorted(self._obstypes.items())[::-1]]

    def performAction(self, action, onlyavatar=False):
        """ Action is an index for the actionset.  """
        if action is None:
            return   
        # take action and compute consequences
        self._avatar._readMultiActions = lambda * x: [self._actionset[action]]        

        if self.visualize:
            self._game._clearAll()            

        # update sprites 
        if onlyavatar:
            self._avatar.update(self._game)
        else:
            for s in self._game:
                s.update(self._game)

        # handle collision effects                
        self._game._updateCollisionDict()
        self._game._eventHandling()
        
        # update screen
        if self.visualize:
            self._game._drawAll()                            
            pygame.display.update(VGDLSprite.dirtyrects)
            VGDLSprite.dirtyrects = []
            pygame.time.wait(self._actionDelay)                  

        
    def _isDone(self):
        # remember reward if the final state ends the game
        for t in self._game.terminations[1:]: 
            # Convention: the first criterion is for keyboard-interrupt termination
            ended, win = t.isDone(self._game)
            if ended:
                return ended, win
        return False, False

    def rollOut(self, action_sequence, init_state=None, callback=lambda *_:None):
        """ Take a sequence of actions. """
        if init_state is not None:
            self.setState(init_state)
        for a in action_sequence:
            if self._isDone()[0]:
                break
            self.performAction(a)
            callback(self)
        

class GameTask(EpisodicTask):
    """ A minimal Task wrapper that only considers win/loss information. """
    _ended = False
    
    def reset(self):
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
        return self._ended


class InteractiveAgent(Agent):
    """ Reading key commands from the user. """
       
    def getAction(self):
        from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
        from ontology import RIGHT, LEFT, UP, DOWN
        pygame.event.pump()
        keystate = pygame.key.get_pressed()    
        res = None
        if   keystate[K_RIGHT]: res = BASEDIRS.index(RIGHT)
        elif keystate[K_LEFT]:  res = BASEDIRS.index(LEFT)
        elif   keystate[K_UP]:    res = BASEDIRS.index(UP)
        elif keystate[K_DOWN]:  res = BASEDIRS.index(DOWN)
        return res


def makeGifVideo(game, actions, prefix='seq_', duration=0.1, 
                 outdir='../gifs/', tmpdir='../temp/'):
    """ Generate an animated gif from a sequence of actions. """
    from external_libs.images2gif import writeGif
    import Image 
    env = GameEnvironment(game, visualize=True)
    env._counter = 1
    res_images = []
    astring = ''.join([str(a) for a in actions if a is not None])
    
    def cb(*_):
        fn = tmpdir+"tmp%05d.png" %  env._counter
        pygame.image.save(game.screen, fn)
        res_images.append(Image.open(fn))
        env._counter += 1
        
    env.rollOut(actions, callback=cb)
    writeGif(outdir+prefix+'%s.gif' % astring, res_images, duration=duration, dither=0)
    
    

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
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    makeGifVideo(g, actions)
    
    
def testInteractions():
    from random import randint
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from core import VGDLParser
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1
    
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

    
if __name__ == "__main__":
    # testRollout()
    # testInteractions()
    testRolloutVideo()
    
