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
        avatar EOS > killSprite 
        pad avatar  > killIfSlow    # relative velocity
        
    LevelMapping
        G > pad
"""

lander_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
         w    w            w
     A    wwww              
                            
                            
                            
                      www   
                     wwww  w
        w        wwwwwwwwGGw
       wwwwwGGGwwwwwwwwwwwww
     wwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(lander_game, lander_level)
