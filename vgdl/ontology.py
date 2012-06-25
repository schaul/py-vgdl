'''
Video game description language -- ontology of concepts.

@author: Tom Schaul
'''

from random import choice, random
from math import sqrt
import pygame
from tools import triPoints, unitVector, vectNorm, oncePerStep

# ---------------------------------------------------------------------
#     Constants
# ---------------------------------------------------------------------
GREEN   = (0,200,0)
BLUE    = (0,0,200)
RED     = (200,0,0)
GRAY    = (90,90,90)
WHITE   = (250,250,250)
BROWN   = (140, 120, 100)
BLACK   = (0, 0, 0)
ORANGE  = (250, 160, 0)

UP     = (0, -1)
DOWN   = (0,  1)
LEFT   = (-1, 0)
RIGHT  = ( 1, 0)

BASEDIRS = [UP, RIGHT, DOWN, LEFT]

# ---------------------------------------------------------------------
#     Types of physics
# ---------------------------------------------------------------------
class GridPhysics():
    """ Define actions and key-mappings for grid-world dynamics. """
    
    def __init__(self, gridsize=(10,10)):
        self.gridsize = gridsize        
                
    def passiveMovement(self, sprite):
        if sprite.speed is None:
            speed=1
        else:
            speed=sprite.speed        
        if speed > 0 and hasattr(sprite, 'orientation'):
            sprite._updatePos(sprite.orientation, speed*self.gridsize[0])   
    
    def activeMovement(self, sprite, action):
        if sprite.speed is None:
            speed=1
        else:
            speed=sprite.speed
        if speed >0 and action is not None:
            sprite._updatePos(action, speed*self.gridsize[0])
    
class ContinuousPhysics(GridPhysics):
    gravity = 0.
    friction = 0.02
    
    def __init__(self, gridsize=None):
        self.gridsize = (1,1)    
    
    def passiveMovement(self, sprite):
        GridPhysics.passiveMovement(self, sprite) 
        if self.gravity > 0 and sprite.mass >0:
            self.activeMovement(sprite, (0, self.gravity*sprite.mass))        
        sprite.speed *= (1-self.friction)
            
    def activeMovement(self, sprite, action):
        """ Here the assumption is that the controls determine the direction of
        acceleration of the sprite. """
        v1 = action[0]/float(sprite.mass) + sprite.orientation[0]*sprite.speed
        v2 = action[1]/float(sprite.mass) + sprite.orientation[1]*sprite.speed
        sprite.orientation = unitVector((v1, v2))        
        sprite.speed = vectNorm((v1, v2))/vectNorm(sprite.orientation)
        
class GravityPhysics(ContinuousPhysics):
    gravity = 0.5

        
# ---------------------------------------------------------------------
#     Sprite types
# ---------------------------------------------------------------------
from core import VGDLSprite

class Immovable(VGDLSprite):
    """ A gray square that does not budge. """
    color = GRAY
    is_static = True
    
class Passive(VGDLSprite):
    """ A square that may budge. """
    color = RED    
    
class Flicker(VGDLSprite):
    """ A square that persists just a few timesteps. """
    color = RED    
    def __init__(self, limit=1, **kwargs):
        self.limit = limit
        self.age = 0
        VGDLSprite.__init__(self, **kwargs)    
        
    def update(self, game):
        VGDLSprite.update(self, game)
        if self.age > self.limit:
            killSprite(self, None, game)
        self.age += 1
        
class SpriteProducer(VGDLSprite):
    """ Superclass for all sprites that may produce other sprites, of type 'stype'. """    
    def __init__(self, stype=None, **kwargs):
        self.stype = stype
        VGDLSprite.__init__(self, **kwargs)    
    
class Portal(SpriteProducer):
    is_static = True
    color = BLUE

class SpawnPoint(SpriteProducer):
    prob  = None
    delay = None
    total = None
    color = BLACK
    is_static = True
    
    def __init__(self, delay=1, prob=1, total=None, **kwargs):
        SpriteProducer.__init__(self, **kwargs)
        if prob:
            self.prob  = prob
        if delay:
            self.delay = delay
        if total:
            self.total = total        
        self.counter = 0
        
    def update(self, game):
        if (game.time%self.delay == 0 and random() < self.prob):
            game._createSprite([self.stype], (self.rect.left, self.rect.top))
            self.counter += 1
            
        if self.total and self.counter >= self.total:
            killSprite(self, None, game) 

