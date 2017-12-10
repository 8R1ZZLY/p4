from src.classes.thing import GameRuler
from src.classes.thing import Factory
import pygame
import pygame.color
import os
from pygame.locals import *
from src.classes.client import Client
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(Factory.windowsize(),HWSURFACE|DOUBLEBUF)#RESIZABLE
    
    game = GameRuler(pygame,screen,[('Player 1',320),('Player 2','540')])
    game.runlocal()

if __name__ == '__main__':
    main()