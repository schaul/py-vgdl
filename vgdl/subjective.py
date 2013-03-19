'''
Created on 2013 2 19

@author: Tom Schaul (schaul@gmail.com)

Playing a game in subjective perspective mode.

Optional: small cheat screen gives the global view.
'''

import pygame

from ontology import DARKGRAY, BASEDIRS, LIGHTGRAY, RED, LIGHTBLUE
from tools import squarePoints
from interfaces import GameEnvironment

backscale = 0.4
midscale = 0.65
frontscale = 5
# 4 corners 
knownPolygons = {'center-back':squarePoints((0, 0), backscale),
                 'left-back':squarePoints((-backscale, 0), backscale),
                 'right-back':squarePoints((backscale, 0), backscale),
                 'center-mid':squarePoints((0, 0), midscale),
                 'left-mid':squarePoints((-midscale, 0), midscale),
                 'right-mid':squarePoints((midscale, 0), midscale),
                 'left-tomid-close':[(-0.5 * frontscale, 0.5 * frontscale),
                                     (-0.5 * midscale, 0.5 * midscale),
                                     (-0.5 * midscale, -0.5 * midscale),
                                     (-0.5 * frontscale, -0.5 * frontscale)],
                 'left-tomid-far':[(-1.5 * frontscale, 0.5 * frontscale),
                                   (-1.5 * midscale, 0.5 * midscale),
                                   (-1.5 * midscale, -0.5 * midscale),
                                   (-1.5 * frontscale, -0.5 * frontscale)],
                 'right-tomid-close':[(0.5 * frontscale, 0.5 * frontscale),
                                     (0.5 * midscale, 0.5 * midscale),
                                     (0.5 * midscale, -0.5 * midscale),
                                     (0.5 * frontscale, -0.5 * frontscale)],
                 'right-tomid-far':[(1.5 * frontscale, 0.5 * frontscale),
                                   (1.5 * midscale, 0.5 * midscale),
                                   (1.5 * midscale, -0.5 * midscale),
                                   (1.5 * frontscale, -0.5 * frontscale)],
                 'left-toback-close':[(-0.5 * backscale, 0.5 * backscale),
                                     (-0.5 * midscale, 0.5 * midscale),
                                     (-0.5 * midscale, -0.5 * midscale),
                                     (-0.5 * backscale, -0.5 * backscale)],
                 'left-toback-far':[(-1.5 * backscale, 0.5 * backscale),
                                   (-1.5 * midscale, 0.5 * midscale),
                                   (-1.5 * midscale, -0.5 * midscale),
                                   (-1.5 * backscale, -0.5 * backscale)],
                 'right-toback-close':[(0.5 * backscale, 0.5 * backscale),
                                     (0.5 * midscale, 0.5 * midscale),
                                     (0.5 * midscale, -0.5 * midscale),
                                     (0.5 * backscale, -0.5 * backscale)],
                 'right-toback-far':[(1.5 * backscale, 0.5 * backscale),
                                   (1.5 * midscale, 0.5 * midscale),
                                   (1.5 * midscale, -0.5 * midscale),
                                   (1.5 * backscale, -0.5 * backscale)],
                 'center-mid-floor':[(0.5 * backscale, 0.5 * backscale),
                                   (0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * backscale, 0.5 * backscale)],
                 'right-mid-floor':[(1.5 * backscale, 0.5 * backscale),
                                   (1.5 * midscale, 0.5 * midscale),
                                   (0.5 * midscale, 0.5 * midscale),
                                   (0.5 * backscale, 0.5 * backscale)],
                 'left-mid-floor':[(-1.5 * backscale, 0.5 * backscale),
                                   (-1.5 * midscale, 0.5 * midscale),
                                   (-0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * backscale, 0.5 * backscale)],
                 'right-front-floor':[(1.5 * frontscale, 0.5 * frontscale),
                                   (1.5 * midscale, 0.5 * midscale),
                                   (0.5 * midscale, 0.5 * midscale),
                                   (0.5 * frontscale, 0.5 * frontscale)],
                 'left-front-floor':[(-1.5 * frontscale, 0.5 * frontscale),
                                   (-1.5 * midscale, 0.5 * midscale),
                                   (-0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * frontscale, 0.5 * frontscale)],
                 'center-front-floor':[(0.5 * frontscale, 0.5 * frontscale),
                                   (0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * midscale, 0.5 * midscale),
                                   (-0.5 * frontscale, 0.5 * frontscale)],
                 }


