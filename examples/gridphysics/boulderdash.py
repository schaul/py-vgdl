'''
VGDL example: Boulder Dash.

@author: Julian Togelius
'''

boulderdash_level = """
wwwwwwwwwwwwwwwwwwwwwwwwww
w...o.xx.o......o..xoxx..w
w...oooooo........o..o...w
w....xxx.........o.oxoo.ow
wx...............oxo...oow
wwwwwwwwww........o...wxxw
wb ...co..............wxxw
w  ........Ao....o....wxxw
wooo............. ....w..w
w......x....wwwwx x.oow..w
wc  .....x..ooxxo ....w..w
w   ..E..........b     ..w
wwwwwwwwwwwwwwwwwwwwwwwwww
"""

boulderdash_game = """
BasicGame
	SpriteSet
		dirt > Immovable color=BROWN
		exitdoor > Immovable color=GREEN
		diamond > Resource color=YELLOW res_limit=10
		boulder > Missile orientation=DOWN color=GRAY speed=0.2
		moving > 
			avatar > MovingAvatar color=WHITE 
			crab > RandomNPC
			butterfly > RandomNPC
	LevelMapping
		. > dirt
		E > exitdoor
		o > boulder
		x > diamond
		c > crab
		b > butterfly
	InteractionSet
		dirt avatar > killSprite
		diamond avatar > collectResource scoreChange=5
		diamond avatar > killSprite
		moving wall > stepBack
		moving boulder > stepBack
		avatar boulder > killIfFromAbove
		boulder boulder > stepBack
		avatar butterfly > killSprite
		avatar crab > killSprite
		boulder dirt > stepBack
		boulder wall > stepBack
		boulder diamond > stepBack
		crab dirt > stepBack
		crab diamond > stepBack
		butterfly dirt > stepBack
		butterfly diamond > stepBack
		crab butterfly > killSprite
		butterfly crab > transformTo stype=diamond scoreChange=1
		exitdoor avatar > killIfOtherHasMore resource=diamond limit=9 scoreChange=100
	
	TerminationSet
		SpriteCounter stype=avatar limit=0 win=False
		SpriteCounter stype=exitdoor limit=0 win=True
		
"""

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(boulderdash_game, boulderdash_level)  