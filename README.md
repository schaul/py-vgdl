# PyVGDL

PyVGDL is a high-level video game description language (VGDL) built on top of pygame.

The aim is to decompose game descriptions into two parts: 1) a very high-level description, close to human language, to specify the dynamics, which builds on 2) an ontology of preprogrammed concepts for dynamics, interactions, control.
Programmers extend the possibilities of (1) by writing modules in (2), and game designers can very quickly compose new games from those components without programming.


## References

The original idea was [discussed in the 2012 Dagstuhl seminar](http://drops.dagstuhl.de/opus/volltexte/2013/4338/pdf/9.pdf),
with a [full description](http://www.idsia.ch/~tom/publications/pyvgdl.pdf) presented at the IEEE CIG conference 2013 (this is also
the reference paper to [cite](http://www.idsia.ch/~tom/bibtex/pyvgdl.bib) if you use PyVGDL for academic work).
 
## Installation and Dependencies


### Dependencies
*  Get the [pygame](http://www.pygame.org/download.shtml) package
* (Alternative Method) Using Homebrew and virtualenv on Mac OSX

            brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
            pip install mercurial
            pip install hg+http://bitbucket.org/pygame/pygame

*  For all reinforcement learning usage, also get the [PyBrain](http://www.pybrain.org) machine learning library

*  For the upload to youtube functionality, you will need the [gdata](https://pypi.python.org/pypi/gdata) library
 
### Installation

using pip on linux

	sudo pip install git+git://github.com/schaul/py-vgdl.git

using pip on windows

	pip install git+git://github.com/schaul/py-vgdl.git
	
otherwise you can download it and install it using 

	python setup.py install
 
*  Try examples

          python -m examples.gridphysics.aliens
          python -m examples.gridphysics.frogs
          python -m examples.gridphysics.zelda

## Features

* Language
 * A simple programming language of 2D video game design
 * A parser for the language
 * A parser for textual level descriptions
 * An ontology with numerous high-level building blocks for games
     * grid-based physics engine
     * continuous physics engine, including gravity, friction, etc.
     * stochastic events
* Classic examples (simplified versions)
 * Space invaders
 * Frogger
 * Lunar lander
 * Zelda
 * Super Mario
 * Portal
 * Sokoban
 * PTSP
 * Pong
 * Tank wars
 * Dig-dug
 * Pacman
 * ...
* Human play
 * Interactive play, either from bird-eye viewpoint, or from first-person viewpoint
 * Create animated GIFs from replayed action sequences
* Bot play
 * Interface for artificial players (bots)
 * Conversion of game dynamics into the transition matrices of a Markov Decision Process (MDP)
 * Automatically generated local/subjective observation features
 * Reinforcement learning
     * Easy interface to RL algorithms from PyBrain
     * Classic grid world benchmarks
