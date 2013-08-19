'''
Youtube_upload API Wrapper for use with py-vgdl

@author: Spyridon Samothrakis
'''
import sys
import external_libs.youtube_upload as yu


def upload(file_name):
    args = sys.argv[:]
    args[0] = file_name
    args.append("-c")
    args.append("Tech")
    yu.external_main(args)
    
