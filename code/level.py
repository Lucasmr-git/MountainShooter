#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.background import Background
from code.entityFactory import EntityFactory
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Level:

    def __init__(self, window):

        self.window = window

        self.clock = pygame.time.Clock()

        self.factory = EntityFactory()

        self.background = Background()

        self.player = self.factory.get_entity("player")

        self.enemy_list = []

        self.score = 0

        self.font = pygame.font.SysFont(
            "Arial",
            25,
            bold=True
        )

        for i in range(5):

            enemy = self.factory.get_entity("enemy")

            enemy.rect.x = 80 + (i * 120)
            enemy.rect.y = -100 - (i * 150)

            self.enemy_list.append(enemy)

    def update(self):

        self.player.update()

        for enemy in self.enemy_list:
            enemy.update()

        # Colisão entre tiros e inimigos

        for shot in self.player.shot_list[:]:

            for enemy in self.enemy_list:

                if shot.rect.colliderect(enemy.rect):

                    if shot in self.player.shot_list:
                        self.player.shot_list.remove(shot)

                    enemy.spawn()

                    self.score += 10

                    break

    def draw(self):

        # Fundo
        self.background.draw(self.window)

        # Jogador
        self.window.blit(
            self.player.surf,
            self.player.rect
        )

        # Tiros
        for shot in self.player.shot_list:

            self.window.blit(
                shot.surf,
                shot.rect
            )

        # Inimigos
        for enemy in self.enemy_list:

            self.window.blit(
                enemy.surf,
                enemy.rect
            )

        # HUD

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        self.window.blit(
            score_text,
            (10, 10)
        )

        pygame.display.flip()

    def run(self):

        pygame.mixer.music.load("./asset/Level1.mp3")
        pygame.mixer.music.play(-1)

        running = True

        while running:

            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return

            self.update()

            self.draw()