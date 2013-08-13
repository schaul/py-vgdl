'''
VGDL example: Pong, two-players and a ball

@author: Tom Schaul
'''



pong_game = """
BasicGame
    SpriteSet
        goal > Immovable color=GREEN
            othergoal > 
            mygoal    >
        racket > VerticalAvatar speed=0.25
            avatar      > alternate_keys=True
            otheravatar > color=BLUE 
        ball > Missile orientation=LEFT speed=5 color=ORANGE physicstype=NoFrictionPhysics
            
    TerminationSet # from the perspective of player 1 (on the left)
        SpriteCounter stype=othergoal limit=6 win=False     
        SpriteCounter stype=mygoal    limit=6 win=True     
           
    InteractionSet
        goal ball   > killSprite
        ball racket > wallBounce #bounceDirection
        ball wall   > wallBounce
        
    LevelMapping
        - > mygoal
        + > othergoal
        a > otheravatar
        o > ball
"""

pong_level = """
wwwwwwwwwwwwwwwwwwwwww
w+                  -w
w+                  -w
w+                  -w
w+A        o       a-w
w+                  -w
w+                  -w
w+                  -w
wwwwwwwwwwwwwwwwwwwwww
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(pong_game, pong_level)
