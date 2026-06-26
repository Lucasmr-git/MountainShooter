#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pygame

from code.entity import Entity
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Enemy(Entity):

    def __init__(self):

        super().__init__()

        self.name = "Enemy"

        self.speed = random.randint(2, 5)

        self.surf = pygame.image.load(
            "./asset/Enemy1.png"
        ).convert_alpha()

        self.rect = self.surf.get_rect()

        self.spawn()

    def spawn(self):

        self.rect.x = random.randint(
            0,
            WIN_WIDTH - self.rect.width
        )

        self.rect.y = random.randint(
            -600,
            -50
        )

        self.speed = random.randint(2, 5)

    def update(self):
        self.move()

    def move(self):

        self.rect.y += self.speed

        if self.rect.top > WIN_HEIGHT:
            self.spawn()