#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.entity import Entity
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Background(Entity):

    def __init__(self):

        super().__init__()

        self.name = "Background"

        self.surf = pygame.image.load(
            "./asset/Level1Background.png"
        ).convert()

        # Redimensiona o fundo para o tamanho da janela
        self.surf = pygame.transform.smoothscale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.rect = self.surf.get_rect()

        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass

    def move(self):
        pass

    def draw(self, window):

        window.blit(
            self.surf,
            self.rect
        )