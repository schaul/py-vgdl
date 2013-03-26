'''
Demonstration of learning how to play a VGDL game, when full state information 
is *not* available, only observations are, and furthermore, 
we don't have access to a model of the dynamics, only to a finite number of rollout sequences.

We use a neural network controller trained by the SNES algorithm.

@author: Tom Schaul
'''

from vgdl.interfaces import GameEnvironment, GameTask
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.agents import LearningAgent
import pylab
from vgdl.core import VGDLParser
from vgdl.plotting import featurePlot, addTrajectory
    
#TODO: random starting points
    
    
def someEpisodes(game_env, net, discountFactor=0.99, maxSteps=100, avgOver=1, returnEvents=False):
    """ Return the fitness value for one episode of play, given the policy defined by a neural network. """
    task = GameTask(game_env)
    game_env.recordingEnabled = True        
    game_env.reset()        
    net.reset()
    task.maxSteps=maxSteps
    agent = LearningAgent(net)
    agent.learning = False
    agent.logging = False
    exper = EpisodicExperiment(task, agent)
    fitness = 0
    for _ in range(avgOver):
        rs = exper.doEpisodes(1)
        # add a slight bonus for more exploration, if rewards are identical
        fitness += len(set(game_env._allEvents)) * 1e-6
        # the true, discounted reward        
        fitness += sum([sum([v*discountFactor**step for step, v in enumerate(r)]) for r in rs])
    fitness /= avgOver
    if returnEvents:
        return fitness, game_env._allEvents
    else:
        return fitness

    
def buildNet(indim, hidden, outdim=2, temperature=1., recurrent=True):
    from pybrain import FullConnection, BiasUnit, TanhLayer, SoftmaxLayer, RecurrentNetwork, LinearLayer, LinearConnection, FeedForwardNetwork, SigmoidLayer
    if recurrent:
        net = RecurrentNetwork()
    else:
        net = FeedForwardNetwork()
    net.addInputModule(LinearLayer(indim, name = 'i'))
    net.addModule(TanhLayer(hidden, name = 'h'))
    net.addModule(BiasUnit('bias'))
    net.addModule(SigmoidLayer(outdim, name = 'unscaled'))
    net.addOutputModule(SoftmaxLayer(outdim, name = 'o'))
    net.addConnection(FullConnection(net['i'], net['h']))
    net.addConnection(FullConnection(net['bias'], net['h']))
    net.addConnection(FullConnection(net['bias'], net['unscaled']))
    net.addConnection(FullConnection(net['h'], net['unscaled']))
    lconn = LinearConnection(net['unscaled'], net['o'])
    lconn._setParameters([1./temperature]*outdim)
    # these are fixed. 
    lconn.paramdim = 0
    net.addConnection(lconn)
    if recurrent:
        net.addRecurrentConnection(FullConnection(net['h'], net['h']))
    net.sortModules()
    print  net
    print 'number of parameters', net.paramdim
    return net

def test1():
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1    
    
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    
    game_env = GameEnvironment(g)
    print 'number of observations:', game_env.outdim
    
    net = buildNet(game_env.outdim, 2, 2)
    for i in range(200):
        net.randomize()
        net.reset()
        print someEpisodes(game_env, net),
        if i% 20 == 19:
            print


def plotBackground(env, known=[[]]):
    if len(known[0]) == 0:
        from vgdl.mdpmap import MDPconverter
        g = env._game
        C = MDPconverter(g, env=env, verbose=False)
        _, R, _ = C.convert()
        size = (g.width, g.height)
        known[0].append((size, C.states, R))
    featurePlot(*known[0][0])
    
    
def plotTrajectories(env, net, num_traj=5):
    cols = ['r', 'c', 'b', 'g', 'y']
    
    for ci in range(num_traj):
        fit, alls = someEpisodes(env, net, returnEvents=True)
        print fit, len(alls),
        if len(alls) == 0:
            print 'Oops?'
            continue
        sseq = [s for s, _, _ in alls]+[alls[-1][-1]]
        addTrajectory(sseq, cols[ci%len(cols)])
    print
        
