try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

libname="vgdl"
setup(
name = libname,
version="1.0",
description='A video game description language (VGDL) built on top pf pygame',
author='Tom Schaul',
url='https://github.com/schaul/py-vgdl',
packages=         ['vgdl'],
install_requires=['pygame']
)

