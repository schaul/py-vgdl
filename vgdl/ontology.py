'''
Video game description language -- ontology of concepts.

@author: Tom Schaul
'''

from random import choice, random

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


# ---------------------------------------------------------------------
#     Types of physics
# ---------------------------------------------------------------------
class GridPhysics():
    """ Define actions and key-mappings for grid-world dynamics. """
    
    def __init__(self, gridsize=(10,10)):
        self.gridsize = gridsize
        
    def _scaleDir(self, d):
        return (d[0]*self.gridsize[0], d[1]*self.gridsize[1])
        
    def keyDirection(self, keystate):        
        from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
        if keystate[K_RIGHT]:   return self._scaleDir(RIGHT)
        elif keystate[K_LEFT]:  return self._scaleDir(LEFT)
        elif keystate[K_UP]:    return self._scaleDir(UP)
        elif keystate[K_DOWN]:  return self._scaleDir(DOWN)
        else:                   return (0,0)
                
    def allDirections(self):
        """ Returns the 4 direction vectors. """
        return [self._scaleDir(UP), self._scaleDir(RIGHT), self._scaleDir(DOWN), self._scaleDir(LEFT)]


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
    
class Portal(Immovable):
    def __init__(self, stype=None, **kwargs):
        self.stype = stype
        VGDLSprite.__init__(self, **kwargs)    

class RandomNPC(VGDLSprite):
    """ Chooses randomly from all available actions each step. """    
    def update(self, game):
        self._updatePos(choice(self.physics.allDirections()))
        
class MovingAvatar(VGDLSprite):
    color=WHITE    
    
    def update(self, game):
        self._updatePos(self.physics.keyDirection(game.keystate))
        
class Frog(MovingAvatar):
    """ Has an additional flag that keeps if from drowning if true. """
    drowning_safe = False
    
    def update(self, game):
        MovingAvatar.update(self, game)
        self.drowning_safe = False
        
class FlakAvatar(VGDLSprite):
    """ Only horizontal moves. Hitting the space button creates a sprite of the 
    specified type at its location. """
    color=GREEN        
    def __init__(self, shoot=None, **kwargs):
        self.shoot = shoot
        VGDLSprite.__init__(self, **kwargs)
    
    def update(self, game):
        from pygame.locals import K_SPACE
        self._updatePos((self.physics.keyDirection(game.keystate)[0], 0))
        if self.shoot and game.keystate[K_SPACE]:
            game._createSprite([self.shoot], (self.rect.left, self.rect.top))
        
class Missile(VGDLSprite):
    """ A sprite that constantly moves in the same direction. """    
    def __init__(self, direction=None, **kwargs):
        VGDLSprite.__init__(self, **kwargs)
        if direction:   
            self.direction=direction
        else:
            self.direction=RIGHT
        
    def update(self, game):
        self._updatePos(self.physics._scaleDir(self.direction))
        
class RandomMissile(Missile):
    def __init__(self, **kwargs):
        Missile.__init__(self, direction=choice([UP, DOWN, LEFT, RIGHT]),
                         speedup = choice([0.1, 0.2, 0.4]), **kwargs)
        
class SpawnPoint(Immovable):
    prob  = None
    delay = None
    total = None
    color = BLACK
    
    def __init__(self, stype=None, delay=1, prob=1, total=None, **kwargs):
        VGDLSprite.__init__(self, **kwargs)
        self.stype = stype
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

class Bomber(SpawnPoint, Missile):
    direction = RIGHT
    color     = ORANGE
    is_static = False
    def update(self, game):
        Missile.update(self, game)
        SpawnPoint.update(self, game)
        
        
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
    """ Game ends when the number of sprites of type 'stype' hits 'limit'. """
    def __init__(self, limit=0, stype=None, win=True):
        self.limit = limit
        self.stype = stype
        self.win = win
    
    def isDone(self, game):
        if len(game.sprite_groups[self.stype]) == self.limit:
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
        if sum([len(game.sprite_groups[st]) for st in self.stypes])== self.limit:
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
    
def stepBack(sprite, partner, game):
    """ Revert last move. """
    sprite.rect=sprite.lastrect    
    
def undoAll(sprite, partner, game):
    """ Revert last moves of all sprites. """
    for s in game:
        s.rect=s.lastrect
            
def bounceForward(sprite, partner, game):
    """ The partner sprite pushed, so if possible move in the opposite direction. """
    sprite._updatePos(partner.lastdirection)
    # check for new induced collisions
    game._updateCollisionDict()
    
def turnAround(sprite, partner, game):
    sprite.rect=sprite.lastrect    
    sprite.lastmove = 100
    sprite._updatePos(sprite.physics._scaleDir(DOWN))
    sprite.lastmove = 100
    sprite._updatePos(sprite.physics._scaleDir(DOWN))
    changeDirection(sprite, partner, game)
    
def changeDirection(sprite, partner, game):
    if sprite.direction==RIGHT:
        sprite.direction=LEFT
    elif sprite.direction==LEFT:
        sprite.direction=RIGHT
    elif sprite.direction==UP:
        sprite.direction=DOWN
    elif sprite.direction==DOWN:
        sprite.direction=UP
        
def drownSprite(sprite, partner, game):
    if not sprite.drowning_safe:
        killSprite(sprite, partner, game)
    
def drownSafe(sprite, partner, game):
    sprite.drowning_safe = True
    
def wrapAround(sprite, partner, game):
    """ Move to the edge of the screen in the direction the sprite is coming from. """
    if sprite.direction[0] > 0:
        sprite.rect.left=0
    elif sprite.direction[0] < 0:
        sprite.rect.left=game.screensize[0]-sprite.rect.size[0]
    if sprite.direction[1] > 0:
        sprite.rect.top=0
    elif sprite.direction[1] < 0:        
        sprite.rect.top=game.screensize[1]-sprite.rect.size[1]
    sprite.lastmove=0
    
def pullWithIt(sprite, partner, game):
    """ The partner sprite adds its movement to the sprite's. """
    if hasattr(sprite, 'lastpull'):
        # pull only once per timestep, even if there are multiple collisions
        if sprite.lastpull == game.time:
            return
    sprite.lastpull = game.time
    tmp = sprite.lastrect
    sprite._updatePos(partner.lastdirection, speedup=1)
    sprite.lastrect = tmp
    
def teleportToExit(sprite, partner, game):
    e = choice(game.sprite_groups[partner.stype])
    sprite.rect=e.rect       
    sprite.lastmove=0