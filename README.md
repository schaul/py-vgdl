py-vgdl
=======

A high-level video game description language (VGDL) built on top of pygame.

The aim is to decompose game descriptions into two parts: 1) a very high-level description, close to human language, to specify the dynamics, which builds on 2) an ontology of preprogrammed concepts for dynamics, interactions, control.
Programmers extend the possibilities of (1) by writing modules in (2), and game designers can very quickly compose new games from those components without programming.
 
Installation and Dependencies
-----------------------------

*  Get the [pygame](http://www.pygame.org/download.shtml) package
 
*  Download repository 

          git clone git://github.com/schaul/py-vgdl.git
 
*  Try examples

          python examples/gridphysics/aliens.py
          python examples/gridphysics/frogs.py
          python examples/gridphysics/zelda.py
