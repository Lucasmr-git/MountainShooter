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

        # Pontuação necessária para vencer
        self.win_score = 300

        self.font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

        self.big_font = pygame.font.SysFont(
            "Arial",
            48,
            bold=True
        )

        self.game_over = False
        self.win = False

        for i in range(5):

            enemy = self.factory.get_entity("enemy")

            enemy.rect.x = 80 + (i * 120)
            enemy.rect.y = -100 - (i * 120)

            self.enemy_list.append(enemy)

    def update(self):

        if self.game_over or self.win:
            return

        self.player.update()

        for enemy in self.enemy_list:

            enemy.update()

            # Colisão jogador x inimigo
            if self.player.rect.colliderect(enemy.rect):

                self.player.hit()
                enemy.spawn()

            # Colisão tiro do inimigo x jogador
            for shot in enemy.shot_list[:]:

                if shot.rect.colliderect(self.player.rect):

                    enemy.shot_list.remove(shot)
                    self.player.hit()

            # Colisão tiro do jogador x inimigo
            for shot in self.player.shot_list[:]:

                if shot.rect.colliderect(enemy.rect):

                    self.player.shot_list.remove(shot)

                    enemy.spawn()

                    self.score += 15

                    if self.score >= self.win_score:

                        self.win = True
                        pygame.mixer.music.stop()

                    break

            if self.win:
                break

        if self.player.life <= 0:

            self.game_over = True
            pygame.mixer.music.stop()

    def draw(self):

        self.background.draw(self.window)

        # Jogador piscando quando está invencível
        if self.player.invincible % 10 < 5:

            self.window.blit(
                self.player.surf,
                self.player.rect
            )

        # Tiros do jogador
        for shot in self.player.shot_list:

            self.window.blit(
                shot.surf,
                shot.rect
            )

        # Inimigos e tiros dos inimigos
        for enemy in self.enemy_list:

            self.window.blit(
                enemy.surf,
                enemy.rect
            )

            for shot in enemy.shot_list:

                self.window.blit(
                    shot.surf,
                    shot.rect
                )

        # HUD
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        life_text = self.font.render(
            f"Lives: {self.player.life}",
            True,
            (255, 255, 255)
        )

        self.window.blit(score_text, (10, 10))
        self.window.blit(life_text, (10, 40))

        # Tela de vitória
        if self.win:

            win_text = self.big_font.render(
                "MISSION COMPLETE!",
                True,
                (0, 255, 0)
            )

            score_final = self.font.render(
                f"Pontuação final: {self.score}",
                True,
                (255, 255, 255)
            )

            info_text = self.font.render(
                "Pressione ESC para voltar ao menu",
                True,
                (255, 255, 255)
            )

            self.window.blit(
                win_text,
                (
                    WIN_WIDTH // 2 - win_text.get_width() // 2,
                    WIN_HEIGHT // 2 - 70
                )
            )

            self.window.blit(
                score_final,
                (
                    WIN_WIDTH // 2 - score_final.get_width() // 2,
                    WIN_HEIGHT // 2
                )
            )

            self.window.blit(
                info_text,
                (
                    WIN_WIDTH // 2 - info_text.get_width() // 2,
                    WIN_HEIGHT // 2 + 40
                )
            )

        # Tela de derrota
        if self.game_over:

            game_over_text = self.big_font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            score_final = self.font.render(
                f"Pontuação final: {self.score}",
                True,
                (255, 255, 255)
            )

            info_text = self.font.render(
                "Pressione ESC para voltar ao menu",
                True,
                (255, 255, 255)
            )

            self.window.blit(
                game_over_text,
                (
                    WIN_WIDTH // 2 - game_over_text.get_width() // 2,
                    WIN_HEIGHT // 2 - 70
                )
            )

            self.window.blit(
                score_final,
                (
                    WIN_WIDTH // 2 - score_final.get_width() // 2,
                    WIN_HEIGHT // 2
                )
            )

            self.window.blit(
                info_text,
                (
                    WIN_WIDTH // 2 - info_text.get_width() // 2,
                    WIN_HEIGHT // 2 + 40
                )
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