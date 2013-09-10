'''
VGDL example: Same as frogs.py, but uploads video on youtube

@author: Tom Schaul, Spyridon Samothrakis
'''

from frogs import frog_level, frog_game

if __name__ == "__main__":
    from vgdl.core import VGDLParser
    from vgdl.youtube import upload    
    game = VGDLParser.playGame(frog_game, frog_level, persist_movie=True) 
    upload(game.video_file)
    