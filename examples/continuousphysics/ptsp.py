'''
VGDL example: a simplified version the physical TSP benchmark.

@author: Tom Schaul
'''


ptsp_game = """
BasicGame
    SpriteSet    
        wall   > Immovable
        pad    > Immovable color=BLUE 
        avatar > InertialVehicle
            
    TerminationSet
        SpriteCounter stype=pad limit=0 win=True     
           
    InteractionSet
        avatar wall > changeDirection 
        pad avatar  > killSprite
        
    LevelMapping
        w > wall
        1 > avatar
        2 > pad
"""

ptsp_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w        w    w    w       w
w    1    wwww    www      w
w                   w     ww
w             2     w  2   w
w   w                      w
w    www                w  w
w      wwwwwww        www  w
w                    ww    w
w  2                  w    w
w        ww  2           2 w
w     wwwwwwwwww           w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from core import VGDLParser
    #VGDLParser.playGame(ptsp_game, ptsp_level)
    #TODO    