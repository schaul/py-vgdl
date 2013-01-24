'''
VGDL example: a lunar lander variant.

@author: Tom Schaul
'''

lander_game = """
BasicGame
    SpriteSet 
        wall   > Immovable
        pad    > Passive color=BLUE 
        avatar > InertialAvatar physicstype=GravityPhysics
            
    TerminationSet
        SpriteCounter stype=pad limit=4 win=True     
        SpriteCounter stype=avatar      win=False     
           
    InteractionSet
        avatar wall > killSprite 
        pad avatar  > killIfSlow    # relative velocity
        
    LevelMapping
        w > wall
        1 > avatar
        2 > pad
"""

lander_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w        w    w            w
w    1    wwww             w
w                          w
w                          w
w                          w
w                          w
w                     www  w
w                    wwww  w
w       w        wwwwwwww22w
w      wwwww222wwwwwwwwwwwww
w    wwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(lander_game, lander_level)
