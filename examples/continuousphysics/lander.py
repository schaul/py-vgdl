'''
VGDL example: a lunar lander variant.

@author: Tom Schaul
'''


lander_game = """
BasicGame
    SpriteSet    
        wall   > Immovable
        pad    > Immovable color=BLUE 
        avatar > LanderAvatar
            
    TerminationSet
        SpriteCounter stype=pad limit=1 win=True     
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
w                     wwwwww
w                    ww    w
w                     w    w
w            22wwww   w    w
w          wwwwwwwwwww     w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from core import VGDLParser
    #VGDLParser.playGame(lander_game, lander_level)
    #TODO    