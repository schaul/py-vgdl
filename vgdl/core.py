'''
Video game description language -- parser, framework and core game classes.

@author: Tom Schaul
'''

import pygame
from random import choice
from tools import Node, indentTreeParser
from collections import defaultdict
from vgdl.tools import roundedPoints
 

class VGDLParser(object):
    """ Parses a string into a Game object. """    
    verbose = False
    
    @staticmethod     
    def playGame(game_str, map_str):
        """ Parses the game and level map strings, and starts the game. """
        g = VGDLParser().parseGame(game_str)
        g.buildLevel(map_str)
        g.startGame()
               
    def parseGame(self, tree):
        """ Accepts either a string, or a tree. """        
        if not isinstance(tree, Node):
            tree = indentTreeParser(tree).children[0]
        sclass, args = self._parseArgs(tree.content)            
        self.game = sclass(**args)        
        for c in tree.children:
            if c.content == "SpriteSet":
                self.parseSprites(c.children)
            if c.content == "InteractionSet":
                self.parseInteractions(c.children)
            if c.content == "LevelMapping":
                self.parseMappings(c.children)
            if c.content == "TerminationSet":
                self.parseTerminations(c.children)
        return self.game
    
    def _eval(self, estr):
        """ Whatever is visible in the global namespace (after importing the ontologies)
        can be used in the VGDL, and is evaluated.   
        """
        from ontology import * #@UnusedWildImport
        return eval(estr)

    def parseInteractions(self, inodes):        
        for inode in inodes:
            if ">" in inode.content:
                pair, edef = [x.strip() for x in inode.content.split(">")]
                eclass, args = self._parseArgs(edef)
                self.game.collision_eff.append(tuple([x.strip() for x in pair.split(" ") if len(x)>0]
                                                     +[eclass, args]))
                if self.verbose:            
                    print "Collision", pair, "has effect:", edef              
                
    def parseTerminations(self, tnodes):
        for tn in tnodes:
            sclass, args = self._parseArgs(tn.content)
            if self.verbose:
                print "Adding:", sclass, args             
            self.game.terminations.append(sclass(**args))
                
    def parseSprites(self, snodes, parentclass=None, parentargs={}, parenttypes=[]):
        for sn in snodes:
            assert ">" in sn.content
            key, sdef = [x.strip() for x in sn.content.split(">")]
            sclass, args = self._parseArgs(sdef, parentclass, parentargs.copy())
            stypes = parenttypes+[key]
            if 'singleton' in args:
                if args['singleton']==True:
                    self.game.singletons.append(key)
                args = args.copy()
                del args['singleton']
            
            if len(sn.children) == 0:
                if self.verbose:
                    print "Defining:", key, sclass, args, stypes 
                self.game.sprite_constr[key] = (sclass, args, stypes)
                if key in self.game.sprite_order:
                    # last one counts
                    self.game.sprite_order.remove(key)
                self.game.sprite_order.append(key)
            else:              
                self.parseSprites(sn.children, sclass, args, stypes)
       
    def parseMappings(self, mnodes):        
        for mn in mnodes:
            c, val = [x.strip() for x in mn.content.split(">")]
            assert len(c) == 1, "Only single character mappings allowed."
            # a char can map to multiple sprites
            keys = [x.strip() for x in val.split(" ") if len(x)>0]
            if self.verbose:            
                print "Mapping", c, keys 
            self.game.char_mapping[c] = keys
    
    def _parseArgs(self, s,  sclass=None, args=None):
        if not args: 
            args = {}
        sparts = [x.strip() for x in s.split(" ") if len(x) > 0]
        if len(sparts) == 0:
            return sclass, args
        if not '=' in sparts[0]:
            sclass = self._eval(sparts[0])
            sparts = sparts[1:]
        for sp in sparts:
            k, val = sp.split("=")
            try:
                args[k] = self._eval(val)
            except:
                args[k] = val
        return sclass, args
                
            
