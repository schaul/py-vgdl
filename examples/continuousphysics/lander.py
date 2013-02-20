'''
VGDL example: a lunar lander variant.

@author: Tom Schaul
'''

lander_game = """
BasicGame
    SpriteSet 
        pad    > Passive color=BLUE 
        avatar > InertialAvatar physicstype=GravityPhysics
            
    TerminationSet
        SpriteCounter stype=pad limit=4 win=True     
        SpriteCounter stype=avatar      win=False     
           
    InteractionSet
        avatar wall > killSprite 
        pad avatar  > killIfSlow    # relative velocity
        
    LevelMapping
        G > pad
"""

lander_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w        w    w            w
w    A    wwww             w
w                          w
w                          w
w                          w
w                          w
w                     www  w
w                    wwww  w
w       w        wwwwwwwwGGw
w      wwwwwGGGwwwwwwwwwwwww
w    wwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(lander_game, lander_level)
