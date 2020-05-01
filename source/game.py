"""Moduł odpowiadajacy za wszystkie zdarzenia i czynności wykonywane podczas gry"""

from terrain import *
from player import *
import pygame

import defs


class Game:
    def __init__(self, scr_width, scr_height, clock, font):
        self.font = font

        self.width = scr_width
        self.height = scr_height

        self.screen = pygame.display.set_mode((defs.SCR_WIDTH, defs.SCR_HEIGHT))
        self.clock = clock

        self.terrain = Terrain(self, 200)
        self.terrain.generate()

        self.players = [Player(self, 34, self.terrain.heights[34] - 46, defs.LEFT),
                        Player(self, 906, self.terrain.heights[921] - 46, defs.RIGHT)]
        self.current_player = self.players[0]

    def game_loop(self):
        """Pętla główna gry"""

        running = True
        while running:
            self.clock.tick(30)

            self.screen.fill((186, 233, 255))  # background color
            self.screen.blit(self.terrain.surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            shoot = self.current_player.do_move()
            if shoot:
                pygame.time.delay(600)
                if self.current_player == self.players[0]:
                    self.current_player = self.players[1]
                else:
                    self.current_player = self.players[0]

                if len(self.players) <= 1:
                    game_over = True
            self.draw_players()
            self.info_to_screen("Angle: {}".format(self.current_player.barrel_angle), self.current_player.x, 10)
            self.info_to_screen("Power: {}".format(self.current_player.power), self.current_player.x, 22)

            pygame.display.flip()

    def draw_players(self):
        """Rysuje graczy na ekranie"""

        for player in self.players:
            player.draw(self.screen)

    def info_to_screen(self, msg, x, y):
        """Wyświetla dany tekst z początkiem w danych współrzędnych"""

        text = self.font.render(msg, True, (0, 0, 0))
        self.screen.blit(text, [x, y])