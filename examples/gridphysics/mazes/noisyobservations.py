'''
The well-known 89-state maze which is difficult because its actions 
and its subjective observations are stochastic. 

@author: Tom Schaul
'''


maze_89 = """
wwwwwwwww
ww     ww
wA w w  w
ww w w ww
w  w w Gw
ww     ww
wwwwwwwww
"""

noisy_maze = """
BasicGame 
    LevelMapping
        G > goal  
    InteractionSet
        avatar wall        > stepBack
        goal avatar        > killSprite    
    SpriteSet         
        goal   > Immovable color=GREEN
        avatar > NoisyRotatingFlippingAvatar 
    TerminationSet
        SpriteCounter stype=goal limit=0 win=True
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playSubjectiveGame(noisy_maze, maze_89)