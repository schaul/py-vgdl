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
        bullet > Missile color=RED singleton=True
        fire   > Spreader color=ORANGE spreadprob=0.25
        avatar > ShootAvatar ammo=mana stype=bullet
            
    InteractionSet
        mana avatar  > collectResource scoreChange=5
        mana avatar  > killSprite
        avatar wall  > stepBack
        goal avatar  > killSprite scoreChange=100
        avatar fire  > killSprite
        wall bullet  > killSprite scoreChange=1
        bullet wall  > transformTo stype=fire
        fire   wall  > killSprite
        fire   fire  > killSprite
        mana   fire  > killSprite
        
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