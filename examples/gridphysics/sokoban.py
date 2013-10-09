'''
VGDL example: a simplified Sokoban variant: push the boxes into the holes.

@author: Tom Schaul
'''

box_level = """
wwwwwwwwwwwww
w        w  w
w   1       w
w   A 1 w 0ww
www w1  wwwww
w       w 0 w
w 1        ww
w          ww
wwwwwwwwwwwww
"""

        
push_game = """
BasicGame frame_rate=30
    SpriteSet        
        hole   > Immovable color=DARKBLUE
        avatar > MovingAvatar #cooldown=4
        box    > Passive                
    LevelMapping
        0 > hole
        1 > box            
    InteractionSet
        avatar wall > stepBack        
        box avatar  > bounceForward
        box wall    > undoAll        
        box box     > undoAll
        box hole    > killSprite        
    TerminationSet
        SpriteCounter stype=box    limit=0 win=True          
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(push_game, box_level)    