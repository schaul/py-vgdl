'''
VGDL example: a simplified version the physical TSP benchmark.

@author: Tom Schaul
'''


ptsp_game = """
BasicGame
    SpriteSet    
        pad    > Immovable color=BLUE 
        inertial > 
            avatar > InertialAvatar
            
    TerminationSet
        SpriteCounter stype=pad    win=True     
        SpriteCounter stype=avatar win=False     
           
    InteractionSet
        inertial wall > wallBounce 
        pad avatar    > killSprite
        
    LevelMapping
        G > pad
"""

ptsp_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w        w    w    w       w
w    A    wwww    www      w
w                   w     ww
w             G     w  G   w
w   w                      w
w    www                w  w
w      wwwwwww        www  w
w                    ww    w
w  G                  w    w
w        ww  G           G w
w     wwwwwwwwww           w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(ptsp_game, ptsp_level)
        