class BasicGame(object):
    """ This regroups all the components of a game's dynamics, after parsing. """    
    MAX_SPRITES = 10000
    
    default_mapping = {'w': ['wall'],
                       'A': ['avatar'],
                       }
    
    def __init__(self, block_size=10, frame_rate=20):
        from ontology import Immovable, DARKGRAY, MovingAvatar
        self.block_size = block_size
        self.frame_rate = frame_rate
        # contains mappings to constructor (just a few defaults are known)
        self.sprite_constr = {'wall': (Immovable, {'color': DARKGRAY}, ['wall']),
                              'avatar': (MovingAvatar, {}, ['avatar']),
                              }
        # z-level of sprite types (in case of overlap)  
        self.sprite_order  = ['wall', 
                              'avatar',
                              ] 
        # contains instance lists
        self.sprite_groups = defaultdict(list)
        # which sprite types (abstract or not) are singletons?
        self.singletons = []
        # collision effects (ordered by execution order)
        self.collision_eff = []
        # for reading levels
        self.char_mapping = {}
        # termination criteria
        self.terminations = [Termination()]
        self.num_sprites = 0
        self.kill_list=[]        
        self.is_stochastic = False
    
    def buildLevel(self, lstr):        
        from ontology import stochastic_effects
        lines = [l for l in lstr.split("\n") if len(l)>0]
        lengths = map(len, lines)
        assert min(lengths)==max(lengths), "Inconsistent line lengths."
        self.width = lengths[0]
        self.height = len(lines)
        assert self.width > 1 and self.height > 1, "Level too small."
        # rescale pixels per block to adapt to the level        
        self.block_size = max(2,int(800./max(self.width, self.height)))
        self.screensize = (self.width*self.block_size, self.height*self.block_size)
        
        # create sprites
        for row, l in enumerate(lines):
            for col, c in enumerate(l):
                if c in self.char_mapping:
                    pos = (col*self.block_size, row*self.block_size)
                    self._createSprite(self.char_mapping[c], pos)
                elif c in self.default_mapping:
                    pos = (col*self.block_size, row*self.block_size)
                    self._createSprite(self.default_mapping[c], pos)
        self.kill_list=[]
        for _, _, effect, _ in self.collision_eff:
            if effect in stochastic_effects:
                self.is_stochastic = True
                        
        # guarantee that avatar is always visible        
        self.sprite_order.remove('avatar')
        self.sprite_order.append('avatar')        
                        
    def _createSprite(self, keys, pos):
        res = []
        for key in keys:
            if self.num_sprites > self.MAX_SPRITES:
                print "Sprite limit reached."
                return
            sclass, args, stypes = self.sprite_constr[key] 
            # verify the singleton condition
            anyother = False
            for pk in stypes[::-1]:
                if pk in self.singletons:
                    if self.numSprites(pk) > 0:
                        anyother = True
                        break
            if anyother:
                continue
            s = sclass(pos=pos, size=(self.block_size, self.block_size), **args)
            s.stypes = stypes
            s.name = key
            self.sprite_groups[key].append(s)
            self.num_sprites += 1
            if s.is_stochastic:
                self.is_stochastic = True
            res.append(s)
        return res
            
    def _initScreen(self, size):
        from ontology import LIGHTGRAY
        pygame.init()    
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.Surface(size)
        self.background.fill(LIGHTGRAY)
        self.screen.blit(self.background, (0,0))        
        
    def __iter__(self):
        """ Iterator over all sprites """
        for key in self.sprite_order:
            if key not in self.sprite_groups:
                # abstract type
                continue
            for s in self.sprite_groups[key]:
                yield s
                
    def numSprites(self, key):
        """ Abstract sprite groups are computed on demand only """
        deleted = len([s for s in self.kill_list if key in s.stypes])
        if key in self.sprite_groups:
            return len(self.sprite_groups[key])-deleted
        else: 
            return len([s for s in self if key in s.stypes])-deleted
        
    def getSprites(self, key):
        if key in self.sprite_groups:
            return [s for s in self.sprite_groups[key] if s not in self.kill_list]
        else:
            return [s for s in self if key in s.stypes and s not in self.kill_list]
        
    def getAvatars(self):
        """ The currently alive avatar(s) """
        return [s for s in self if isinstance(s, Avatar) and s not in self.kill_list]
        
    def _clearAll(self, onscreen=True):
        for s in set(self.kill_list):
            if onscreen:
                s._clear(self.screen, self.background, double=True)
            self.sprite_groups[s.name].remove(s)
        if onscreen:
            for s in self:
                s._clear(self.screen, self.background)
        self.kill_list = []            
    
    def _drawAll(self):
        for s in self:
            s._draw(self.screen)
            
    def _updateCollisionDict(self):
        # create a dictionary that maps type pairs to a list of sprite pairs
        self.lastcollisions = defaultdict(list)
        nonstatics = [s for s in self if not s.is_static]
        statics = [s for s in self if s.is_static]
        for i, s1 in enumerate(nonstatics):
            for s2 in (nonstatics+statics)[i+1:]:
                assert s1 != s2
                if s1.rect.colliderect(s2.rect):
                    for key1 in s1.stypes:
                        for key2 in s2.stypes:
                            self.lastcollisions[(key1, key2)].append((s1, s2))
                            self.lastcollisions[(key2, key1)].append((s2, s1))
            # detect end-of-screen
            if not pygame.Rect((0,0), self.screensize).contains(s1.rect):
                for key1 in s1.stypes:
                    self.lastcollisions[(key1, 'EOS')].append((s1, None))
                    
    def _eventHandling(self):
        for g1, g2, effect, args in self.collision_eff:
            for s1, s2 in set(self.lastcollisions[(g1, g2)]):
                # TODO: this is not a bullet-proof way, but seems to work
                if s1 not in self.kill_list:
                    effect(s1, s2, self, **args)
                                            
    def startGame(self):        
        self._initScreen(self.screensize)
        clock = pygame.time.Clock()
        self.time = 0
        self.kill_list=[]
        pygame.display.flip()
        ended = False
        win = False
        while not ended:
            clock.tick(self.frame_rate) 
            self.time += 1
            self._clearAll()            
            # gather events
            pygame.event.pump()
            self.keystate = pygame.key.get_pressed()            
            # termination criteria
            for t in self.terminations:
                ended, win = t.isDone(self)
                if ended:
                    break            
            # update sprites 
            for s in self:
                s.update(self)                
            # handle collision effects
            self._updateCollisionDict()
            self._eventHandling()
            self._drawAll()                            
            pygame.display.update(VGDLSprite.dirtyrects)
            VGDLSprite.dirtyrects = []
            
        if win:
            print "Dude, you're a born winner!"
        else:
            print "Dang. Try again..."            
        pygame.time.wait(50)    
    

