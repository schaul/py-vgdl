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
                paratroopa > WalkJumper color=GREEN
        goal > Immovable color=GREEN
        wall > Immovable
            
    TerminationSet
        SpriteCounter stype=goal      win=True     
        SpriteCounter stype=avatar    win=False     
           
    InteractionSet
        moving EOS  > killSprite 
        goal avatar > killSprite
        avatar evil > killSprite
        moving wall > wallStop friction=0.1
        moving elevator > pullWithIt        
        elevator EOS    > wrapAround
        
    LevelMapping
        w > wall
        1 > avatar
        2 > goal
        3 > goomba
        4 > paratroopa
        = > elevator
"""

mario_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
w                          w
w                        23w
w             ===       wwww
w                     3    w
w                w  4 ww   w
w                wwwwwww   w
w                          w
w                          w
w          4        4      w
w        www      wwwwww   w
w 1      3   ===           w
wwww   wwww        4       w
wwwwwwwwww      wwww       w
"""

if __name__ == "__main__":
    from core import VGDLParser
    VGDLParser.playGame(mario_game, mario_level)
