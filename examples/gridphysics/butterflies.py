'''
VGDL example: a simple chasing butterflies game.

If a butterfly hits a cocooned one, if frees it.
If they all are freed, you lose.

@author: Tom Schaul
'''


chase_game = """
BasicGame
    SpriteSet    
        wall   > Immovable
        cocoon > Immovable color=BLUE 
        animal > physicstype=GridPhysics
            avatar    > MovingAvatar 
            butterfly > RandomNPC speed=0.6
            
    TerminationSet
        SpriteCounter stype=butterfly win=True     
        SpriteCounter stype=cocoon    win=False     
           
    InteractionSet
        butterfly avatar > killSprite 
        butterfly cocoon > cloneSprite
        cocoon butterfly > killSprite
        animal    wall   > stepBack        
        
    LevelMapping
        w > wall
        1 > avatar
        2 > butterfly
        3 > cocoon
"""

chase_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w  2     2  w   3 3 3 3w333w
w 2                    w333w
w   2   3     1        w333w
wwwwwwwwwwww             33w
w3                  w     ww
w3      2                  w
w3         wwwww    2     3w
wwwww                w     w
w        3 3 3 3 3   w3   3w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(chase_game, chase_level)    