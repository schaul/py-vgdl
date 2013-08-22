'''
VGDL example: gain mana crystals, and use them to shoot fireballs through walls...

@author: Tom Schaul
'''

caster_level = """
wwwwwwwwwwwwwwwwwww
wA  .w  wwww .w wGw
w. . w  wwww w.  ww
wwwwww wwwww wwwwww
w     w wwww   w .w
w     wwwwwww    ww
w  .   w www  ww  w
wwwww   w.wwww    w
w  .w    w    ww  w
w         .     www
wwwwwwwwwwwwwwwwwww
"""

caster_game = """
BasicGame
    SpriteSet    
        goal   > Immovable color=GREEN
        mana   > Resource color=LIGHTBLUE res_limit=3
        fire   > Missile color=RED singleton=True
        avatar > ShootAvatar ammo=mana stype=fire
            
    InteractionSet
        mana avatar  > collectResource
        mana avatar  > killSprite
        avatar wall  > stepBack
        goal avatar  > killSprite
        wall fire    > killSprite
        fire wall    > killSprite
        
    TerminationSet
        SpriteCounter stype=avatar limit=0 win=False
        SpriteCounter stype=goal   limit=0 win=True
    
    LevelMapping
        G > goal
        . > mana        
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(caster_game, caster_level)    