'''
Created on 2013 3 13

@author: Tom Schaul (schaul@gmail.com)

Managing states and observations, for different types of games
'''

import pygame
from pybrain.utilities import setAllArgs

from ontology import RotatingAvatar, BASEDIRS, GridPhysics, LinkAvatar, kill_effects
from core import Avatar
from tools import listRotate



class StateObsHandler(object):
    """ Managing different types of state representations,
    and of observations. 
    
    A state is always composed of a tuple, with the avatar position (x,y) in the first places.
    If the avatar orientation matters, the orientation is the third element of the tuple. 
    """
    
    # is the avatar having an orientation or not?
    orientedAvatar = False
    
    # is the avatar a single persistent sprite, or can it be transformed?
    uniqueAvatar = True
    
    # can the avatar die?
    mortalAvatar = False
    
    # can other sprites die?
    mortalOther = False
    
    # can other sprites move
    staticOther = True
    
    def __init__(self, game, **kwargs):
        setAllArgs(self, kwargs)
        self._game = game
        self._avatar_types = []
        self._abs_avatar_types = []
        self._other_types = []
        self._mortal_types = []
        for skey in sorted(game.sprite_constr): 
            sclass, _, stypes = game.sprite_constr[skey]
            if issubclass(sclass, Avatar):
                self._abs_avatar_types += stypes[:-1]
                self._avatar_types += [stypes[-1]]
                if issubclass(sclass, RotatingAvatar) or issubclass(sclass, LinkAvatar):
                    self.orientedAvatar = True
            if skey not in game.sprite_groups:
                continue 
            ss = game.sprite_groups[skey]
            if len(ss) == 0:
                continue
            if isinstance(ss[0], Avatar):
                assert issubclass(ss[0].physicstype, GridPhysics), \
                        'Not supported: Game must have grid physics, has %s'\
                        % (self._avatar.physicstype.__name__)                       
            else:
                self._other_types += [skey]
                if not ss[0].is_static:
                    self.staticOther = False
        assert self.staticOther, "not yet supported: all non-avatar sprites must be static. "
        
        self._avatar_types = sorted(set(self._avatar_types).difference(self._abs_avatar_types))
        self.uniqueAvatar = (len(self._avatar_types) == 1)
        #assert self.uniqueAvatar, 'not yet supported: can only have one avatar class'
        
        # determine mortality
        for skey, _, effect, _ in game.collision_eff:
            if effect in kill_effects:
                if skey in self._avatar_types+self._abs_avatar_types:
                    self.mortalAvatar = True
                if skey in self._other_types:
                    self.mortalOther = True
                    self._mortal_types += [skey]
        
                 
        # retain observable features, and their colors
        self._obstypes = {}
        self._obscols = {}
        for skey in self._other_types:
            ss = game.sprite_groups[skey]
            self._obstypes[skey] = [self._sprite2state(sprite, oriented=False) 
                                    for sprite in ss if sprite.is_static]
            self._obscols[skey] = ss[0].color            
        
        if self.mortalOther:
            self._gravepoints = {}
            for skey in self._mortal_types:
                for s in self._game.sprite_groups[skey]:
                    self._gravepoints[(skey, self._rect2pos(s.rect))] = True
         
    @property
    def _avatar(self):
        ss = self._game.getAvatars()
        assert len(ss) <= 1, 'Not supported: Only a single avatar can be used, found %s' % ss
        if len(ss) == 0:
            return None
        return ss[0]
    
    def setState(self, state):
        # no avatar?
        if self._avatar is None:
            pos = (state[0]*self._game.block_size, state[1]*self._game.block_size)
            if self.uniqueAvatar:
                atype = self._avatar_types[0]
            else:
                atype = state[-1]
            self._game._createSprite([atype], pos)
        
        # bad avatar?
        if not self.uniqueAvatar:
            atype = state[-1]
            if self._avatar.name != atype:
                self._game.kill_list.append(self._avatar)
                pos = (state[0]*self._game.block_size, state[1]*self._game.block_size)
                self._game._createSprite([atype], pos)            
            
        if not self.uniqueAvatar:
            state = state[:-1]
        if self.mortalOther:
            self._setPresences(state[-1])
            state = state[:-1]  
        self._setSpriteState(self._avatar, state)
        self._avatar.lastrect = self._avatar.rect
        self._avatar.lastmove = 0               
        
    def getState(self):        
        if self._avatar is None:
            return (-1,-1, 'dead')
        if self.mortalOther:
            if self.uniqueAvatar:
                return tuple(list(self._sprite2state(self._avatar)) + [self._getPresences()])
            else:
                return tuple(list(self._sprite2state(self._avatar)) 
                             + [self._getPresences()] + [self._avatar.name])
        else:
            if self.uniqueAvatar:
                return self._sprite2state(self._avatar)
            else:
                return tuple(list(self._sprite2state(self._avatar)) 
                             + [self._avatar.name])
                
    def _getPresences(self):
        """ Binary vector of which non-avatar sprites are present. """
        res = []
        for skey, pos in sorted(self._gravepoints):
            if pos in [self._rect2pos(s.rect) for s in self._game.sprite_groups[skey]
                       if s not in self._game.kill_list]:
                res.append(1)
            else:
                res.append(0)
        return tuple(res)
    
    def _setPresences(self, p):
        for i, (skey, pos) in enumerate(sorted(self._gravepoints)):
            target = p[i] != 0 
            matches = [s for s in self._game.sprite_groups[skey] if self._rect2pos(s.rect)==pos]
            current = (not len(matches) == 0 and matches[0] not in self._game.kill_list)
            if current == target:
                continue
            elif current:
                #print 'die', skey, pos, matches
                self._game.kill_list.append(matches[0])
            elif target:
                #print 'live', skey, pos, matches
                pos = (pos[0]*self._game.block_size, pos[1]*self._game.block_size)
                self._game._createSprite([skey], pos)
                    
    def _rawSensor(self, state):
        return [(state in ostates) for _, ostates in sorted(self._obstypes.items())[::-1]]
    
    def _sprite2state(self, s, oriented=None):
        pos = self._rect2pos(s.rect)
        if oriented is None and self.orientedAvatar:
            return (pos[0], pos[1], s.orientation)
        else:
            return pos
        
    def _rect2pos(self, r):
        return (r.left / self._game.block_size, r.top / self._game.block_size)
    
    def _setRectPos(self, s, pos):
        s.rect = pygame.Rect((pos[0] * self._game.block_size,
                              pos[1] * self._game.block_size),
                             (self._game.block_size, self._game.block_size))
        
    def _setSpriteState(self, s, state):
        if self.orientedAvatar:
            s.orientation = state[2]
        self._setRectPos(s, (state[0], state[1]))
        
    def _stateNeighbors(self, state):
        """ Can be different in subclasses... 
        
        By default: current position and four neighbors. """
        pos = (state[0], state[1])
        ns = [(a[0] + pos[0], a[1] + pos[1]) for a in BASEDIRS]
        if self.orientedAvatar:
            # subjective perspective, so we rotate the view according to the current orientation
            ns = listRotate(ns, BASEDIRS.index(state[2]))
            return ns
        else:
            return ns
        
    