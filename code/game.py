#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu
from code.level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            size=(WIN_WIDTH, WIN_HEIGHT)
        )

        pygame.display.set_caption("Shadowed Sky")

    def run(self):

        while True:

            menu = Menu(self.window)
            option = menu.run()

            if option == 'NEW GAME 1P':

                level = Level(self.window)

                level.run()

            elif option == 'NEW GAME 2P - COP':
                print("Iniciando jogo coop...")

            elif option == 'SCORE':
                print("Abrindo placar...")

            elif option == 'EXIT':
                pygame.quit()
                return
