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

        self.speed = 10

        self.surf = pygame.image.load(
            "./asset/Player1.png"
        ).convert_alpha()

        self.surf = pygame.transform.smoothscale(
            self.surf,
            (64, 64)
        )

        self.rect = self.surf.get_rect()

        self.rect.center = (
            WIN_WIDTH // 2,
            WIN_HEIGHT - 120
        )

        # Sistema de tiros
        self.shot_list = []
        self.shot_delay = 0

        # Sistema de vidas
        self.life = 3

        # Invencibilidade temporária
        self.invincible = 0

        # Sons
        self.shoot_sound = self.load_sound("./asset/Shoot.wav", 0.3)

    def load_sound(self, path, volume=0.5):

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound

        except pygame.error:
            return None

    def update(self):

        self.move()

        if self.shot_delay > 0:
            self.shot_delay -= 1

        if self.invincible > 0:
            self.invincible -= 1

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

                if self.shoot_sound is not None:
                    self.shoot_sound.play()

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

    def hit(self):

        if self.invincible == 0:

            self.life -= 1

            self.invincible = 120

            return True

        return False