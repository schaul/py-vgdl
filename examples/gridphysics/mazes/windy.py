'''
VGDL example: the windy gridworld is a classical RL benchmark. 
Here: a deterministic and a stochastic version. 

@author: Tom Schaul
'''

windy_level = """
wwwwwwwwwwww
w          w
w   ...... w
w   ...--. w
w1  ...-0. w
w   ...--. w
w   ...--. w
w   ...--. w
wwwwwwwwwwww
"""


windymaze_game = """
BasicGame 
    LevelMapping
        w > wall
        . > lowwind
        - > highwind
        0 > goal
        1 > avatar
        
    SpriteSet         
        structure > Immovable
            wall         > 
            goal         > color=GREEN
            wind  > Conveyor orientation=UP
                lowwind  > strength=1 color=LIGHTBLUE
                highwind > strength=2 
                 
        avatar   > MovingAvatar

    InteractionSet
        avatar wall        > stepBack
        goal avatar        > killSprite
        avatar wind        > conveySprite

    
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(windymaze_game, windy_level)