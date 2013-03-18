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
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
GRAY = (90, 90, 90)
WHITE = (250, 250, 250)
BROWN = (140, 120, 100)
BLACK = (0, 0, 0)
ORANGE = (250, 160, 0)
YELLOW = (250, 250, 0)
PINK = (250, 200, 200)
LIGHTRED = (250, 50, 50)
LIGHTORANGE = (250, 200, 100)
LIGHTBLUE = (50, 100, 250)
LIGHTGREEN = (50, 250, 50)
LIGHTGRAY = (150, 150, 150)
DARKGRAY = (30, 30, 30)
DARKBLUE = (20, 20, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BASEDIRS = [UP, LEFT, DOWN, RIGHT]

# ---------------------------------------------------------------------
#     Types of physics
# ---------------------------------------------------------------------
class GridPhysics():
    """ Define actions and key-mappings for grid-world dynamics. """
    
    def __init__(self, gridsize=(10, 10)):
        self.gridsize = gridsize        
                
    def passiveMovement(self, sprite):
        if sprite.speed is None:
            speed = 1
        else:
            speed = sprite.speed        
        if speed != 0 and hasattr(sprite, 'orientation'):
            sprite._updatePos(sprite.orientation, speed * self.gridsize[0])   
    
    def activeMovement(self, sprite, action, speed=None):
        if speed is None:
            if sprite.speed is None:
                speed = 1
            else:
                speed = sprite.speed
        if speed != 0 and action is not None:
            sprite._updatePos(action, speed * self.gridsize[0])
            
            
    def distance(self, r1, r2):
        """ Grid physics use Hamming distances. """
        return (abs(r1.top - r2.top) 
                + abs(r1.left - r2.left))
    
    
class ContinuousPhysics(GridPhysics):
    gravity = 0.
    friction = 0.02    
    
    def passiveMovement(self, sprite):
        if sprite.speed != 0 and hasattr(sprite, 'orientation'):
            sprite._updatePos(sprite.orientation, sprite.speed)   
            if self.gravity > 0 and sprite.mass > 0:
                self.activeMovement(sprite, (0, self.gravity * sprite.mass))        
            sprite.speed *= (1 - self.friction)
            
    def activeMovement(self, sprite, action, speed=None):
        """ Here the assumption is that the controls determine the direction of
        acceleration of the sprite. """
        if speed is None:
            speed = sprite.speed
        v1 = action[0] / float(sprite.mass) + sprite.orientation[0] * speed
        v2 = action[1] / float(sprite.mass) + sprite.orientation[1] * speed
        sprite.orientation = unitVector((v1, v2))        
        sprite.speed = vectNorm((v1, v2)) / vectNorm(sprite.orientation)
        
    def distance(self, r1, r2):
        """ Continuous physics use Euclidean distances. """
        return sqrt((r1.top - r2.top) ** 2 
                    + (r1.left - r2.left) ** 2)

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
    stype = None   
    
class Portal(SpriteProducer):
    is_static = True
    color = BLUE

class SpawnPoint(SpriteProducer):
    prob = None
    total = None
    color = BLACK
    cooldown = None
    is_static = True    
    def __init__(self, cooldown=1, prob=1, total=None, **kwargs):
        SpriteProducer.__init__(self, **kwargs)
        if prob:
            self.prob = prob
            self.is_stochastic = (prob > 0 and prob < 1)
        if cooldown:
            self.cooldown = cooldown        
        if total:
            self.total = total        
        self.counter = 0
        
    def update(self, game):
        if (game.time % self.cooldown == 0 and random() < self.prob):
            game._createSprite([self.stype], (self.rect.left, self.rect.top))
            self.counter += 1
            
        if self.total and self.counter >= self.total:
            killSprite(self, None, game) 

class RandomNPC(VGDLSprite):
    """ Chooses randomly from all available actions each step. """    
    speed = 1
    is_stochastic = True
    
    def update(self, game):
        VGDLSprite.update(self, game)
        self.physics.activeMovement(self, choice(BASEDIRS))    
                    
class OrientedSprite(VGDLSprite):
    """ A sprite that maintains the current orientation. """    
    draw_arrow = False
    orientation = RIGHT    
    
    def _draw(self, screen):
        """ With a triangle that shows the orientation. """
        VGDLSprite._draw(self, screen)
        if self.draw_arrow:
            col = (self.color[0], 255 - self.color[1], self.color[2])
            pygame.draw.polygon(screen, col, triPoints(self.rect, unitVector(self.orientation)))

class Conveyor(OrientedSprite):
    """ A static object that used jointly with the 'conveySprite' interaction to move 
    other sprites around."""
    is_static = True
    color = BLUE
    strength = 1
    draw_arrow = True
    
class Missile(OrientedSprite):
    """ A sprite that constantly moves in the same direction. """            
    speed = 1 
    
class OrientedFlicker(OrientedSprite, Flicker):
    """ Preserves directionality """
    draw_arrow = True    
    speed = 0
    
class Walker(Missile):
    """ Keep moving in the current horizontal direction. If stopped, pick one randomly. """
    airsteering = False
    is_stochastic = True
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
    is_stochastic = True         
    def update(self, game):
        if self.lastdirection[0] == 0:
            if self.prob < random():
                self.physics.activeMovement(self, (0, -self.strength))    
        Walker.update(self, game)
        
    
class RandomInertial(OrientedSprite, RandomNPC):
    physicstype = ContinuousPhysics    
        
class RandomMissile(Missile):
    def __init__(self, **kwargs):
        Missile.__init__(self, orientation=choice(BASEDIRS),
                         speed=choice([0.1, 0.2, 0.4]), **kwargs)
        
class ErraticMissile(Missile):
    """ A missile that randomly changes direction from time to time.
    (with probability 'prob' per timestep). """
    def __init__(self, prob=0.1, **kwargs):
        Missile.__init__(self, orientation=choice(BASEDIRS), **kwargs)
        self.prob = prob
        self.is_stochastic = (prob > 0 and prob < 1)
    
    def update(self, game):
        Missile.update(self, game)
        if random() < self.prob:
            self.orientation = choice(BASEDIRS)

class Bomber(SpawnPoint, Missile):
    color = ORANGE
    is_static = False    
    def update(self, game):
        Missile.update(self, game)
        SpawnPoint.update(self, game)

class Chaser(RandomNPC):
    """ Pick an action that will move toward the closest sprite of the provided target type. """
    stype = None    
    fleeing = False
    
    def _closestTargets(self, game):
        bestd = 1e100
        res = []
        for target in game.getSprites(self.stype):
            d = self.physics.distance(self.rect, target.rect)
            if d < bestd:
                bestd = d
                res = [target]
            elif d == bestd:
                res.append(target)
        return res
    
    def _movesToward(self, game, target):
        """ Find the canonical direction(s) which move toward
        the target. """
        res = []
        basedist = self.physics.distance(self.rect, target.rect) 
        for a in BASEDIRS:
            r = self.rect.copy()
            r = r.move(a)
            newdist = self.physics.distance(r, target.rect)
            if self.fleeing and basedist < newdist:
                res.append(a)
            if not self.fleeing and basedist > newdist:
                res.append(a)
        return res
    
    def update(self, game):
        VGDLSprite.update(self, game)
        options = []
        for target in self._closestTargets(game):
            options.extend(self._movesToward(game, target))
        if len(options) == 0:
            options = BASEDIRS
        self.physics.activeMovement(self, choice(options))    
                    
class Fleeing(Chaser):
    """ Just reversing directions"""
    fleeing = True
    
    
    
# ---------------------------------------------------------------------
#     Avatars: player-controlled sprite types
# ---------------------------------------------------------------------
from core import Avatar

class MovingAvatar(VGDLSprite, Avatar):
    """ Default avatar, moves in the 4 cardinal directions. """
    color = WHITE    
    speed = 1    
    is_avatar = True
    def _readAction(self, game):        
        actions = self._readMultiActions(game)
        if actions:
            return actions[0]
        else:
            return None
        
    def _readMultiActions(self, game):
        """ Read multiple simultaneously pressed button actions. """        
        from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
        res = []
        if   game.keystate[K_RIGHT]: res += [RIGHT]
        elif game.keystate[K_LEFT]:  res += [LEFT]
        if   game.keystate[K_UP]:    res += [UP]
        elif game.keystate[K_DOWN]:  res += [DOWN]
        return res

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
    color = GREEN            
    def update(self, game):
        VGDLSprite.update(self, game)        
        action = self._readAction(game)
        if action in [RIGHT, LEFT]:
            self.physics.activeMovement(self, action)
        from pygame.locals import K_SPACE
        if self.stype and game.keystate[K_SPACE]:
            game._createSprite([self.stype], (self.rect.left, self.rect.top))
            
class OrientedAvatar(OrientedSprite, MovingAvatar):
    """ Avatar retains its orientation, but moves in cardinal directions. """
    draw_arrow = True          
    def update(self, game):
        tmp = self.orientation
        self.orientation = (0, 0)
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
            
class RotatingAvatar(OrientedSprite, MovingAvatar):                
    """ Avatar retains its orientation, and moves forward/backward or rotates 
    relative to that. """
    draw_arrow = True      
    speed = 0    
    def update(self, game):
        actions = self._readMultiActions(game)
        if UP in actions:
            self.speed = 1
        elif DOWN in actions:
            self.speed = -1
        if LEFT in actions:
            i = BASEDIRS.index(self.orientation)
            self.orientation = BASEDIRS[(i + 1) % len(BASEDIRS)]
        elif RIGHT in actions:
            i = BASEDIRS.index(self.orientation)
            self.orientation = BASEDIRS[(i - 1) % len(BASEDIRS)]    
        VGDLSprite.update(self, game)
        self.speed = 0
        
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
            newones = game._createSprite([self.stype], (self.lastrect.left + u[0] * self.lastrect.size[0],
                                                       self.lastrect.top + u[1] * self.lastrect.size[1]))
            if len(newones) > 0  and isinstance(newones[0], OrientedSprite):
                newones[0].orientation = unitVector(self.orientation)
                            
class InertialAvatar(OrientedAvatar):
    speed = 1
    physicstype = ContinuousPhysics
    def update(self, game):
        MovingAvatar.update(self, game)
        
class MarioAvatar(InertialAvatar):
    """ Mario can have two states: in contact with the ground, or in parabolic flight. """
    physicstype = GravityPhysics    
    draw_arrow = False
    strength = 10
    airsteering = False    
    def update(self, game):
        action = self._readAction(game)
        if action is None:
            action = (0, 0)
        from pygame.locals import K_SPACE
        if game.keystate[K_SPACE] and self.orientation[1] == 0:
            action = (action[0] * sqrt(self.strength), -self.strength)
        elif self.orientation[1] == 0 or self.airsteering:
            action = (action[0] * sqrt(self.strength), 0)
        else:
            action = (0, 0)
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
        if sum([game.numSprites(st) for st in self.stypes]) == self.limit:
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
    
def transformTo(sprite, partner, game, stype='wall'):
    newones = game._createSprite([stype], (sprite.rect.left, sprite.rect.top))
    if len(newones) > 0:
        if isinstance(sprite, OrientedSprite) and isinstance(newones[0], OrientedSprite):
            newones[0].orientation = sprite.orientation
        killSprite(sprite, partner, game)
    
def stepBack(sprite, partner, game):
    """ Revert last move. """
    sprite.rect = sprite.lastrect   
    
def undoAll(sprite, partner, game):
    """ Revert last moves of all sprites. """
    for s in game:
        s.rect = s.lastrect
            
def bounceForward(sprite, partner, game):
    """ The partner sprite pushed, so if possible move in the opposite direction. """
    sprite.physics.activeMovement(sprite, unitVector(partner.lastdirection))
    game._updateCollisionDict()

def conveySprite(sprite, partner, game):
    """ Moves the partner in target direction by some step size. """
    tmp = sprite.lastrect
    v = unitVector(partner.orientation)
    sprite.physics.activeMovement(sprite, v, speed=partner.strength)
    sprite.lastrect = tmp
    game._updateCollisionDict()
    
def windGust(sprite, partner, game):
    """ Moves the partner in target direction by some step size, but stochastically
    (step, step-1 and step+1 are equally likely) """
    s = choice([partner.strength, partner.strength + 1, partner.strength - 1])
    if s != 0:
        tmp = sprite.lastrect
        v = unitVector(partner.orientation)
        sprite.physics.activeMovement(sprite, v, speed=s)
        sprite.lastrect = tmp
        game._updateCollisionDict()
        
def slipForward(sprite, partner, game, prob=0.5):
    """ Slip forward in the direction of the current orientation, sometimes."""
    if prob > random():
        tmp = sprite.lastrect        
        v = unitVector(sprite.orientation)
        sprite.physics.activeMovement(sprite, v, speed=1)
        sprite.lastrect = tmp
        game._updateCollisionDict()
        
def attractGaze(sprite, partner, game, prob=0.5):
    """ Turn the orientation to the value given by the partner. """
    if prob > random():
        sprite.orientation = partner.orientation    
    
def turnAround(sprite, partner, game):
    sprite.rect = sprite.lastrect    
    sprite.lastmove = sprite.cooldown
    sprite.physics.activeMovement(sprite, DOWN)
    sprite.lastmove = sprite.cooldown
    sprite.physics.activeMovement(sprite, DOWN)
    reverseDirection(sprite, partner, game)
    game._updateCollisionDict()
    
def reverseDirection(sprite, partner, game):
    sprite.orientation = (-sprite.orientation[0], -sprite.orientation[1])
    
def flipDirection(sprite, partner, game):
    sprite.orientation = choice(BASEDIRS)
    
def bounceDirection(sprite, partner, game, friction=0):
    """ The centers of the objects determine the direction"""
    # TODO: not yet correct
    stepBack(sprite, partner, game)
    inc = sprite.orientation
    snorm = unitVector((-sprite.rect.centerx + partner.rect.centerx,
                        - sprite.rect.centery + partner.rect.centery))
    dp = snorm[0] * inc[0] + snorm[1] * inc[1]
    sprite.orientation = (2 * dp * snorm[0] - inc[0], 2 * dp * snorm[1] - inc[1])   
    sprite.speed *= (1. - friction)
            
def wallBounce(sprite, partner, game, friction=0):
    """ Bounce off orthogonally to the wall. """
    if not oncePerStep(sprite, game, 'lastbounce'): 
        return
    sprite.speed *= (1. - friction)
    stepBack(sprite, partner, game)
    if abs(sprite.rect.centerx - partner.rect.centerx) > abs(sprite.rect.centery - partner.rect.centery):
        sprite.orientation = (-sprite.orientation[0], sprite.orientation[1])
    else:
        sprite.orientation = (sprite.orientation[0], -sprite.orientation[1])    
        
def wallStop(sprite, partner, game, friction=0):
    """ Stop just in front of the wall, removing that velocity component,
    but possibly sliding along it. """
    if not oncePerStep(sprite, game, 'laststop'): 
        return
    stepBack(sprite, partner, game)
    if abs(sprite.rect.centerx - partner.rect.centerx) > abs(sprite.rect.centery - partner.rect.centery):
        sprite.orientation = (0, sprite.orientation[1] * (1. - friction))
    else:
        sprite.orientation = (sprite.orientation[0] * (1. - friction), 0)        
    sprite.speed = vectNorm(sprite.orientation) * sprite.speed
    sprite.orientation = unitVector(sprite.orientation)
        
def killIfSlow(sprite, partner, game, limitspeed=1):
    """ Take a decision based on relative speed. """
    if sprite.is_static:
        relspeed = partner.speed
    elif partner.is_static:
        relspeed = sprite.speed
    else:
        relspeed = vectNorm((sprite._velocity()[0] - partner._velocity()[0],
                             sprite._velocity()[1] - partner._velocity()[1]))
    if relspeed < limitspeed:
        killSprite(sprite, partner, game)

def drownSprite(sprite, partner, game):
    if not sprite.drowning_safe:
        killSprite(sprite, partner, game)
    
def drownSafe(sprite, partner, game):
    sprite.drowning_safe = True
    
def wrapAround(sprite, partner, game, offset=0):
    """ Move to the edge of the screen in the direction the sprite is coming from. 
    Plus possibly an offset. """
    if sprite.orientation[0] > 0:
        sprite.rect.left = offset * sprite.rect.size[1]
    elif sprite.orientation[0] < 0:
        sprite.rect.left = game.screensize[0] - sprite.rect.size[0] * (1 + offset)
    if sprite.orientation[1] > 0:
        sprite.rect.top = offset * sprite.rect.size[1]
    elif sprite.orientation[1] < 0:        
        sprite.rect.top = game.screensize[1] - sprite.rect.size[1] * (1 + offset)
    sprite.lastmove = 0
    
def pullWithIt(sprite, partner, game):
    """ The partner sprite adds its movement to the sprite's. """
    if not oncePerStep(sprite, game, 'lastpull'): 
        return
    tmp = sprite.lastrect
    v = unitVector(partner.lastdirection)
    sprite._updatePos(v, partner.speed * sprite.physics.gridsize[0])
    if isinstance(sprite.physics, ContinuousPhysics):
        sprite.speed = partner.speed
        sprite.orientation = partner.lastdirection
    sprite.lastrect = tmp
    
def teleportToExit(sprite, partner, game):
    e = choice(game.sprite_groups[partner.stype])
    sprite.rect = e.rect       
    sprite.lastmove = 0
    
# this allows us to determine whether the game has stochastic elements or not
stochastic_effects = [teleportToExit, windGust, slipForward, attractGaze, flipDirection]

# this allows is to determine which effects might kill a sprite
kill_effects = [killSprite, drownSprite, killIfSlow, transformTo]