class RandomNPC(VGDLSprite):
    """ Chooses randomly from all available actions each step. """    
    speed=1
    def update(self, game):
        VGDLSprite.update(self, game)
        self.physics.activeMovement(self, choice(BASEDIRS))    
                    
class OrientedSprite(VGDLSprite):
    """ A sprite that maintains the current orientation. """    
    draw_arrow  = False
    orientation = RIGHT    
    def __init__(self, orientation=None, draw_arrow=None, **kwargs):
        VGDLSprite.__init__(self, **kwargs)
        if orientation is not None:   
            self.orientation=orientation
        if draw_arrow is not None:
            self.draw_arrow = draw_arrow        
    
    def _draw(self, screen):
        """ With a triangle that shows the orientation. """
        VGDLSprite._draw(self, screen)
        if self.draw_arrow:
            col = (self.color[0], 255-self.color[1], self.color[2])
            pygame.draw.polygon(screen, col, triPoints(self.rect, unitVector(self.orientation)))
            
class Missile(OrientedSprite):
    """ A sprite that constantly moves in the same direction. """            
    speed = 1 
    
class Walker(Missile):
    """ Keep moving in the current horizontal direction. If stopped, pick one randomly. """
    airsteering=False
    def __init__(self, airsteering=None, **kwargs):
        Missile.__init__(self, **kwargs)
        if airsteering is not None:   
            self.airsteering=airsteering
    
    def update(self, game):
        if self.airsteering or self.lastdirection[0] == 0:
            if self.orientation[0] > 0:
                d = 1
            elif self.orientation[0] < 0:
                d = -1
            else:
                d = choice([-1, 1])
            self.physics.activeMovement(self, (d, 0))    
        Missile.update(self, game)
        
    
class WalkJumper(Walker):
    prob = 0.1
    strength = 10
    def __init__(self, prob=None, strength=None, **kwargs):
        Walker.__init__(self, **kwargs)
        if prob is not None:   
            self.prob=prob
        if strength is not None:
            self.strength = strength        
    
    def update(self, game):
        if self.lastdirection[0] == 0:
            if self.prob < random():
                self.physics.activeMovement(self, (0, -self.strength))    
        Walker.update(self, game)
        
    
class RandomInertial(OrientedSprite, RandomNPC):
    physicstype=ContinuousPhysics    
        
class RandomMissile(Missile):
    def __init__(self, **kwargs):
        Missile.__init__(self, orientation=choice(BASEDIRS),
                         speed = choice([0.1, 0.2, 0.4]), **kwargs)
        
class ErraticMissile(Missile):
    """ A missile that randomly changes direction from time to time.
    (with probability 'prob' per timestep). """
    def __init__(self, prob=0.1, **kwargs):
        Missile.__init__(self, orientation=choice(BASEDIRS), **kwargs)
        self.prob=prob
    
    def update(self, game):
        Missile.update(self, game)
        if random() < self.prob:
            self.orientation = choice(BASEDIRS)

class Bomber(SpawnPoint, Missile):
    color     = ORANGE
    is_static = False
    def update(self, game):
        Missile.update(self, game)
        SpawnPoint.update(self, game)


# ---------------------------------------------------------------------
#     Avatars: player-controlled sprite types
# ---------------------------------------------------------------------
class MovingAvatar(VGDLSprite):
    color=WHITE    
    speed=1    
    def _readAction(self, game):        
        from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
        if   game.keystate[K_RIGHT]: return RIGHT
        elif game.keystate[K_LEFT]:  return LEFT
        elif game.keystate[K_UP]:    return UP
        elif game.keystate[K_DOWN]:  return DOWN
        else:                        return None
        
    def update(self, game):
        VGDLSprite.update(self, game)
        action = self._readAction(game)
        if action:
            self.physics.activeMovement(self, action)
        
class Frog(MovingAvatar):
    """ Has an additional flag that keeps if from drowning if true. """
    drowning_safe = False
    
    def update(self, game):
        MovingAvatar.update(self, game)
        self.drowning_safe = False
        
class FlakAvatar(MovingAvatar, SpriteProducer):
    """ Only horizontal moves. Hitting the space button creates a sprite of the 
    specified type at its location. """
    color=GREEN        
    
    def update(self, game):
        VGDLSprite.update(self, game)        
        action = self._readAction(game)
        if action in [RIGHT, LEFT]:
            self.physics.activeMovement(self, action)
        from pygame.locals import K_SPACE
        if self.stype and game.keystate[K_SPACE]:
            game._createSprite([self.stype], (self.rect.left, self.rect.top))
            
