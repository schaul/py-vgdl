PyVGDL
=======

PyVGDL is a high-level video game description language (VGDL) built on top of pygame.

The aim is to decompose game descriptions into two parts: 1) a very high-level description, close to human language, to specify the dynamics, which builds on 2) an ontology of preprogrammed concepts for dynamics, interactions, control.
Programmers extend the possibilities of (1) by writing modules in (2), and game designers can very quickly compose new games from those components without programming.
 
Installation and Dependencies
-----------------------------

*  Get the [pygame](http://www.pygame.org/download.shtml) package

*  For all reinforcement learning usage, also get the [PyBrain](http://www.pybrain.org) machine learning library
 
*  Download repository 

          git clone git://github.com/schaul/py-vgdl.git
 
*  Try examples

          python examples/gridphysics/aliens.py
          python examples/gridphysics/frogs.py
          python examples/gridphysics/zelda.py

Features
--------
* Language
 * A simple programming language of 2D video game design
 * A parser for the language
 * A parser for textual level descriptions
 * An ontology with numerous high-level building blocks for games
     * grid-based physics engine
     * continous physics engine, including gravity, friction, etc.
* Classic examples (simplified versions)
 * Space invaders
 * Frogger
 * Lunar lander
 * Zelda
 * Super Mario
 * Portal
 * Sokoban
 * PTSP
* Human play
 * Interactive play, either from bird-eye viewpoint, or from first-person viewpoint
 * Create animated GIFs from replayed action sequences
* Bot play
 * Interface for artificial players (bots)
 * Conversion of game dynamics into the transition matrices of a Markov Decision Process (MDP)
 * Automaticlly generated local/subjective observation features
 * Reinforcement learning
     * Easy interface to RL algorithms from PyBrain
     * Classic grid world benchmarks
