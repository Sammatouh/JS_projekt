"""Moduł odpowiadajacy za wszystkie zdarzenia i czynności wykonywane podczas gry"""

import pygame

import bullet
import defs
import player
import terrain


class Game:
    def __init__(self, scr_width, scr_height, clock):
        self.running = True
        self.playing = False
        self.bullet_flying = False

        self.bullet = None

        self.width = scr_width
        self.height = scr_height

        self.screen = pygame.display.set_mode((defs.SCR_WIDTH, defs.SCR_HEIGHT))
        self.clock = clock

        self.terrain = terrain.Terrain(self, defs.TERRAIN_ROUGHNESS)

        self.players = []
        self.current_player = None
        self.idle_player = None

    def new_game(self):
        """Rozpoczęcie nowej gry"""
        self.terrain.generate()

        self.players = [player.Player(self, defs.LEFT_PLR_X, self.terrain.heights[defs.LEFT_PLR_X] - defs.CANNON_H, defs.LEFT),
                        player.Player(self, defs.RIGHT_PLR_X, self.terrain.heights[defs.RIGHT_PLR_X] - defs.CANNON_H, defs.RIGHT)]
        self.current_player = self.players[0]
        self.idle_player = self.players[1]

    def game_loop(self):
        """Pętla główna gry"""
        self.playing = True
        while self.playing:
            self.clock.tick(30)

            self.screen.fill(defs.Colors.BACKGROUND_COLOR)  # background color
            self.screen.blit(self.terrain.surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

            shoot = self.current_player.do_move()
            if shoot:
                self.bullet_flying = True
                self.bullet = bullet.Bullet(self, shoot[0][0], shoot[0][1], shoot[1][0], shoot[1][1])

                while self.bullet_flying:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.bullet_flying = False
                            self.running = False
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.bullet_flying = False
                            self.running = False

                    # sprawdzanie czy nastąpiła kolizja pocisku z terenem
                    cords = self.terrain.mask.overlap(self.bullet.mask, (self.bullet.rect.x, self.bullet.rect.y))
                    if cords:
                        # jesli tak - zrób dziurę w miejscu uderzenia (promień - 20px)
                        self.terrain.make_hole(cords[0], cords[1], 20)
                        self.bullet_flying = False

                    # sprawdzanie czy pocisk trafił w przeciwnika
                    if self.bullet.rect.colliderect(self.idle_player.rect):
                        plr_hit = self.idle_player.mask.overlap(self.bullet.mask, (self.bullet.rect.x - self.idle_player.rect.x,
                                                                                   self.bullet.rect.y - self.idle_player.rect.y))
                        if plr_hit:
                            self.players.remove(self.idle_player)
                            self.bullet_flying = False

                    self.bullet.update()
                    self.screen.fill(defs.Colors.BACKGROUND_COLOR)  # background color
                    self.screen.blit(self.terrain.surface, (0, 0))
                    self.bullet.draw(self.screen)
                    self.refresh_screen()

                if not self.bullet_flying:
                    if len(self.players) < 2:
                        self.playing = False
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

    def info_to_screen(self, msg, x, y):
        """Wyświetla dany tekst z początkiem w danych współrzędnych"""
        text = defs.Assets.DEFAULT_FONT.render(msg, True, (0, 0, 0))
        self.screen.blit(text, [x, y])

    def refresh_screen(self):
        self.draw_players()
        pygame.display.flip()
