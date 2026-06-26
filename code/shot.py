#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.entity import Entity


class Shot(Entity):

    def __init__(self, x, y):

        super().__init__()

        self.name = "PlayerShot"

        self.speed = 12

        self.surf = pygame.image.load(
            "./asset/Player1Shot.png"
        ).convert_alpha()

        self.rect = self.surf.get_rect()

        self.rect.center = (x, y)

    def update(self):
        self.move()

    def move(self):

        self.rect.y -= self.speed