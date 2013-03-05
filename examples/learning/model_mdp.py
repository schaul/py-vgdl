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
from vgdl.tools import featurePlot


    
def plotOptimalValues(gametype, layout, discountFactor=0.9):
    g = VGDLParser().parseGame(gametype)
    g.buildLevel(layout)
    C = MDPconverter(g)
    Ts, R, _ = C.convert()
    _, Topt = policyIteration(Ts, R, discountFactor=discountFactor)
    Vopt = trueValues(Topt, R, discountFactor=discountFactor)    
    featurePlot((g.width, g.height), C.states, Vopt)
    
    
def test1():
    from examples.gridphysics.mazes.mazegames import maze_game
    from examples.gridphysics.mazes.simple import maze_level_2
    plotOptimalValues(maze_game, maze_level_2)
    pylab.show()

    
def test2():
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
    
    
if __name__ == '__main__':
    test2()