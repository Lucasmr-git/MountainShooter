#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.entity import Entity


class EnemyShot(Entity):

    def __init__(self, x, y):

        super().__init__()

        self.name = "EnemyShot"

        self.speed = 8

        self.surf = pygame.image.load(
            "./asset/Enemy1Shot.png"
        ).convert_alpha()

        self.surf = pygame.transform.smoothscale(
            self.surf,
            (12, 24)
        )

        self.rect = self.surf.get_rect()

        self.rect.center = (x, y)

    def update(self):
        self.move()

    def move(self):

        self.rect.y += self.speed