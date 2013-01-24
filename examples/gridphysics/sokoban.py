'''
VGDL example: a simplified Sokoban variant: push the boxes into the holes.

@author: Tom Schaul
'''

box_level = """
wwwwwwwwwwwww
w        w  w
w   2       w
w   1 2 w 0ww
www w2  wwwww
w       w 0 w
w 2        ww
w          ww
wwwwwwwwwwwww
"""

        
push_game = """
BasicGame frame_rate=30
    SpriteSet        
        wall   > Immovable 
        hole   > Immovable color=GREEN
        movable >
            avatar > MovingAvatar cooldown=4
            box    > Passive                
    LevelMapping
        w > wall
        0 > hole
        1 > avatar
        2 > box            
    InteractionSet
        avatar wall > stepBack        
        box avatar  > bounceForward
        box wall    > undoAll        
        box box     > undoAll
        movable hole> killSprite        
    TerminationSet
        SpriteCounter stype=box    limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False              
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(push_game, box_level)    