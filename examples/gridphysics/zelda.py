'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''

zelda_level = """
wwwwwwwwwwwww
w1       w  w
w  w        w
w   w   w +ww
www w2  wwwww
w       w 0 w
w 2        ww
w     2    ww
wwwwwwwwwwwww
"""

        
zelda_game = """
BasicGame 
    SpriteSet         
        wall   > Immovable 
        goal   > Immovable color=GREEN
        key    > Immovable color=ORANGE
        sword  > Flicker limit=5  singleton=True
        movable > 
            avatar  > LinkAvatar   stype=sword 
                withoutkey >
                withkey    > color=ORANGE
            monster > RandomNPC    color=BROWN cooldown=2 speed=0.5
    LevelMapping
        w > wall
        0 > goal
        + > key        
        1 > withoutkey
        2 > monster            
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