'''
Created on Oct 8, 2013

@author: tom.schaul
'''


def testInteractions():
    from vgdl.core import VGDLParser
    from examples.gridphysics.aliens import aliens_level, aliens_game
    from pygame.locals import K_SPACE
    # from examples.gridphysics.sokoban import so
    from pybrain.rl.agents.agent import Agent
    
    class DummyAgent(Agent):
        total = 4
        def getAction(self):
            # res = randint(0, self.total - 1)
            return 1
        
    map_str, game_str = aliens_level, aliens_game
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    g._initScreen(g.screensize,headless=True)
        
    for _ in range(300):
        win, _ = g.tick(K_SPACE)
        if win is not None:
            break
        
     
def testLoadSave():
    from vgdl.core import VGDLParser
    from examples.gridphysics.aliens import aliens_level, aliens_game
        
    map_str, game_str = aliens_level, aliens_game
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)
    
    for _ in range(1000):
        s = g.getFullState()
        g.setFullState(s)
    
if __name__ == "__main__":
    from pybrain.tests.helpers import sortedProfiling
    sortedProfiling('testInteractions()')
    # sortedProfiling('testLoadSave()')
