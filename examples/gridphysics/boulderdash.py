'''
VGDL example: Boulder Dash.

@author: Julian Togelius
'''

boulderdash_level = """
wwwwwwwwwwwwwwwwwwwwwwwwww
w...o.xx.o...............w
w...oooooo...............w
w....xxx.................w
wx.......................w
wwwwwwwwww...............w
w........................w
w..........A.............w
wooo.....................w
w........................w
wc  .....................w
w   ................C....w
wwwwwwwwwwwwwwwwwwwwwwwwww
"""

boulderdash_game = """
BasicGame
	SpriteSet
		avatar > MovingAvatar color=WHITE 
		dirt > Immovable color=BROWN
		exit > Immovable color=GREEN
		diamond > Missile orientation=DOWN color=YELLOW
		boulder > Missile orientation=DOWN color=GRAY speed=0.2
		crab > RandomNPC
		butterfly > RandomNPC
	LevelMapping
		. > dirt
		E > exit
		o > boulder
		x > diamond
	InteractionSet
		dirt avatar > killSprite
		diamond avatar > killSprite
		diamond dirt > stepBack
		diamond boulder > stepBack
		diamond wall > stepBack
		avatar wall > stepBack
		avatar boulder > stepBack
		boulder dirt > stepBack
		boulder wall > stepBack
		boulder diamond > stepBack
		crab wall > stepBack
		crab boulder > stepBack
		crab dirt > stepBack
		crab diamond > stepBack
		butterfly wall > stepBack
		butterfly boulder > stepBack
		butterfly dirt > stepBack
		butterfly diamond > stepBack
		
		
	TerminationSet
		SpriteCounter stype=diamond win=True
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(boulderdash_game, boulderdash_level)  