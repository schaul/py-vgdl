'''
VGDL example: a simple game that lets you infect a population with enthusiasm.

@author: Tom Schaul
'''


infection_game = """
BasicGame
    SpriteSet
        virus > Immovable color=RED
        moving > 
            avatar > MovingAvatar 
                 normal   > color=WHITE
                 carrier  > color=RED 
            npc    > RandomNPC speed=0.25
                 host     > color=GREEN
                 infected > color=ORANGE speed=1
                 guardian > color=BLUE speed=0.1 
            
    TerminationSet
        SpriteCounter stype=host   win=True     
           
    InteractionSet
        moving wall       > stepBack
        avatar guardian   > transformTo stype=normal 
        host carrier      > transformTo stype=infected
        infected guardian > transformTo stype=host
        normal infected   > transformTo stype=carrier
        host infected     > transformTo stype=infected
        normal virus      > transformTo stype=carrier        
        host virus        > transformTo stype=infected
        guardian virus    > killSprite 
        
    LevelMapping
        1 > guardian
        0 > host
        X > virus
        A > normal
"""

chase_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
www  0  w   w   0 www 0w0  w
w       1   w        X w  0w
w 0     0 w   A        w0  w
w   wwwwwwww             0 w
w0                  ww  wwww
w    0  1 w        w    X  w
w0  w      wwwww   wX w  10w
wwww                wwX 1 Xw
wwww     0   0   0 www 0 Xww
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(infection_game, chase_level)    