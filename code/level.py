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

        # Controle para não tocar sons finais várias vezes
        self.game_over_sound_played = False
        self.win_sound_played = False

        # Sons
        self.explosion_sound = self.load_sound("./asset/Explosion.wav", 1.0)
        self.hit_sound = self.load_sound("./asset/Hit.wav", 0.8)
        self.game_over_sound = self.load_sound("./asset/GameOver.wav", 1.0)
        self.win_sound = self.load_sound("./asset/Win.wav", 1.0)

        # Canal exclusivo para vitória e derrota
        self.end_channel = pygame.mixer.Channel(7)
        self.end_channel.set_volume(1.0)

        for i in range(5):

            enemy = self.factory.get_entity("enemy")

            enemy.rect.x = 80 + (i * 120)
            enemy.rect.y = -100 - (i * 120)

            self.enemy_list.append(enemy)

    def load_sound(self, path, volume=1.0):

        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            print(f"Som carregado: {path}")
            return sound

        except (pygame.error, FileNotFoundError) as error:
            print(f"Erro ao carregar som {path}: {error}")
            return None

    def play_sound(self, sound):

        if sound is not None:
            sound.play()

    def damage_player(self):

        life_before = self.player.life

        was_hit = self.player.hit()

        if was_hit and self.player.life < life_before:
            self.play_sound(self.hit_sound)

    def update(self):

        if self.game_over or self.win:
            return

        self.player.update()

        for enemy in self.enemy_list:

            enemy.update()

            # Colisão jogador x inimigo
            if self.player.rect.colliderect(enemy.rect):

                self.damage_player()
                enemy.spawn()

            # Colisão tiro do inimigo x jogador
            for shot in enemy.shot_list[:]:

                if shot.rect.colliderect(self.player.rect):

                    enemy.shot_list.remove(shot)
                    self.damage_player()

            # Colisão tiro do jogador x inimigo
            for shot in self.player.shot_list[:]:

                if shot.rect.colliderect(enemy.rect):

                    if shot in self.player.shot_list:
                        self.player.shot_list.remove(shot)

                    enemy.spawn()

                    # Som de explosão
                    self.play_sound(self.explosion_sound)

                    self.score += 10

                    # Condição de vitória
                    if self.score >= self.win_score and not self.win:

                        self.win = True

                        pygame.mixer.music.stop()

                        if not self.win_sound_played and self.win_sound is not None:
                            self.end_channel.play(self.win_sound)
                            self.win_sound_played = True

                    break

            if self.win:
                break

        # Condição de derrota
        if self.player.life <= 0 and not self.game_over:

            self.player.life = 0
            self.game_over = True

            pygame.mixer.music.stop()

            if not self.game_over_sound_played and self.game_over_sound is not None:
                self.end_channel.play(self.game_over_sound)
                self.game_over_sound_played = True

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
        pygame.mixer.music.set_volume(0.35)
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