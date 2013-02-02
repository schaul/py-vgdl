"""
The "fovea" benchmark from our 2011 IJCAI paper. It only becomes interesting with the right limited observation setup. 

@author: Tom Schaul
"""


maze_game = """
BasicGame 
    LevelMapping
        w > wall
        . > floortile
        0 > goal
        1 > avatar
        
    InteractionSet
        avatar wall        > stepBack
        goal avatar        > killSprite
        
    SpriteSet         
        structure > Immovable
            wall         > 
            floortile    > color=BLUE
            goal         > color=GREEN
        avatar   > MovingAvatar
    TerminationSet
        SpriteCounter stype=goal limit=4 win=True
"""

fovea_floor = """
wwwwwwwwwwwwwwwww
w..    ..     . w
w   ..      ..  w
w..0 .1  . 0 . .w
w ... .. .    ..w
w. . . . . .   .w
w    .  . .     w
w    . 0.  . .. w
w.  .   . . . ..w
w . .. .... ... w
w .... .....  ..w
w  0.. ..  0    w
w.  .  . . .  ..w
w ....   ...... w
w   .    . ... .w
w.  . .. ...... w
wwwwwwwwwwwwwwwww
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(maze_game, fovea_floor)    