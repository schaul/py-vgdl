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
from ontology import BASEDIRS
from interfaces import GameEnvironment


class MDPconverter(object):
    """ Simple case: Assume the game has a single avatar,
        physics are grid-based, and all other sprites are Immovables. 
    """
            
    def __init__(self, game=None, verbose=False, actionset=BASEDIRS, env=None, avgOver=10):
        if env is None:
            env = GameEnvironment(game, actionset=actionset)
        self.env = env
        self.verbose = verbose
        self.sas_tuples = []
        self.rewards = {}
        if env._game.is_stochastic:
            # in the stochastic case, how often is every state-action pair tried?
            self.avgOver = avgOver
        else:
            self.avgOver = 1
            
    def convert(self, observations=True):
        if self.verbose:
            if observations:
                print 'Number of features:', 5 * len(self.env._obstypes)
        initSet = [self.env._initstate]
        self.states = sorted(flood(self.tryMoves, None, initSet))
        dim = len(self.states)        
        if self.verbose:
            print 'Actual states:', dim
            print 'Non-zero rewards:', self.rewards
            print 'Initial state', initSet[0]
        Ts = [zeros((dim, dim)) for _ in self.env._actionset]
        R = zeros(dim)
        statedic = {}
        actiondic = {}        
        for si, pos in enumerate(self.states):
            statedic[pos] = si
        for ai, a in enumerate(self.env._actionset):
            actiondic[a] = ai
        for pos, val in self.rewards.items():
            R[statedic[pos]] += val
        for pos, a, dest in self.sas_tuples:
            ai = actiondic[a]
            si = statedic[pos]
            di = statedic[dest]
            Ts[ai][si, di] += 1. / self.avgOver
        if self.verbose:
            print 'Built Ts.'
        for T in Ts:
            for ti, row in enumerate(T):
                if sum(row) > 0:  
                    row /= sum(row)
                else:
                    row[ti] = 1
        if self.verbose:
            print 'Normalized Ts.'
        if observations:
            # one observation for current position and each of the 4 neighbors.
            fMap = zeros((len(self.env._obstypes) * 5, dim))
            for si, state in enumerate(self.states):
                fMap[:, si] = self.env.getSensors(state)                
            if self.verbose:
                print 'Built features.'        
            return Ts, R, fMap
        else:
            return Ts, R
        
    def initIndex(self):
        return self.states.index(self.env._initstate)
        
    def tryMoves(self, state):
        res = []
        if state in self.rewards:
            return res
        for ai, a in self.avgOver * list(enumerate(self.env._actionset)):
            # reset game to starting state
            self.env.setState(state)
            self.env.performAction(ai)
            # remember the outcome of the action
            dest = self.env.getState()
            res.append(dest)
            if self.verbose:
                print state, 'do', a, '>', dest
            self.sas_tuples.append((state, a, dest))            
            # remember reward if the final state ends the game
            ended, win = self.env._isDone()
            if ended:
                if win:
                    self.rewards[dest] = 1
                else:
                    self.rewards[dest] = -1
                if self.verbose:
                    print 'Ends with', win
        # pass on the list of neighboring states
        return res
        
                        
def testMaze():
    from core import VGDLParser
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1
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

def testStochMaze():
    from core import VGDLParser
    from examples.gridphysics.mazes.stochastic import stoch_game, stoch_level
    g = VGDLParser().parseGame(stoch_game)
    g.buildLevel(stoch_level)
    C = MDPconverter(g, verbose=True)
    Ts, R, fMap = C.convert()
    print C.states
    print R
    for T in Ts:
        print T
    print fMap

    
if __name__ == '__main__':
    # testMaze()
    testStochMaze()