def test2():
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1    
    from pybrain.optimization import SNES
    
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    game_env = GameEnvironment(g, actionDelay=100, recordingEnabled=True)
    net = buildNet(game_env.outdim, 6, 2)
    
    algo = SNES(lambda x: someEpisodes(game_env, x), net, verbose=True, desiredEvaluation=0.43)
    rows, cols = 3,3
    episodesPerStep = 2
    for i in range(rows*cols):
        pylab.subplot(rows, cols, i+1)
        algo.learn(episodesPerStep)
        net._setParameters(algo.bestEvaluable)
        plotBackground(game_env)    
        plotTrajectories(game_env, net)
        pylab.title(str((i+1)*episodesPerStep))
        if algo.desiredEvaluation <= algo.bestEvaluation:
            break
        print
    pylab.show()
    
def test3():
    from examples.gridphysics.mazes.simple import office_layout_2, consistent_corridor
    from examples.gridphysics.mazes import polarmaze_game
    from pybrain.optimization import SNES
    g = VGDLParser().parseGame(polarmaze_game)
    g.buildLevel(consistent_corridor)
    game_env = GameEnvironment(g)
    net = buildNet(game_env.outdim, 4, 4, temperature=0.05, recurrent=False)
    
    algo = SNES(lambda x: someEpisodes(game_env, x), net, verbose=True, desiredEvaluation=0.78)
    rows, cols = 2,2
    episodesPerStep = 3
    for i in range(rows*cols):
        pylab.subplot(rows, cols, i+1)
        algo.learn(episodesPerStep)
        net._setParameters(algo.bestEvaluable)
        plotBackground(game_env)    
        plotTrajectories(game_env, net)
        pylab.title(str((i+1)*episodesPerStep))
        if algo.desiredEvaluation <= algo.bestEvaluation:
            break
        print
    pylab.show()
    

# a maze with loops, and simple reactive solution (stay left) 
labyrinth1 = """
wwwwwwwwwwwww
w       w   w
w  www    w w
w w  wwAwww w
w w wwwww   w
w   w  Gww ww
w  ww www w w
w     w  w ww
wwwwwwwwwwwww
"""

labyrinth2 = """
wwwwwwwwwwwww
w       ww ww
w  wwww     w
w w  wwAww ww
w w wwwwGw  w
w   w    ww w
w  ww ww    w
w        w ww
wwwwwwwwwwwww
"""
    
    
def test4():
    from numpy import ndarray
    from examples.gridphysics.mazes import polarmaze_game
    from pybrain.optimization import SNES, WeightGuessing
    g = VGDLParser().parseGame(polarmaze_game)
    g.buildLevel(labyrinth2)
    game_env = GameEnvironment(g)
    net = buildNet(game_env.outdim, 5, 4, temperature=0.1, recurrent=False)
    
    algo = SNES(lambda x: someEpisodes(game_env, x, avgOver=3), net, verbose=True, desiredEvaluation=0.75)
    #algo = WeightGuessing(lambda x: someEpisodes(game_env, x), net, verbose=True, desiredEvaluation=0.78)
    rows, cols = 2,2
    episodesPerStep = 4
    for i in range(rows*cols):
        pylab.subplot(rows, cols, i+1)
        algo.learn(episodesPerStep)
        if isinstance(algo.bestEvaluable, ndarray):
            net._setParameters(algo.bestEvaluable)
        else:
            net = algo.bestEvaluable
        plotBackground(game_env)    
        plotTrajectories(game_env, net)
        pylab.title(str((i+1)*episodesPerStep))
        if algo.desiredEvaluation <= algo.bestEvaluation:
            break
        print
    pylab.show()
    
    
    
def test5():
    from numpy import ndarray
    from examples.gridphysics.mazes import polarmaze_game
    from pybrain.optimization import SNES
    g = VGDLParser().parseGame(polarmaze_game)
    g.buildLevel(labyrinth2)
    game_env = GameEnvironment(g)
    net = buildNet(game_env.outdim, 6, 4, temperature=0.1, recurrent=False)
    
    algo = SNES(lambda x: someEpisodes(game_env, x, avgOver=3, maxSteps=50), net, verbose=True, desiredEvaluation=0.75)
    rows, cols = 2,2
    episodesPerStep = 5
    for i in range(rows*cols):
        pylab.subplot(rows, cols, i+1)
        algo.learn(episodesPerStep)
        if isinstance(algo.bestEvaluable, ndarray):
            net._setParameters(algo.bestEvaluable)
        else:
            net = algo.bestEvaluable
        plotBackground(game_env)    
        plotTrajectories(game_env, net)
        pylab.title(str((i+1)*episodesPerStep))
        if algo.desiredEvaluation <= algo.bestEvaluation:
            break
        print
    pylab.show()


    
if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    #test4()
    test5()
    
    