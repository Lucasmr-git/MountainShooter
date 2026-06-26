#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pygame

from code.entity import Entity
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.enemyShot import EnemyShot


class Enemy(Entity):

    def __init__(self):

        super().__init__()

        self.name = "Enemy"

        self.speed = random.randint(2, 4)

        self.surf = pygame.image.load(
            "./asset/Enemy1.png"
        ).convert_alpha()

        self.surf = pygame.transform.smoothscale(
            self.surf,
            (64, 64)
        )

        self.rect = self.surf.get_rect()

        self.shot_list = []

        # Tempo equilibrado entre disparos
        self.shot_delay = random.randint(90, 180)

        self.spawn()

    def spawn(self):

        self.rect.x = random.randint(
            20,
            WIN_WIDTH - self.rect.width - 20
        )

        self.rect.y = random.randint(
            -600,
            -80
        )

        self.speed = random.randint(2, 4)

        # Quando renasce, espera um pouco antes de atirar
        self.shot_delay = random.randint(90, 180)

    def update(self):

        self.move()

        if self.shot_delay > 0:
            self.shot_delay -= 1

        else:

            # Só atira se estiver aparecendo na tela
            if self.rect.top > 0 and self.rect.bottom < WIN_HEIGHT - 80:

                # Permite até 2 tiros ativos por inimigo
                if len(self.shot_list) < 2:

                    self.shot_list.append(
                        EnemyShot(
                            self.rect.centerx,
                            self.rect.bottom
                        )
                    )


            self.shot_delay = random.randint(90, 180)

        for shot in self.shot_list[:]:

            shot.update()

            if shot.rect.top > WIN_HEIGHT:
                self.shot_list.remove(shot)

    def move(self):

        self.rect.y += self.speed

        if self.rect.top > WIN_HEIGHT:
            self.spawn()