class VGDLSprite(object):
    """ Base class for all sprite types. """
    
    COLOR_DISC = [20,80,140,200]
    dirtyrects = []
    
    is_static= False
    is_avatar= False
    is_stochastic = False
    color    = None
    cooldown = 0 # pause ticks in-between two moves 
    speed    = None   
    mass     = 1
    physicstype=None
    shrinkfactor=0
    
    def __init__(self, pos, size=(10,10), color=None, speed=None, cooldown=None, physicstype=None, **kwargs):
        self.rect = pygame.Rect(pos, size)
        self.lastrect = self.rect
        if physicstype is not None:
            self.physicstype = physicstype            
        elif self.physicstype is None:
            from ontology import GridPhysics
            self.physicstype = GridPhysics
        self.physics = self.physicstype(size)
        if speed is not None:
            self.speed = speed
        if cooldown is not None:
            self.cooldown = cooldown
        if color:
            self.color = color
        elif self.color is None:
            self.color = (choice(self.COLOR_DISC), choice(self.COLOR_DISC), choice(self.COLOR_DISC))
        for name, value in kwargs.items():
            if hasattr(self, name):
                self.__dict__[name] = value
            else:
                print "WARNING: undefined parameter '%s' for sprite '%s'! "%(name, self.__class__.__name__)
        # how many timesteps ago was the last move?
        self.lastmove = 0        
        
    def update(self, game):
        """ The main place where subclasses differ. """
        self.lastrect = self.rect
        # no need to redraw if nothing was updated
        self.lastmove += 1
        if not self.is_static:
            self.physics.passiveMovement(self)
        
    def _updatePos(self, orientation, speed=None):
        if speed is None:
            speed = self.speed
        if not(self.cooldown > self.lastmove or abs(orientation[0])+abs(orientation[1])==0):
            self.rect = self.rect.move((orientation[0]*speed, orientation[1]*speed))
            self.lastmove = 0
            
    def _velocity(self):
        """ Current velocity vector. """
        if self.speed is None or self.speed==0 or not hasattr(self, 'orientation'):
            return (0,0)
        else:
            return (self.orientation[0]*self.speed, self.orientation[1]*self.speed)
    
    @property
    def lastdirection(self):
        return (self.rect[0]-self.lastrect[0], self.rect[1]-self.lastrect[1])     
    
    def _draw(self, screen):
        from ontology import LIGHTGREEN
        if self.shrinkfactor != 0:
            shrunk = self.rect.inflate(-self.rect.width*self.shrinkfactor, 
                                       -self.rect.height*self.shrinkfactor)
        else:
            shrunk = self.rect
            
        if self.is_avatar:
            rounded = roundedPoints(shrunk)
            pygame.draw.polygon(screen, self.color, rounded)
            pygame.draw.lines(screen, LIGHTGREEN, True, rounded, 2)
            r = self.rect.copy()
        elif not self.is_static:
            rounded = roundedPoints(shrunk)
            pygame.draw.polygon(screen, self.color, rounded)
            r = self.rect.copy()
        else:
            r = screen.fill(self.color, shrunk)
        VGDLSprite.dirtyrects.append(r)
        
    def _clear(self, screen, background, double=False):
        r = screen.blit(background, self.rect, self.rect)
        VGDLSprite.dirtyrects.append(r)
        if double:    
            r = screen.blit(background, self.lastrect, self.lastrect)
            VGDLSprite.dirtyrects.append(r)    

    def __repr__(self):
        return self.name+" at (%s,%s)"%(self.rect.left, self.rect.top)


class Avatar(object):
    """ Abstract superclass of all avatars. """
    shrinkfactor=0.15
   
class Termination(object):
    """ Base class for all termination criteria. """
    def isDone(self, game):
        """ returns whether the game is over, with a win/lose flag """
        from pygame.locals import K_ESCAPE, QUIT        
        if game.keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            return True, False    
        else:
            return False, None