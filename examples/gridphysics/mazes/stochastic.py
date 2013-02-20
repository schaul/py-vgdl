'''
Some stochastic environments, with wind, gaze-attractors, slippery ground, etc.

@author: Tom Schaul (schaul@gmail.com)
'''

stoch_level = """
wwwwwwwwwwww
w0        <w
w www<wwww w
w----    w w
www- ww<=w w
w    w^== ^w
w  ===== www
w1 =======^w
wwwwwwwwwwww
"""


stoch_game = """
BasicGame 
    LevelMapping
        w > wall
        - > wind
        = > ice
        0 > goal
        1 > avatar
        < > tvleft
        ^ > tvup
        
    SpriteSet         
        structure > Immovable
            wall  > 
            goal  > color=GREEN
            tv    > Conveyor color=RED
                tvup    > orientation=UP
                tvleft  > orientation=LEFT
            ice   > color=WHITE
            wind  > Conveyor orientation=RIGHT strength=1
                                         
        avatar   > RotatingAvatar

    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
        
    InteractionSet
        goal avatar  > killSprite
        avatar wind  > windGust
        avatar tv    > attractGaze prob=1
        avatar ice   > slipForward prob=0.3
        avatar wall  > stepBack
        
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(stoch_game, stoch_level)