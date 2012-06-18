'''
VGDL example: a simple dodge-the-bullets game

@author: Tom Schaul
'''

bullet_level = """
wwwwwwwwwwwwwwwwwww
w1  w  <  -      2w
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
            slowbullet > speedup=0.1 color=ORANGE
                upslow    >     direction=UP    
                downslow  >     direction=DOWN  
                leftslow  >     direction=LEFT  
                rightslow >     direction=RIGHT
            fastbullet > speedup=0.2  color=RED
                rightfast >     direction=RIGHT
                downfast  >     direction=DOWN  
        wall      > Immovable
        goal      > Immovable  color=GREEN
        avatar    > MovingAvatar
    
    InteractionSet
        goal   avatar > killSprite
        avatar bullet > killSprite
        avatar wall   > stepBack
        bullet EOS    > wrapAround
    
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        w > wall
        ^ > upslow
        < > leftslow
        v > downslow
        - > rightslow
        = > rightfast
        V > downfast
        1 > avatar
        2 > goal
"""

if __name__ == "__main__":
    from core import VGDLParser
    VGDLParser.playGame(bullet_game, bullet_level)    