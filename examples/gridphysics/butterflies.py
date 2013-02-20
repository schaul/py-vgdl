'''
VGDL example: a simple chasing butterflies game.

If a butterfly hits a cocooned one, if frees it.
If they all are freed, you lose.

@author: Tom Schaul
'''


chase_game = """
BasicGame
    SpriteSet    
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
        1 > butterfly
        0 > cocoon
"""

chase_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w  1     1  w   0 0 0 0w000w
w 1                    w000w
w   1   0     A        w000w
wwwwwwwwwwww             00w
w0                  w     ww
w0      1                  w
w0         wwwww    1     0w
wwwww                w     w
w        0 0 0 0 0   w0   0w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(chase_game, chase_level)    