'''
VGDL example: survive the onslaught of zombies for a while -- the bees are your friends, and their honey makes you strong...

@author: Tom Schaul
'''

zombie_level = """
wwwwwwwwwwwwwwwwwww
wA  .        ..  1w
w. .         ..  0w
wwwww        wwwwww
w     w ..     w1.w
w 0 2 wwwwwww    ww
w  .              w
wwwww     www     w
w  1w             w
w        ... 0  www
wwwwwwwwwwwwwwwwwww
"""

zombie_game = """
BasicGame
    SpriteSet    
        flower > SpawnPoint stype=bee    prob=0.02 color=PINK
        hell   > SpawnPoint stype=zombie prob=0.05 color=RED
        honey  > Resource color=GOLD limit=10 
        moving >
            avatar > MovingAvatar            
            bee    > RandomNPC speed=1   cooldown=3  color=YELLOW
            zombie > Chaser stype=avatar cooldown=6 speed=0.5 color=BROWN
            
    InteractionSet
        honey avatar    > collectResource scoreChange=1
        honey avatar    > killSprite
        moving wall     > stepBack
        avatar zombie   > killIfHasLess resource=honey limit=1 scoreChange=-1
        avatar zombie   > changeResource resource=honey value=-1
        zombie avatar   > killSprite
        bee zombie      > transformTo stype=honey
        zombie bee      > killSprite
        avatar hell     > killSprite
        
    TerminationSet
        Timeout limit=1000 win=True
        SpriteCounter stype=avatar limit=0 win=False
    
    LevelMapping
        0 > flower
        1 > hell
        . > honey
        2 > zombie
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(zombie_game, zombie_level)    