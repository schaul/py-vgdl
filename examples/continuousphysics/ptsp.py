'''
VGDL example: a simplified version the physical TSP benchmark.

@author: Tom Schaul
'''


ptsp_game = """
BasicGame
    SpriteSet    
        wall   > Immovable
        pad    > Immovable color=BLUE 
        inertial > 
            avatar > InertialAvatar
            bullet > RandomInertial
            
    TerminationSet
        SpriteCounter stype=pad    win=True     
        SpriteCounter stype=avatar win=False     
           
    InteractionSet
        inertial wall > bounceDirection 
        avatar bullet > killSprite
        pad avatar    > killSprite
        
    LevelMapping
        w > wall
        1 > avatar
        2 > pad
        3 > bullet
"""

ptsp_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w        w    w    w       w
w    1    wwww    www      w
w                   w     ww
w             2     w  2   w
w   w                      w
w    www   3            w  w
w      wwwwwww        www  w
w                    ww    w
w  2                  w    w
w        ww  2           2 w
w     wwwwwwwwww           w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from core import VGDLParser
    VGDLParser.playGame(ptsp_game, ptsp_level)
        