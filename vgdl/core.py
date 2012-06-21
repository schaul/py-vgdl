'''
Video game description language -- parser, framework and core game classes.

@author: Tom Schaul
'''

import pygame
from random import choice
from tools import Node, indentTreeParser


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
            
            if len(sn.children) == 0:
                if self.verbose:
                    print "Defining:", key, sclass, args, stypes 
                self.game.sprite_constr[key] = (sclass, args, stypes)
                self.game.sprite_groups[key] = []
                self.game.sprite_order.append(key)
            else:
                #self.game.sprite_abstractgroups[key] = []                
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
    MAX_SPRITES = 1000
    
    def __init__(self, block_size=10, frame_rate=20):
        self.block_size = block_size
        self.frame_rate = frame_rate
        # contains mappings to constructor
        self.sprite_constr = {}
        # z-level of sprite types (in case of overlap)  
        self.sprite_order  = [] 
        # contains instance lists
        self.sprite_groups = {}
        # collision effects
        self.collision_eff = []
        # for reading levels
        self.char_mapping = {}
        # termination criteria
        self.terminations = [Termination()]
        self.num_sprites = 0
    
    def buildLevel(self, lstr):
        lines = [l for l in lstr.split("\n") if len(l)>0]
        lengths = map(len, lines)
        assert min(lengths)==max(lengths), "Inconsistent line lengths."
        width = lengths[0]
        height = len(lines)
        assert width > 1 and height > 1, "Level too small."
        
        # rescale pixels per block to adapt to the level        
        self.block_size = max(1,int(500/max(width, height)))*2
        self._initScreen((width*self.block_size, height*self.block_size))
        
        # create sprites
        for row, l in enumerate(lines):
            for col, c in enumerate(l):
                if c in self.char_mapping:
                    pos = (col*self.block_size, row*self.block_size)
                    self._createSprite(self.char_mapping[c], pos)
                
    def _createSprite(self, keys, pos):
        for key in keys:
            if self.num_sprites > self.MAX_SPRITES:
                print "Sprite limit reached."
                return
            sclass, args, stypes = self.sprite_constr[key] 
            if 'singleton' in args and args['singleton']==True:
                if len(self.sprite_groups[key]) > 0:                    
                    continue
                else:
                    args = args.copy()
                    del args['singleton']
            
            s = sclass(pos=pos, size=(self.block_size, self.block_size), **args)
            s.stypes = stypes
            s.name = key
            self.sprite_groups[key].append(s)
            self.num_sprites += 1
            
    def _initScreen(self, size):
        pygame.init()    
        self.screensize = size
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.Surface(size)
        self.screen.blit(self.background, (0,0))
        
    def __iter__(self):
        """ Iterator over all sprites """
        for key in self.sprite_order:
            for s in self.sprite_groups[key]:
                yield s
                
    def numSprites(self, key):
        """ Abstract sprite groups are computed on demand only """
        if key in self.sprite_groups:
            return len(self.sprite_groups[key])
        else: 
            return len([s for s in self if key in s.stypes])
        
    def _clearAll(self):
        for s in set(self.kill_list):
            s._clear(self.screen, self.background, double=True)
            self.sprite_groups[s.name].remove(s)
        for s in self:
            s._clear(self.screen, self.background)
        self.kill_list = []            
    
    def _drawAll(self):
        for s in self:
            s._draw(self.screen)
            
    def _updateCollisionDict(self):
        # create a dictionary that maps type pairs to a list of sprite pairs
        self.lastcollisions = {}
        nonstatics = [s for s in self if not s.is_static]
        statics = [s for s in self if s.is_static]
        for i, s1 in enumerate(nonstatics):
            for s2 in (nonstatics+statics)[i+1:]:
                assert s1 != s2
                if s1.rect.colliderect(s2.rect):
                    for key1 in s1.stypes:
                        for key2 in s2.stypes:
                            if (key1, key2) not in self.lastcollisions:
                                self.lastcollisions[(key1, key2)] = []
                                self.lastcollisions[(key2, key1)] = []
                            self.lastcollisions[(key1, key2)].append((s1, s2))
                            self.lastcollisions[(key2, key1)].append((s2, s1))
            # detect end-of-screen
            if not pygame.Rect((0,0), self.screensize).contains(s1.rect):
                for key1 in s1.stypes:
                    if (key1, 'EOS') not in self.lastcollisions:
                        self.lastcollisions[(key1, 'EOS')] = []
                    self.lastcollisions[(key1, 'EOS')].append((s1, None))
                                    
    def startGame(self):
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
            for g1, g2, effect, args in self.collision_eff:
                if (g1, g2) in self.lastcollisions:
                    for s1, s2 in set(self.lastcollisions[(g1, g2)]):
                        effect(s1, s2, self, **args)
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
    color    = None
    speedup  = 1
    cooldown = 0 # pause ticks in-between two moves 
    
    def __init__(self, pos, size=(10,10), color=None, speedup=None, cooldown=None, physicstype=None):
        self.rect = pygame.Rect(pos, size)
        self.lastrect = self.rect
        if not physicstype:
            from ontology import GridPhysics
            physicstype = GridPhysics
        self.physics = physicstype(size)
        if speedup is not None:
            self.speedup = speedup
        if cooldown is not None:
            self.cooldown = cooldown
        if color:
            self.color = color
        elif self.color is None:
            self.color = (choice(self.COLOR_DISC), choice(self.COLOR_DISC), choice(self.COLOR_DISC))
        self.lastmove = 0        
        
    def update(self, game):
        """ The main place where subclasses differ. """
        self.lastmove += 1
        self.lastrect = self.rect        
    
    def _updatePos(self, direction, speedup=None):
        if not speedup:
            speedup = self.speedup
        self.lastrect = self.rect
        if self.cooldown > self.lastmove:
            self.lastmove += 1
        elif abs(direction[0])+abs(direction[1])==0:
            # no need to redraw if nothing was updated
            self.lastmove += 1
        else:
            self.rect = self.rect.move((direction[0]*speedup, direction[1]*speedup))
            self.lastmove = 0       
    
    @property
    def lastdirection(self):
        return (self.rect[0]-self.lastrect[0], self.rect[1]-self.lastrect[1])     
    
    def _draw(self, screen):
        r = screen.fill(self.color, self.rect)
        VGDLSprite.dirtyrects.append(r)
        
    def _clear(self, screen, background, double=False):
        r = screen.blit(background, self.rect, self.rect)
        VGDLSprite.dirtyrects.append(r)
        if double:    
            r = screen.blit(background, self.lastrect, self.lastrect)
            VGDLSprite.dirtyrects.append(r)    


class Termination(object):
    """ Base class for all termination criteria. """
    def isDone(self, game):
        """ returns whether the game is over, with a win/lose flag """
        from pygame.locals import K_ESCAPE, QUIT        
        if game.keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            return True, False    
        else:
            return False, None