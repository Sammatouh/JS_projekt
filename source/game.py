"""Moduł odpowiadajacy za wszystkie zdarzenia i czynności wykonywane podczas gry"""

from terrain import Terrain
from player import Player
from bullet import Bullet
import pygame

import defs


class Game:
    def __init__(self, scr_width, scr_height, clock, font):
        self.font = font

        self.running = True
        self.bullet_flying = False

        self.width = scr_width
        self.height = scr_height

        self.screen = pygame.display.set_mode((defs.SCR_WIDTH, defs.SCR_HEIGHT))
        self.clock = clock

        self.terrain = Terrain(self, defs.TERRAIN_ROUGHNESS)
        self.terrain.generate()

        self.players = [Player(self, defs.LEFT_PLR_X, self.terrain.heights[defs.LEFT_PLR_X] - defs.CANNON_H, defs.LEFT),
                        Player(self, defs.RIGHT_PLR_X, self.terrain.heights[defs.RIGHT_PLR_X] - defs.CANNON_H, defs.RIGHT)]
        self.current_player = self.players[0]
        self.idle_player = self.players[1]

    def game_loop(self):
        """Pętla główna gry"""
        while self.running:
            self.clock.tick(30)

            self.screen.fill(defs.BACKGROUND_COLOR)  # background color
            self.screen.blit(self.terrain.surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            shoot = self.current_player.do_move()
            if shoot:
                self.bullet_flying = True
                bullet = Bullet(self, shoot[0][0], shoot[0][1], shoot[1][0], shoot[1][1])

                while self.bullet_flying:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.bullet_flying = False
                            self.running = False
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.bullet_flying = False
                            self.running = False

                    # sprawdzanie czy nastąpiła kolizja pocisku z terenem
                    cords = self.terrain.mask.overlap(bullet.mask, (bullet.rect.x, bullet.rect.y))
                    if cords:
                        # jesli tak - zrób dziurę w miejscu uderzenia (promień - 20px)
                        self.terrain.make_hole(cords[0], cords[1], 20)
                        self.bullet_flying = False

                    # sprawdzanie czy pocisk trafił w przeciwnika
                    if bullet.rect.colliderect(self.idle_player.rect):
                        plr_hit = self.idle_player.mask.overlap(bullet.mask, (bullet.rect.x - self.idle_player.rect.x,
                                                                              bullet.rect.y - self.idle_player.rect.y))
                        if plr_hit:
                            self.players.remove(self.idle_player)
                            self.bullet_flying = False
                            print("Trafienie w gracza!")

                    bullet.update()
                    self.screen.fill(defs.BACKGROUND_COLOR)  # background color
                    self.screen.blit(self.terrain.surface, (0, 0))
                    bullet.draw(self.screen)
                    self.refresh_screen()

                if not self.bullet_flying:
                    if len(self.players) <= 1:
                        game_over = True
                        break

                    if self.current_player == self.players[0]:
                        self.current_player = self.players[1]
                        self.idle_player = self.players[0]
                    else:
                        self.current_player = self.players[0]
                        self.idle_player = self.players[1]

            self.refresh_screen()

    def draw_players(self):
        """Rysuje graczy na ekranie"""
        for player in self.players:
            player.draw(self.screen)
            pygame.draw.rect(self.screen, (255, 0, 0), player.rect, 1)

    def info_to_screen(self, msg, x, y):
        """Wyświetla dany tekst z początkiem w danych współrzędnych"""
        text = self.font.render(msg, True, (0, 0, 0))
        self.screen.blit(text, [x, y])

    def refresh_screen(self):
        self.draw_players()
        pygame.display.flip()
