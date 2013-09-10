'''
VGDL example: Mario, jump around! 

@author: Tom Schaul
'''

mario_game = """
BasicGame
    SpriteSet 
        elevator > Missile orientation=UP speed=0.1 color=BLUE
        moving > physicstype=GravityPhysics
            avatar > MarioAvatar airsteering=True
            evil   >  orientation=LEFT
                goomba     > Walker     color=BROWN 
                paratroopa > WalkJumper color=RED
        goal > Immovable color=GREEN
            
    TerminationSet
        SpriteCounter stype=goal      win=True     
        SpriteCounter stype=avatar    win=False     
           
    InteractionSet
        evil avatar > killIfFromAbove scoreChange=1
        avatar evil > killIfAlive
        moving EOS  > killSprite 
        goal avatar > killSprite
        moving wall > wallStop friction=0.1
        moving elevator > pullWithIt        
        elevator EOS    > wrapAround
        
    LevelMapping
        G > goal
        1 > goomba
        2 > paratroopa
        = > elevator
"""

mario_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w                          w
w                        G1w
w             ===       wwww
w                     1    w
w                w  2 ww   w
w                wwwwwww   w
w                          w
w                          w
w          2        2      w
w        www      wwwwww   w
w A      1   ===           w
wwww   wwww        2       w
wwwwwwwwww      wwww       w
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(mario_game, mario_level)
