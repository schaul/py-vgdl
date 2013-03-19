'''
VGDL example: a small digging game resembling Dig-Dug.

Collect gems and gold sacks, but don't let them fall on your head.
Also, double/long-clicking creates a rolling boulder that can kill enemies, but
you need to pick it up to use it again.

@author: Tom Schaul
'''


underground = """
wwwwwwwwwwwwwwwwwwwwwwwwwXwwwwwwwwwwww
wwwwwwwwwwwwww1wwwwwwwwww wwwwwwwwwwww
wwwwwwwwwwwwwwwwww1wwwwww0wwwwwwwwwwww
wwwwwwwww1wwwwww0 0 0 0ww wwwwwwwwwwww
wwww1wwww0wwwwwwwww1wwwww wwww1wwwwwww
www0w0www wwwwww0 0 0 www wwwwwww1wwww
wwww0w0ww0wwwwww 0 0 0www wwwwww0 0 0w
www0w0www ww1wwwwwwwwwwww wwwwww     w
ww0w0w0ww0wwwwwwwwwwwwwww wwwwww0 0 0w
www0w0www wwwwwwwwwwwwwww wwwwwwwwwwww
ww0w0w0ww0w111wwwwwwwwwww ww1wwwwwwwww
w wwwwwwwww   wwwwwwwwwww wwwwwww1wwww
w wwwwwwwww   w0wwwwwwww   wwwwww wwww
wA          w                     wwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
"""


digdug_game="""
BasicGame
    SpriteSet
        goodies > Immovable
            gold > color=YELLOW
            gem  > color=GREEN shrinkfactor=0.6
        shovel > OrientedFlicker limit=2 color=LIGHTGRAY
        weapon > singleton=True color=ORANGE
            boulder > Missile  speed=0.2 
            resting > Immovable speed=0
        moving > 
            avatar  > LinkAvatar stype=shovel
            monster > Missile color=RED orientation=DOWN cooldown=4
            falling > Missile orientation=DOWN color=YELLOW speed=0.5
        entrance > SpawnPoint total=5 cooldown=200 stype=monster
        
    LevelMapping
        0 > gem
        1 > gold
        X > entrance wall monster

    TerminationSet
        SpriteCounter  stype=avatar  limit=0 win=False
        MultiSpriteCounter  stype1=goodies stype2=monster limit=0 win=True
        
    InteractionSet
        moving  EOS  > stepBack
        weapon  EOS  > stepBack
        moving  wall > stepBack
        avatar gold  > stepBack
        boulder wall > stepBack
        monster wall > flipDirection
        monster EOS  > flipDirection
        falling wall > killSprite
        wall shovel  > killSprite  
        gem  avatar  > killSprite        
        weapon avatar> killSprite    
        avatar monster  > killSprite        
        monster boulder > killSprite
        moving falling  > killSprite
        shovel shovel> transformTo stype=boulder      
        boulder wall > transformTo stype=resting
        gold shovel  > transformTo stype=falling
        gold boulder > transformTo stype=falling
         
"""



if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(digdug_game, underground)    