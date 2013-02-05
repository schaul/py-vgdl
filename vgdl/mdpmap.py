""" 
Transform a subset of (tractable) VGDL games into explicit Markov Decision Processes (MDPS).

Given a game, we want to produce a list of unique, non-redundant discrete states S 
There is a set of permissible discrete actions A.
Actions and states are identified by their index.

We produce a 3D-array of transition probabilities Ts:
    Ts[action_id][from_state_id][to_state_id] = Prob(nextstate=to_state | from_state,action)

We also produce a reward vector for entering each state 
(by default: -1 for losing, +1 for winning, 0 elsewhere)

Finally, we produce a set of features/observations. Two possibilities:
  - fully observable: the observations uniquely determine the underlying state, 
     then they are basically a factored representation of the state
  - partially observable: generally from first-person avatar perspective
  
"""
from scipy import zeros
from pybrain.utilities import flood
from ontology import MovingAvatar, BASEDIRS, RotatingAvatar
from core import VGDLSprite
from tools import listRotate

    
class MDPconverter(object):
    """ Simplest case: Assume the game has a single avatar,
        with 4 actions, outcomes are deterministic, physics are grid-based,
        and all other sprites are Immovables. """
        
    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose=verbose
        self.actions = BASEDIRS
        self.sas_tuples = []
        self.rewards = {}
        self.oriented = False
        
    def convert(self, observations=True):
        if observations:
            obstypes = []
        for skey, ss in sorted(self.game.sprite_groups.items())[::-1]:
            #find avatar
            if len(ss) == 0:
                continue
            if self.verbose:
                print skey, len(ss)
            if isinstance(ss[0], MovingAvatar):
                self.avatar = ss[0]                
            elif observations:
                # retain observable features
                tmp = [self.sprite2state(sprite) for sprite in ss if sprite.is_static]
                obstypes.append(tmp)
        # what type of movement dynamics do we use?
        if isinstance(self.avatar, RotatingAvatar):
            allPos = set([(col, row, dir_) for row in range(self.game.height) 
                          for col in range(self.game.width)
                          for dir_ in BASEDIRS])
            self.oriented = True
        else:
            allPos = set([(col, row) for row in range(self.game.height) 
                          for col in range(self.game.width)])    
        if self.verbose:
            if observations:
                print 'Number of features:', 5*len(obstypes)
            print 'Maximum state space:', len(allPos)
        initSet = [self.sprite2state(self.avatar)]
        self.states = sorted(flood(self.tryMoves, allPos, initSet))
        dim = len(self.states)        
        if self.verbose:
            print 'Actual states:', dim
            print 'Non-negative rewards:', self.rewards
            print 'Initial state', initSet[0]
        Ts = [zeros((dim, dim)) for _ in self.actions]
        R = zeros(dim)
        statedic= {}
        actiondic = {}        
        for si, pos in enumerate(self.states):
            statedic[pos] = si
        for ai, a in enumerate(self.actions):
            actiondic[a] = ai
        for pos, val in self.rewards.items():
            R[statedic[pos]] += val
        for pos, a, dest in self.sas_tuples:
            ai = actiondic[a]
            si = statedic[pos]
            di = statedic[dest]
            Ts[ai][si, di] += 1
        if self.verbose:
            print 'Built Ts.'
        for T in Ts:
            for row in T:  
                row /= sum(row)
        if self.verbose:
            print 'Normalized Ts.'
        if observations:
            # one observation for current position and each of the 4 neighbors.
            fMap = zeros((len(obstypes)*5, dim))
            for si, state in enumerate(self.states):
                if self.oriented:
                    pos = (state[0], state[1])
                else:
                    pos = state 
                for i, p in enumerate([pos]+self.stateNeighbors(state)):
                    for j, obs in enumerate(obstypes):
                        if p in obs:
                            fMap[j*5+i, si] = 1
            if self.verbose:
                print 'Built features.'        
            return Ts, R, fMap
        else:
            return Ts, R

    def stateNeighbors(self, state):
        if self.oriented:
            pos = (state[0], state[1])
        else:
            pos = state
        ns = [(a[0]+pos[0], a[1]+pos[1]) for a in BASEDIRS]
        if self.oriented:
            # subjective perspective, so we rotate the view according to the current orientation
            ns = listRotate(ns, BASEDIRS.index(state[2]))
            return ns
        else:
            return ns
    
    def sprite2state(self, s):
        pos = self.rect2pos(s.rect)
        if self.oriented:
            return (pos[0], pos[1], s.orientation)
        else:
            return pos
        
    def rect2pos(self, r):
        return (r.left / self.game.block_size, r.top / self.game.block_size)
    
    def setRectPos(self, rect, pos):
        rect.left = pos[0] * self.game.block_size
        rect.top = pos[1] * self.game.block_size
        
    def setSpriteState(self, s, state):
        if self.oriented:
            s.orientation = state[2]
            self.setRectPos(s.rect, (state[0], state[1]))
        else:
            self.setRectPos(s.rect, state)
        
    def setState(self, state):
        self.setSpriteState(self.avatar, state)
        self.game.kill_list = []   
        VGDLSprite.update(self.avatar, self.game)            
    
    def tryMoves(self, pos):
        res = []
        for a in self.actions:
            # reset game to starting state
            self.setState(pos)
            # take action and compute consequences
            self.avatar._readMultiActions = lambda *x: [a]
            #self.avatar.physics.activeMovement(self.avatar, a)
            self.avatar.update(self.game)
            self.game._updateCollisionDict()
            self.game._eventHandling()
            # remember the outcome of the action
            dest = self.sprite2state(self.avatar)
            res.append(dest)
            self.sas_tuples.append((pos, a, dest))            
            # remember reward if the final state ends the game
            for t in self.game.terminations[1:]: 
                # Convention: the first criterion is for keyboard-interrupt termination
                ended, win = t.isDone(self.game)
                if ended:
                    if self.verbose:
                        print '    win', win, pos, a, dest
                    if win:
                        self.rewards[dest] = 1
                    else:
                        self.rewards[dest] = -1
        # pass on the list of neighboring states
        return res
    
def testMaze():
    from core import VGDLParser
    from examples.gridphysics.mazes import * #@UnusedWildImport
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    C = MDPconverter(g, verbose=True)
    Ts, R, fMap = C.convert()
    print C.states
    print R
    for T in Ts:
        print T
    print fMap
    
if __name__ == '__main__':
    testMaze()
