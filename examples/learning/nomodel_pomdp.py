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
from scipy import mean
from vgdl.core import VGDLParser

# TODO: wrap one episode into 


def oneEpisode(game_env, network, discountFactor=0.9, maxSteps=100):
    """ Return the fitness value for one episode of play, given the policy defined by a neural network. """
    task = GameTask(game_env)
    task.maxSteps=maxSteps
    agent = LearningAgent(network)
    exper = EpisodicExperiment(task, agent)
    rs = exper.doEpisodes(1)
    #print len(rs[0]),
    return mean([sum([v*discountFactor**step for step, v in enumerate(r)]) for r in rs])

    
def buildNet(indim, hidden):
    from pybrain import FullConnection, BiasUnit, TanhLayer, SoftmaxLayer, RecurrentNetwork, LinearLayer
    net = RecurrentNetwork()
    net.addInputModule(LinearLayer(indim, name = 'i'))
    net.addModule(TanhLayer(hidden, name = 'h'))
    net.addModule(BiasUnit('bias'))
    net.addOutputModule(SoftmaxLayer(2, name = 'o'))
    net.addConnection(FullConnection(net['i'], net['h']))
    net.addConnection(FullConnection(net['bias'], net['h']))
    net.addConnection(FullConnection(net['bias'], net['o']))
    net.addConnection(FullConnection(net['h'], net['o']))
    net.addRecurrentConnection(FullConnection(net['o'], net['h']))
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
    
    net = buildNet(game_env.outdim, 2)
    for i in range(200):
        net.randomize()
        net.reset()
        print oneEpisode(game_env, net),
        if i% 20 == 19:
            print


def trainOnGame(game_env, maxEpisodes=500):
    from pybrain.optimization import SNES
    print 'number of observations:', game_env.outdim
    
    net = buildNet(game_env.outdim, 6)
    
    print 'Starting training'
    algo = SNES(lambda x: oneEpisode(game_env, x), net, verbose=True, desiredEvaluation=0.43)
    algo.learn(maxEpisodes)
    net._setParameters(algo.bestEvaluable)
    return net
    
    
def test2():
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1    
    
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    game_env = GameEnvironment(g, actionDelay=100)
    
    net = trainOnGame(game_env) 
    print net
    print 'Done. Demonstrating the final controller'
    
    game_env.visualize = True
    game_env.reset()
    task = GameTask(game_env)
    agent = LearningAgent(net)
    exper = EpisodicExperiment(task, agent)
    exper.doEpisodes(1)
    
if __name__ == '__main__':
    #test1()
    test2()