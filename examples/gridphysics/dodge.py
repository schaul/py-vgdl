'''
VGDL example: a simple dodge-the-bullets game

@author: Tom Schaul
'''

bullet_level = """
wwwwwwwwwwwwwwwwwww
wA  w  <  -      Gw
w   w-            w
w            ww   w
w   < w ^      w  w
w ^   w   V    V ww
w   -        v    w
ww   <    www     w
w                 w
www     v       www
wwwwwwwwwwwwwwwwwww
"""

bullet_game = """
BasicGame
    SpriteSet
        bullet > Missile
            slowbullet > speed=0.1 color=ORANGE
                upslow    >     orientation=UP    
                downslow  >     orientation=DOWN  
                leftslow  >     orientation=LEFT  
                rightslow >     orientation=RIGHT
            fastbullet > speed=0.2  color=RED
                rightfast >     orientation=RIGHT
                downfast  >     orientation=DOWN  
        wall      > Immovable
        goal      > Immovable  color=GREEN
        
    InteractionSet
        goal   avatar > killSprite
        avatar bullet > killSprite
        avatar wall   > stepBack
        bullet EOS    > wrapAround
    
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        ^ > upslow
        < > leftslow
        v > downslow
        - > rightslow
        = > rightfast
        V > downfast
        G > goal
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(bullet_game, bullet_level)    