'''
VGDL example: Missile Command.

@author: Tom Schaul and Julian Togelius
'''
missilecommand_level = """
w    m     m    m   m  w
w                      w
w                      w
w                      w
w                      w
w                      w
w           A          w
w                      w
w                      w
w                      w
w     c     c      c   w
wwwwwwwwwwwwwwwwwwwwwwww
"""

missilecommand_game = """
BasicGame
  SpriteSet         
    city  > Immovable color=GREEN
    incoming > Chaser stype=city color=ORANGE speed=0.1
    explosion > Flicker limit=5 singleton=False
    avatar  > ShootAvatar stype=explosion 
  LevelMapping
    c > city
    m > incoming           
  InteractionSet
    movable wall  > stepBack
    incoming city > killSprite
    city incoming > killSprite
    incoming explosion > killSprite             
  TerminationSet
    SpriteCounter stype=city   win=False
    SpriteCounter stype=incoming win=True
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(missilecommand_game, missilecommand_level)  