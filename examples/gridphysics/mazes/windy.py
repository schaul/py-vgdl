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
wA  ...-G. w
w   ...--. w
w   ...--. w
w   ...--. w
wwwwwwwwwwww
"""


windymaze_game = """
BasicGame 
    LevelMapping
        . > lowwind
        - > highwind
        G > goal
        
    SpriteSet         
        structure > Immovable
            goal         > color=GREEN
            wind  > Conveyor orientation=UP
                lowwind  > strength=1 color=LIGHTBLUE
                highwind > strength=2 
        
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
        
    InteractionSet
        goal avatar        > killSprite"""

windy_det_game = windymaze_game+"""
        avatar wind        > conveySprite
        avatar wall        > stepBack
        
"""
windy_stoch_game = windymaze_game+"""
        avatar wind        > windGust
        avatar wall        > stepBack
        
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    #VGDLParser.playGame(windy_det_game, windy_level)
    VGDLParser.playGame(windy_stoch_game, windy_level)