'''
Demonstration of learning how to play a VGDL game, when full state information 
is *not* available, only observations are (POMDP) 
and we have access to a model of the dynamics (transition probabilities).

We use LSPI as implemented in PyBrain.

@author: Tom Schaul
'''


import pylab
from pybrain.rl.learners.modelbased import LSPI_policy, trueValues, LSTD_PI_policy

from vgdl.mdpmap import MDPconverter
from vgdl.core import VGDLParser
from vgdl.tools import featurePlot



def plotLSPIValues(gametype, layout, discountFactor=0.9, useTD=False):
    # build the game
    g = VGDLParser().parseGame(gametype)
    g.buildLevel(layout)
    
    # transform into an MDP and the mapping to observations
    C = MDPconverter(g)
    Ts, R, fMap = C.convert()
    
    # find the the best least-squares approximation to the policy,
    # given only observations, not the state information
    if useTD:
        # state-based
        _, Tlspi = LSTD_PI_policy(fMap, Ts, R, discountFactor=discountFactor)
    else:
        # state-action-based
        _, Tlspi = LSPI_policy(fMap, Ts, R, discountFactor=discountFactor)
    
    # evaluate the policy
    Vlspi = trueValues(Tlspi, R, discountFactor=discountFactor)
    
    # expected discounted reward at initial state
    Vinit = Vlspi[C.initIndex()]
    
    # plot those values    
    featurePlot((g.width, g.height), C.states, Vlspi)
    pylab.xlabel("V0=%.4f"%Vinit)
    
def test1():
    """ Simple maze """
    from examples.gridphysics.mazes.mazegames import maze_game
    from examples.gridphysics.mazes.simple import maze_level_2
    plotLSPIValues(maze_game, maze_level_2)
    pylab.show()

    
def test2():
    """ Two mazes, two types of movement dynamics. """
    from examples.gridphysics.mazes.mazegames import maze_game, polarmaze_game
    from examples.gridphysics.mazes.simple import maze_level_2, office_layout_2
    pylab.subplot(2,2,1)
    plotLSPIValues(maze_game, maze_level_2)
    pylab.subplot(2,2,2)
    plotLSPIValues(polarmaze_game, maze_level_2)
    pylab.subplot(2,2,3)
    plotLSPIValues(maze_game, office_layout_2)
    pylab.subplot(2,2,4)
    plotLSPIValues(polarmaze_game, office_layout_2)
    pylab.show()
    
    
def test3():
    """ Stochastic maze. """    
    from examples.gridphysics.mazes.windy import windy_stoch_game, windy_level
    pylab.subplot(2,1,1)    
    plotLSPIValues(windy_stoch_game, windy_level)
    pylab.subplot(2,1,2)
    plotLSPIValues(windy_stoch_game, windy_level, useTD=True)
    pylab.show()

if __name__ == '__main__':
    #test1()
    #test2()
    test3()