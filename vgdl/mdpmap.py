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
from pybrain.utilities import flood
from ontology import MovingAvatar, BASEDIRS
from core import VGDLSprite

    
class MDPconverter(object):
    """ Simplest case: Assume the game has a single avatar,
        with 4 actions, outcomes are deterministic, physics are grid-based,
        and all other sprites are Immovables. """
        
    def __init__(self, game):
        self.game = game
        obstypes = []
        allPos = set([(col, row) for row in range(game.height) for col in range(game.width)])    
        for key, ss in game.sprite_groups.items():
            print key, len(ss), ss[0]
            if isinstance(ss[0], MovingAvatar):
                self.avatar = ss[0]
            else:
                tmp = [self.rect2pos(sprite.rect) for sprite in ss if sprite.is_static]
                print sorted(set(tmp))
                obstypes.append(tmp)
        initSet = [self.rect2pos(self.avatar.rect)]
        self.actions = BASEDIRS
        self.sas_tuples = {}
        self.rewards = {}
        print sorted(allPos)
        print initSet
        self.states = sorted(flood(self.tryMoves, allPos, initSet))
        print self.states
        print self.rewards
        print len(self.sas_tuples)


    
    
    def rect2pos(self, r):
        return (r.left/self.game.block_size, r.top/self.game.block_size)
    
    def setRectPos(self, r, pos):
        r.left = pos[0]*self.game.block_size
        r.top = pos[1]*self.game.block_size
    
    def tryMoves(self, pos):
        res = []
        for a in self.actions:
            # reset game to starting state
            self.setRectPos(self.avatar.rect, pos)
            self.game.kill_list = []   
            VGDLSprite.update(self.avatar, self.game)
            # take action and compute consequences
            self.avatar.physics.activeMovement(self.avatar, a)
            self.game._updateCollisionDict()
            self.game._eventHandling()
            # remember the outcome of the action
            dest = self.rect2pos(self.avatar.rect)
            res.append(dest)
            self.sas_tuples[(pos, a)] = dest            
            # remember reward if the final state ends the game
            for t in self.game.terminations[1:]: 
                # Convention: the first criterion is for keyboard-interrupt termination
                ended, win = t.isDone(self.game)
                if ended:
                    print 'win', win, pos, a, dest
                    if win:
                        self.rewards[dest] = 1
                    else:
                        self.rewards[dest] = -1
        # pass on the list of neighboring states
        return res
    
def testMaze():
    from core import VGDLParser
    from examples.gridphysics.mazes import maze_game, maze_level_1
    game_str, map_str = maze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    MDPconverter(g)
    
if __name__ == '__main__':
    testMaze()
