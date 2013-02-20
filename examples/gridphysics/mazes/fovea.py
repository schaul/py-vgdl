"""
The "fovea" benchmark from our 2011 IJCAI paper. It only becomes interesting with the right limited observation setup. 

@author: Tom Schaul
"""


maze_game = """
BasicGame 
    LevelMapping
        . > floortile
        G > goal
        
    InteractionSet
        avatar wall        > stepBack
        goal avatar        > killSprite
        
    SpriteSet         
        structure > Immovable
            floortile    > color=BLUE
            goal         > color=GREEN
    TerminationSet
        SpriteCounter stype=goal limit=4 win=True
"""

fovea_floor = """
wwwwwwwwwwwwwwwww
w..    ..     . w
w   ..      ..  w
w..G .A  . G . .w
w ... .. .    ..w
w. . . . . .   .w
w    .  . .     w
w    . G.  . .. w
w.  .   . . . ..w
w . .. .... ... w
w .... .....  ..w
w  G.. ..  G    w
w.  .  . . .  ..w
w ....   ...... w
w   .    . ... .w
w.  . .. ...... w
wwwwwwwwwwwwwwwww
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(maze_game, fovea_floor)    