'''
Demonstration of learning how to play a VGDL game, when full state information is available (MDP) 
and we have access to a model of the dynamics (transition probabilities).

We use policy iteration as implemented in PyBrain.

@author: Tom Schaul
'''


import pylab
from pybrain.rl.learners.modelbased import policyIteration, trueValues

from vgdl.mdpmap import MDPconverter
from vgdl.core import VGDLParser
from vgdl.plotting import featurePlot


from matplotlib import rc
rc('text', usetex=False)
    
def plotOptimalValues(gametype, layout, discountFactor=0.9, showValue=False):
    # build the game
    g = VGDLParser().parseGame(gametype)
    g.buildLevel(layout)
    
    # transform into an MDP
    C = MDPconverter(g)
    Ts, R, _ = C.convert()
    
    # find the optimal policy
    _, Topt = policyIteration(Ts, R, discountFactor=discountFactor)
    
    # evaluate the policy
    Vopt = trueValues(Topt, R, discountFactor=discountFactor)
        
    # plot those values    
    featurePlot((g.width, g.height), C.states, Vopt, plotdirections=True)
    
    if showValue:
        # expected discounted reward at initial state
        Vinit = Vopt[C.initIndex()]
        pylab.xlabel("V0=%.4f"%Vinit)
    
    
def test1():
    """ Simple maze """
    from examples.gridphysics.mazes.mazegames import maze_game
    from examples.gridphysics.mazes.simple import maze_level_2
    plotOptimalValues(maze_game, maze_level_2)
    pylab.show()

    
def test2():
    """ Two mazes, two types of movement dynamics. """
    from examples.gridphysics.mazes.mazegames import maze_game, polarmaze_game
    from examples.gridphysics.mazes.simple import maze_level_2, office_layout_2
    pylab.subplot(2,2,1)
    plotOptimalValues(maze_game, maze_level_2)
    pylab.subplot(2,2,2)
    plotOptimalValues(polarmaze_game, maze_level_2)
    pylab.subplot(2,2,3)
    plotOptimalValues(maze_game, office_layout_2)
    pylab.subplot(2,2,4)
    plotOptimalValues(polarmaze_game, office_layout_2)
    pylab.show()
    
def test3():
    """ Stochastic maze. """    
    from examples.gridphysics.mazes.windy import windy_stoch_game, windy_level
    plotOptimalValues(windy_stoch_game, windy_level)
    pylab.show()
    
def test4():
    """ Same thing, but animated. """
    from examples.gridphysics.mazes.windy import windy_stoch_game, windy_level
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from vgdl.interfaces import GameEnvironment, GameTask
    from vgdl.agents import PolicyDrivenAgent 
    g = VGDLParser().parseGame(windy_stoch_game)
    g.buildLevel(windy_level)
    env = GameEnvironment(g, visualize=True, actionDelay=100)
    task = GameTask(env)
    agent = PolicyDrivenAgent.buildOptimal(env)
    exper = EpisodicExperiment(task, agent)
    res = exper.doEpisodes(5)
    print res
    
def test5():
    from examples.gridphysics.mazes.mazegames import maze_game, flippolarmaze_game
    from examples.gridphysics.mazes.noisyobservations import maze_89
    pylab.subplot(1,2,1)
    plotOptimalValues(maze_game, maze_89)
    pylab.subplot(1,2,2)
    plotOptimalValues(flippolarmaze_game, maze_89)
    pylab.show()
    
if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    #test4()
    test5()