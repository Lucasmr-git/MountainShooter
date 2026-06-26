#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION


class Menu:

    def __init__(self, window):

        self.window = window

        self.surf = pygame.image.load(
            "./asset/MenuBg.png"
        ).convert()

        self.surf = pygame.transform.smoothscale(
            self.surf,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):

        pygame.mixer.music.load("./asset/Menu.mp3")
        pygame.mixer.music.play(-1)

        selected_option = 0

        while True:

            self.window.blit(
                self.surf,
                self.rect
            )

            # Título
            self.menu_text(
                text_size=80,
                text="Shadowed",
                text_color=(255, 128, 0),
                text_center_pos=(WIN_WIDTH / 2, 70)
            )

            self.menu_text(
                text_size=80,
                text="Sky",
                text_color=(255, 128, 0),
                text_center_pos=(WIN_WIDTH / 2, 120)
            )

            # Opções do menu
            for i in range(len(MENU_OPTION)):

                if i == selected_option:
                    color = (255, 255, 0)
                    text = f"> {MENU_OPTION[i]}"
                else:
                    color = (255, 255, 255)
                    text = MENU_OPTION[i]

                self.menu_text(
                    text_size=40,
                    text=text,
                    text_color=color,
                    text_center_pos=(WIN_WIDTH / 2, 200 + 30 * i)
                )

            # Controles (requisito do trabalho)
            self.menu_text(
                text_size=25,
                text="CONTROLES",
                text_color=(255, 255, 0),
                text_center_pos=(WIN_WIDTH / 2, 380)
            )

            self.menu_text(
                text_size=25,
                text="↑ ↓ ← →  Mover",
                text_color=(255, 255, 255),
                text_center_pos=(WIN_WIDTH / 2, 410)
            )

            self.menu_text(
                text_size=25,
                text="SPACE  Atirar",
                text_color=(255, 255, 255),
                text_center_pos=(WIN_WIDTH / 2, 435)
            )

            self.menu_text(
                text_size=25,
                text="ESC  Voltar / Sair",
                text_color=(255, 255, 255),
                text_center_pos=(WIN_WIDTH / 2, 460)
            )

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        selected_option -= 1

                        if selected_option < 0:
                            selected_option = len(MENU_OPTION) - 1

                    elif event.key == pygame.K_DOWN:
                        selected_option += 1

                        if selected_option >= len(MENU_OPTION):
                            selected_option = 0

                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return MENU_OPTION[selected_option]

    def menu_text(
        self,
        text_size: int,
        text: str,
        text_color: tuple,
        text_center_pos: tuple
    ) -> None:

        text_font: Font = pygame.font.SysFont(
            name="Lucida Sans Typewriter",
            size=text_size
        )

        text_surf: Surface = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        text_rect: Rect = text_surf.get_rect(
            center=text_center_pos
        )

        self.window.blit(
            text_surf,
            text_rect
        )