wallLocations = {1: knownPolygons['left-tomid-far'],
                 2: knownPolygons['left-toback-far'],
                 3: knownPolygons['left-back'],
                 4: knownPolygons['center-back'],
                 5: knownPolygons['right-back'],
                 6: knownPolygons['right-toback-far'],
                 7: knownPolygons['right-tomid-far'],
                 }

blockLocations = {1: [knownPolygons['left-tomid-close']],
                  2: [knownPolygons['left-mid'], knownPolygons['left-toback-close']],
                  3: [knownPolygons['center-mid']],
                  4: [knownPolygons['right-mid'], knownPolygons['right-toback-close']],
                  5: [knownPolygons['right-tomid-close']],
                 }

floorLocations = {1:knownPolygons['left-front-floor'],
                  2:knownPolygons['left-mid-floor'],
                  3:knownPolygons['center-mid-floor'],
                  4:knownPolygons['right-mid-floor'],
                  5:knownPolygons['right-front-floor'],
                  6:knownPolygons['center-front-floor'],
                  }

class SubjectiveSceen(object):
    """ Viewpoint from the subjective point of view of the
    avatar, while inside the game. """
    
    def __init__(self):
        self.width = 750
        self.height = 350

    def _drawPolygon(self, ps, col):
        scaled = [(p[0] * self.height + self.width / 2,
                   p[1] * self.height + self.height / 2) for p in ps]
        pygame.draw.polygon(self.screen, col, scaled)
        
    def _colorBlock(self, bid, col):
        """ color one of the 5 possible full blocks. """
        for ps in blockLocations[bid]:
            self._drawPolygon(ps, col)
        pygame.display.flip()
                
    def _colorFloor(self, fid, col):
        """ color the floor of one of the five possible block locations. """
        self._drawPolygon(floorLocations[fid], col)
        pygame.display.flip()
        
    def _colorWall(self, wid, col):
        """ color one of the 7 far walls. """
        col = tuple([50+c/3 for c in col])
        self._drawPolygon(wallLocations[wid], col)
        pygame.display.flip()
        
    def _initScreen(self):
        pygame.init()    
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.Surface(size)
        self.background.fill(LIGHTBLUE)
        self.reset()
        
    def reset(self):
        self.screen.blit(self.background, (0,0))        
        for ps in wallLocations.values():
            self._drawPolygon(ps, DARKGRAY) 
        for ps in floorLocations.values():
            self._drawPolygon(ps, LIGHTGRAY) 
        pygame.display.flip()
        
        
blocky = ['wall']
        
