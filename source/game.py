"""Moduł odpowiadajacy za wszystkie zdarzenia i czynności wykonywane podczas gry"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=line-too-long

import pygame

import bullet
import defs
import player
import terrain


class Game:
    """Klasa główna gry"""
    def __init__(self):
        self.running = True
        self.playing = False
        self.game_over = False
        self.bullet_flying = False

        self.bullet = None

        self.width = defs.SCR_WIDTH
        self.height = defs.SCR_HEIGHT

        self.screen = pygame.display.set_mode((defs.SCR_WIDTH, defs.SCR_HEIGHT))
        self.clock = pygame.time.Clock()

        self.terrain = terrain.Terrain(self, defs.TERRAIN_ROUGHNESS)

        self.players = []
        self.current_player = None
        self.idle_player = None

    def start_screen(self):
        """Pętla ekranu startowego"""
        waiting = True
        while (not self.playing) and waiting:
            self.clock.tick(defs.FPS)
            self.screen.fill(defs.Colors.BACKGROUND_COLOR)
            self.fixed_info_to_screen(defs.TITLE, defs.Colors.BLACK, 1.90, self.width//2, 100)
            self.fixed_info_to_screen("Press P to play", defs.Colors.LIGHT_GREY, 2.50, self.width//2, self.height//2)
            self.fixed_info_to_screen("Controls:", defs.Colors.BLACK, 0.15, self.width//2, 450)
            self.fixed_info_to_screen("UP arrow / DOWN arrow   -   power", defs.Colors.BLACK, 0.15, self.width//2, 470)
            self.fixed_info_to_screen("LEFT arrow / RIGHT arrow   -   angle", defs.Colors.BLACK, 0.15, self.width // 2, 490)
            self.fixed_info_to_screen("Press ESC to quit", defs.Colors.LIGHT_GREY, 0.15, self.width // 2, 550)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    waiting = False
                    self.playing = True

            pygame.display.flip()

    def new_game(self):
        """Rozpoczęcie nowej gry"""
        self.terrain.generate()

        self.players = [player.Player(self, defs.LEFT_PLR_X, self.terrain.heights[defs.LEFT_PLR_X] - defs.CANNON_H, defs.LEFT),
                        player.Player(self, defs.RIGHT_PLR_X, self.terrain.heights[defs.RIGHT_PLR_X] - defs.CANNON_H, defs.RIGHT)]
        self.current_player = self.players[0]
        self.idle_player = self.players[1]

    def game_loop(self):
        """Pętla główna gry"""
        while self.playing:
            self.clock.tick(defs.FPS)

            self.screen.fill(defs.Colors.BACKGROUND_COLOR)
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
                        self.terrain.make_hole(cords[0], cords[1], defs.HOLE_RADIUS)
                        self.bullet_flying = False

                    # sprawdzanie czy pocisk trafił w przeciwnika
                    if self.bullet.rect.colliderect(self.idle_player.rect):
                        plr_hit = self.idle_player.mask.overlap(self.bullet.mask, (self.bullet.rect.x - self.idle_player.rect.x,
                                                                                   self.bullet.rect.y - self.idle_player.rect.y))
                        if plr_hit:
                            self.players.remove(self.idle_player)
                            self.bullet_flying = False

                    self.bullet.update()
                    self.screen.fill(defs.Colors.BACKGROUND_COLOR)
                    self.screen.blit(self.terrain.surface, (0, 0))
                    self.bullet.draw(self.screen)
                    self.refresh_screen()

                if not self.bullet_flying:
                    if len(self.players) < 2:
                        self.playing = False
                        self.game_over = True
                        break

                    if self.current_player == self.players[0]:
                        self.current_player = self.players[1]
                        self.idle_player = self.players[0]
                    else:
                        self.current_player = self.players[0]
                        self.idle_player = self.players[1]

            self.refresh_screen()

    def go_screen(self):
        """Pętla ekranu końcowego"""
        waiting = True
        while self.game_over and waiting:
            self.screen.fill(defs.Colors.BACKGROUND_COLOR)
            self.fixed_info_to_screen("Player  " + str(self.current_player.side) + "  wins", defs.Colors.BLACK, 2.80, self.width//2, 100)
            self.fixed_info_to_screen("Press N to play again", defs.Colors.LIGHT_GREY, 2.50, self.width // 2, self.height // 2)
            self.fixed_info_to_screen("Press ESC to quit", defs.Colors.LIGHT_GREY, 0.15, self.width // 2, 490)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    break

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    waiting = False
                    self.playing = True

            pygame.display.flip()

    def draw_players(self):
        """Rysuje graczy na ekranie"""
        for plr in self.players:
            plr.draw(self.screen)

    def info_to_screen(self, msg, color, font, x, y):
        """Wyświetla dany tekst z początkiem w danych współrzędnych"""
        text = defs.Assets.FONTS[font].render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.x, text_rect.y = (x, y)
        self.screen.blit(text, text_rect)

    def fixed_info_to_screen(self, msg, color, font, x, y):
        """Wyświetla dany tekst ze środkiem w danych współrzędnych"""
        text = defs.Assets.FONTS[font].render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text, text_rect)

    def refresh_screen(self):
        """Odświeżanie ekranu"""
        self.draw_players()
        pygame.display.flip()