class OrientedAvatar(OrientedSprite, MovingAvatar):
    draw_arrow = True      
    def update(self, game):
        tmp = self.orientation
        self.orientation = (0,0)
        VGDLSprite.update(self, game)
        action = self._readAction(game)
        if action:
            self.physics.activeMovement(self, action)
        d = self.lastdirection
        if sum(map(abs, d)) > 0:  
            # only update if the sprite moved.
            self.orientation = d
        else:
            self.orientation = tmp                    
    
class LinkAvatar(OrientedAvatar, SpriteProducer):
    """ Link can use his sword in front of him. """
    def __init__(self, stype=None, **kwargs):
        self.stype = stype
        OrientedSprite.__init__(self, **kwargs)

    def update(self, game):
        OrientedAvatar.update(self, game)
        from pygame.locals import K_SPACE
        if self.stype and game.keystate[K_SPACE]:
            u = unitVector(self.orientation)
            game._createSprite([self.stype], (self.rect.left+u[0]*self.rect.size[0],
                                              self.rect.top+u[1]*self.rect.size[1]))    
                            
class InertialAvatar(OrientedAvatar):
    speed=1
    physicstype=ContinuousPhysics
    def update(self, game):
        MovingAvatar.update(self, game)
        
class MarioAvatar(InertialAvatar):
    """ Mario can have two states: in contact with the ground, or in parabolic flight. """
    physicstype=GravityPhysics    
    draw_arrow=False
    strength=10
    airsteering=False    
    def __init__(self, strength=None, airsteering=None, **kwargs):
        if airsteering is not None:
            self.airsteering = airsteering
        if strength is not None:
            self.strength = strength
        InertialAvatar.__init__(self, **kwargs)

    def update(self, game):
        action = self._readAction(game)
        if action is None:
            action = (0,0)
        from pygame.locals import K_SPACE
        if game.keystate[K_SPACE] and self.orientation[1]==0:
            action = (action[0]*sqrt(self.strength), -self.strength)
        elif self.orientation[1]==0 or self.airsteering:
            action = (action[0]*sqrt(self.strength), 0)
        else:
            action = (0,0)
        self.physics.activeMovement(self, action)
        VGDLSprite.update(self, game)
    
                        
        
# ---------------------------------------------------------------------
#     Termination criteria
# ---------------------------------------------------------------------
from core import Termination
        
class Timeout(Termination):
    def __init__(self, limit=0):
        self.limit = limit
    
    def isDone(self, game):
        if game.time >= self.limit:
            return True, False
        else:
            return False, None
    
class SpriteCounter(Termination):
    """ Game ends when the number of sprites of type 'stype' hits 'limit' (or below). """
    def __init__(self, limit=0, stype=None, win=True):
        self.limit = limit
        self.stype = stype
        self.win = win
    
    def isDone(self, game):
        if game.numSprites(self.stype) <= self.limit:
            return True, self.win
        else:
            return False, None
        
class MultiSpriteCounter(Termination):
    """ Game ends when the sum of all sprites of types 'stypes' hits 'limit'. """
    def __init__(self, limit=0, win=True, **kwargs):
        self.limit = limit
        self.win = win
        self.stypes = kwargs.values()
        
    def isDone(self, game):
        if sum([game.numSprites(st) for st in self.stypes])== self.limit:
            return True, self.win
        else:
            return False, None
    

# ---------------------------------------------------------------------
#     Effect types (invoked after an event).
# ---------------------------------------------------------------------    
def killSprite(sprite, partner, game):
    """ Kill command """
    game.kill_list.append(sprite)
    
def cloneSprite(sprite, partner, game):
    game._createSprite([sprite.name], (sprite.rect.left, sprite.rect.top))
    
def transformTo(sprite, partner, game, stype=None):
    if stype:
        game._createSprite([stype], (sprite.rect.left, sprite.rect.top))
    killSprite(sprite, partner, game)
    
def stepBack(sprite, partner, game):
    """ Revert last move. """
    sprite.rect=sprite.lastrect   
    
def undoAll(sprite, partner, game):
    """ Revert last moves of all sprites. """
    for s in game:
        s.rect=s.lastrect
            
