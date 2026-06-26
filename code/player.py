#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.entity import Entity
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.shot import Shot


class Player(Entity):

    def __init__(self):

        super().__init__()

        self.name = "Player"

        self.speed = 8

        self.surf = pygame.image.load(
            "./asset/Player1.png"
        ).convert_alpha()

        self.rect = self.surf.get_rect()

        self.rect.center = (
            WIN_WIDTH // 2,
            WIN_HEIGHT - 80
        )

        # Lista de tiros
        self.shot_list = []

        # Tempo entre disparos
        self.shot_delay = 0

    def update(self):

        self.move()

        if self.shot_delay > 0:
            self.shot_delay -= 1

        for shot in self.shot_list[:]:

            shot.update()

            if shot.rect.bottom < 0:
                self.shot_list.remove(shot)

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Disparo
        if keys[pygame.K_SPACE]:

            if self.shot_delay == 0:

                self.shot_list.append(
                    Shot(
                        self.rect.centerx,
                        self.rect.top
                    )
                )

                # Aproximadamente 5 tiros por segundo
                self.shot_delay = 12

        # Limites da tela

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT