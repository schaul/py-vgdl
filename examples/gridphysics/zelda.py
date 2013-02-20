'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''

zelda_level = """
wwwwwwwwwwwww
wA       w  w
w  w        w
w   w   w +ww
www w1  wwwww
w       w G w
w 1        ww
w     1    ww
wwwwwwwwwwwww
"""

        
zelda_game = """
BasicGame 
    SpriteSet         
        goal   > Immovable color=GREEN
        key    > Immovable color=ORANGE
        sword  > Flicker limit=5  singleton=True
        movable > 
            avatar  > LinkAvatar   stype=sword 
                withoutkey >
                withkey    > color=ORANGE
            monster > RandomNPC    color=BROWN cooldown=2 speed=0.5
    LevelMapping
        G > goal
        + > key        
        A > withoutkey
        1 > monster            
    InteractionSet
        movable wall   > stepBack
        withoutkey goal> stepBack
        goal withkey   > killSprite        
        monster sword  > killSprite        
        avatar monster > killSprite
        key  avatar    > killSprite
        withoutkey key > transformTo stype=withkey                
    TerminationSet
        SpriteCounter stype=goal   limit=0 win=True
        SpriteCounter stype=avatar limit=0 win=False              
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(zelda_game, zelda_level)    