class SubjectiveGame(GameEnvironment):
    """ Disabling the default visuals and seeing the world from the
    perspective of a (short-sighted) avatar. """
    
    
    def __init__(self, game, **kwargs):
        GameEnvironment.__init__(self, game, visualize=False, **kwargs)
        self.screen = SubjectiveSceen()
        self.screen._initScreen()
        assert self.orientedAvatar, 'Only oriented/directional avatars are currently supported for the first-person view.'
        self.reset()
        
    def reset(self):
        GameEnvironment.reset(self)
        if hasattr(self, 'screen'):
            self.screen.reset()
            pygame.display.flip()  

    def performAction(self, action):
        GameEnvironment.performAction(self, action)
        if action is not None:
            self._drawState()
            pygame.time.wait(self.actionDelay)
        
    def _nearTileIncrements(self):
        p0, p1, orient = self.getState()[:3]
        o0, o1 = orient
        l0, l1 = BASEDIRS[(BASEDIRS.index(orient) + 1) % len(BASEDIRS)]
        r0, r1 = BASEDIRS[(BASEDIRS.index(orient) - 1) % len(BASEDIRS)]
        
        res = [(True, 1, (p0 + 2 * l0, p1 + 2 * l1)),
               (True, 2, (p0 + o0 + 2 * l0, p1 + o1 + 2 * l1)),
               (True, 3, (p0 + 2 * o0 + l0, p1 + 2 * o1 + l1)),
               (True, 4, (p0 + 2 * o0, p1 + 2 * o1)),
               (True, 5, (p0 + 2 * o0 + r0, p1 + 2 * o1 + r1)),
               (True, 6, (p0 + o0 + 2 * r0, p1 + o1 + 2 * r1)),
               (True, 7, (p0 + 2 * r0, p1 + 2 * r1)),
               (False, 2, (p0 + o0 + l0, p1 + o1 + l1)),
               (False, 4, (p0 + o0 + r0, p1 + o1 + r1)),
               (False, 3, (p0 + o0, p1 + o1)),
               (False, 1, (p0 + l0, p1 + l1)),
               (False, 5, (p0 + r0, p1 + r1)),
               (False, 6, (p0, p1)),
               ]
        return res
        
        
    def _drawState(self):
        self.screen.reset()
        for iswall, fid, pos in self._nearTileIncrements():
            for oname, ps in self._obstypes.items():
                b = (oname in blocky)
                col = self._obscols[oname]
                if pos in ps:
                    if iswall:
                        self.screen._colorWall(fid, col)
                    elif not b:
                        self.screen._colorFloor(fid, col)
                    else:
                        self.screen._colorBlock(fid, col)
        pygame.display.flip()  
        
        

        

def test1():
    from ontology import GREEN, ORANGE, WHITE
    s = SubjectiveSceen()
    s._initScreen()
    s._colorWall(3, RED)
    s._colorWall(4, GREEN)
    s._colorWall(5, ORANGE)
    s._colorWall(6, RED)
    s._colorWall(2, ORANGE)
    s._colorWall(1, WHITE)
    #s._colorWall(8, WHITE)
    pygame.time.wait(2000)
    s._colorFloor(4, RED)
    s._colorFloor(1, GREEN)
    pygame.time.wait(1000)
    s._colorFloor(5, RED)
    s._colorFloor(3, WHITE)
    s._colorFloor(2, GREEN)
    pygame.time.wait(1000)
    s.reset()
    pygame.time.wait(1000)
    s._colorBlock(2, RED)
    pygame.time.wait(1000)
    s._colorBlock(4, WHITE)
    pygame.time.wait(1000)
    s._colorBlock(5, GREEN)
    pygame.time.wait(1000)
    s._colorBlock(3, ORANGE)
    pygame.time.wait(1000)
    s._colorBlock(1, GREEN)
    pygame.time.wait(3000)
    
def test2():
    from examples.gridphysics.mazes import polarmaze_game, maze_level_1
    from core import VGDLParser
    game_str, map_str = polarmaze_game, maze_level_1
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)    
    actions = [1, 0, 0, 3, 0, 2, 0, 2, 0, 0, 0]
    env = GameEnvironment(g, visualize=True, actionDelay=100)
    env.rollOut(actions)
    env.reset()
    senv = SubjectiveGame(g, actionDelay=1500)
    senv.rollOut(actions)
       
def test3():
    from examples.gridphysics.mazes import polarmaze_game
    from examples.gridphysics.mazes.simple import maze_level_1b
    from core import VGDLParser
    from pybrain.rl.experiments.episodic import EpisodicExperiment
    from interfaces import GameTask
    from agents import InteractiveAgent, UserTiredException    
    game_str, map_str = polarmaze_game, maze_level_1b
    g = VGDLParser().parseGame(game_str)
    g.buildLevel(map_str)    
    senv = SubjectiveGame(g, actionDelay=100, recordingEnabled=True)
    #senv = GameEnvironment(g, actionDelay=100, recordingEnabled=True, visualize=True)
    task = GameTask(senv)    
    iagent = InteractiveAgent()
    exper = EpisodicExperiment(task, iagent)
    try:
        exper.doEpisodes(1)
    except UserTiredException:
        pass
    print senv._allEvents
    
    
if  __name__ == "__main__":   
    #test1()
    #test2()
    test3()
