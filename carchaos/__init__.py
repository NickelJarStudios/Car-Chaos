#!/usr/bin/env python

from . import storage, player, level
try:
    import pygame, pygame.locals
except ImportError:
    print("""You don't have pygame installed. In order to use this application
        you must have pygame. See the README.md or README.txt file for
        instructions on how to get and install PyGame or run the installer.""")

class CarChaos:
    def __init__(self):
        pygame.init()