'''
VGDL example: a simplified variant of the classic frogger game.

Logs spawn randomly, but trucks wrap around the screen and come back. 

@author: Tom Schaul
'''

frog_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w           wGw            w
w00==000000===0000=====000=2
w0000====0000000000====00012
w00===000===000====0000===02
www   ww   www    www  wwwww
w   ----   ---   -  ----   w
w-     xxx       xxx    xx w
w -   ---     -   ---- --  w
w       A                  w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""


frog_game = """
BasicGame
    SpriteSet
        forest > SpawnPoint stype=log prob=0.4  delay=10
        structure > Immovable
            water > color=BLUE
            goal  > color=GREEN
        log    > Missile    orientation=LEFT  speed=0.1 color=BROWN
        truck  > Missile    orientation=RIGHT 
            fasttruck  > speed=0.2  color=ORANGE
            slowtruck  > speed=0.1  color=RED
        avatar > Frog
        # defining 'wall' last, makes the walls show on top of all other sprites
        wall > Immovable                       
        
    InteractionSet
        goal avatar  > killSprite
        avatar log   > drownSafe
        avatar log   > pullWithIt   # note how one collision can have multiple effects
        avatar wall  > stepBack
        avatar water > drownSprite
        avatar truck > killSprite
        log    EOS   > killSprite
        truck  EOS   > wrapAround
    
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        G > goal
        0 > water
        1 > forest water       # note how a single character can spawn multiple sprites
        2 > forest wall log
        - > slowtruck
        x > fasttruck
        = > log water
         
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(frog_game, frog_level)    