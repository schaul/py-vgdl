'''
VGDL example: a simple game where you need to avoid incoming firestorms, by hiding behind boulders.

@author: Tom Schaul
'''


fire_game = """
BasicGame frame_rate=20
    SpriteSet    
        fire    > Spreader color=ORANGE spreadprob=0.45
        seed    > SpawnPoint color=RED stype=fire prob=0.1
        escape  > Immovable color=GREEN 
        avatar  > MovingAvatar
        wall    > Immovable color=DARKGRAY
            
    TerminationSet
        SpriteCounter stype=escape win=True     
        SpriteCounter stype=avatar win=False     
           
    InteractionSet
        escape avatar > killSprite 
        avatar fire   > killSprite
        fire   wall   > killSprite
        fire   fire   > killSprite
        avatar wall   > stepBack        
        
    LevelMapping
        1 > escape 
        0 > seed
"""

fire_level = """
wwwwwwwwwwwwwwwwwwwwwwwwwwww
wA w   w   w           w 0 w
w  w w     w  w    0   w   w
w    w  w       w      w   w
wwwwwwwwwww        ww      w
w 0                  w     w
w        ww             w  w
w          www w    ww     w
www    0           w       w
w0              w     w   1w
wwwwwwwwwwwwwwwwwwwwwwwwwwww
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(fire_game, fire_level)    