def bounceForward(sprite, partner, game):
    """ The partner sprite pushed, so if possible move in the opposite direction. """
    sprite.physics.activeMovement(sprite, unitVector(partner.lastdirection))
    game._updateCollisionDict()
    
def turnAround(sprite, partner, game):
    sprite.rect=sprite.lastrect    
    sprite.lastmove = sprite.cooldown
    sprite.physics.activeMovement(sprite, DOWN)
    sprite.lastmove = sprite.cooldown
    sprite.physics.activeMovement(sprite, DOWN)
    reverseDirection(sprite, partner, game)
    game._updateCollisionDict()
    
def reverseDirection(sprite, partner, game):
    sprite.orientation = (-sprite.orientation[0], -sprite.orientation[1])
    
def bounceDirection(sprite, partner, game, friction=0):
    """ The centers of the objects determine the direction"""
    # TODO: not yet correct
    stepBack(sprite, partner, game)
    inc = sprite.orientation
    snorm = unitVector((-sprite.rect.centerx+partner.rect.centerx, 
                        -sprite.rect.centery+partner.rect.centery))
    dp = snorm[0]*inc[0]+snorm[1]*inc[1]
    sprite.orientation = (2*dp*snorm[0] - inc[0], 2*dp*snorm[1] - inc[1])   
    sprite.speed *= (1.-friction)
        
def wallBounce(sprite, partner, game, friction=0):
    """ Bounce off orthogonally to the wall. """
    if not oncePerStep(sprite, game, 'lastbounce'): 
        return
    sprite.speed *= (1.-friction)
    stepBack(sprite, partner, game)
    if abs(sprite.rect.centerx-partner.rect.centerx) > abs(sprite.rect.centery-partner.rect.centery):
        sprite.orientation = (-sprite.orientation[0], sprite.orientation[1])
    else:
        sprite.orientation = (sprite.orientation[0], -sprite.orientation[1])    
        
def wallStop(sprite, partner, game, friction=0):
    """ Stop just in front of the wall, removing that velocity component,
    but possibly sliding along it. """
    if not oncePerStep(sprite, game, 'laststop'): 
        return
    stepBack(sprite, partner, game)
    if abs(sprite.rect.centerx-partner.rect.centerx) > abs(sprite.rect.centery-partner.rect.centery):
        sprite.orientation = (0, sprite.orientation[1]*(1.-friction))
    else:
        sprite.orientation = (sprite.orientation[0]*(1.-friction), 0)        
    sprite.speed = vectNorm(sprite.orientation)*sprite.speed
    sprite.orientation = unitVector(sprite.orientation)
        
def killIfSlow(sprite, partner, game, limitspeed=1):
    """ Take a decision based on relative speed. """
    if sprite.is_static:
        relspeed = partner.speed
    elif partner.is_static:
        relspeed = sprite.speed
    else:
        relspeed = vectNorm((sprite._velocity()[0]-partner._velocity()[0], 
                             sprite._velocity()[1]-partner._velocity()[1]))
    if relspeed < limitspeed:
        killSprite(sprite, partner, game)

def drownSprite(sprite, partner, game):
    if not sprite.drowning_safe:
        killSprite(sprite, partner, game)
    
def drownSafe(sprite, partner, game):
    sprite.drowning_safe = True
    
def wrapAround(sprite, partner, game):
    """ Move to the edge of the screen in the direction the sprite is coming from. """
    if sprite.orientation[0] > 0:
        sprite.rect.left=0
    elif sprite.orientation[0] < 0:
        sprite.rect.left=game.screensize[0]-sprite.rect.size[0]
    if sprite.orientation[1] > 0:
        sprite.rect.top=0
    elif sprite.orientation[1] < 0:        
        sprite.rect.top=game.screensize[1]-sprite.rect.size[1]
    sprite.lastmove=0
    
def pullWithIt(sprite, partner, game):
    """ The partner sprite adds its movement to the sprite's. """
    if not oncePerStep(sprite, game, 'lastpull'): 
        return
    tmp = sprite.lastrect
    sprite._updatePos(partner.lastdirection, 1)
    sprite.speed=0
    sprite.lastrect = tmp
    
def teleportToExit(sprite, partner, game):
    e = choice(game.sprite_groups[partner.stype])
    sprite.rect=e.rect       
    sprite.lastmove=0