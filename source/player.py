"""Moduł zawierający definicję klasy gracza"""

import pygame

import game
import defs


class Player:
    def __init__(self, game, x, y, side):
        self.game = game
        self.x = x
        self.y = y
        self.side = side
        self.barrel_angle = 0
        self.power = 150
        self.image_sx, self.image_sy = 0, 0
        if self.side == defs.LEFT:
            self.image = defs.cannon_image_left
        else:
            self.image = defs.cannon_image_right

    def do_move(self):
        """Metoda odpowiedzialna za rejestrację ruchu gracza"""

        keys_state = pygame.key.get_pressed()
        if (keys_state[pygame.K_LEFT] and self.side == defs.LEFT) or (keys_state[pygame.K_RIGHT] and self.side == defs.RIGHT):
            if self.barrel_angle < defs.ANGLE_MAX:
                self.barrel_angle = self.barrel_angle + 1
                self.draw(self.game.screen)
                # pygame.display.flip()
        elif (keys_state[pygame.K_RIGHT] and self.side == defs.LEFT) or (keys_state[pygame.K_LEFT] and self.side == defs.RIGHT):
            if self.barrel_angle > defs.ANGLE_MIN:
                self.barrel_angle = self.barrel_angle - 1
                self.draw(self.game.screen)
                # pygame.display.flip()
        elif keys_state[pygame.K_UP]:
            if self.power < defs.POWER_MAX:
                self.power = self.power + 1
                # pygame.display.flip()
        elif keys_state[pygame.K_DOWN]:
            if self.power > defs.POWER_MIN:
                self.power = self.power - 1
                # pygame.display.flip()
        elif keys_state[pygame.K_SPACE]:
            return self.shoot()

    def shoot(self):
        """Metoda odpowiedzialna za wykonanie strzału"""

        print("SHOOT!")
        return 1

    def draw(self, surface):
        """Metoda rysująca gracza na ekranie"""

        self.image_sx = (self.barrel_angle%defs.CANNON_IMG_COLS) * defs.CANNON_W
        self.image_sy = (self.barrel_angle//defs.CANNON_IMG_COLS) * defs.CANNON_H
        surface.blit(self.image, (self.x, self.y), pygame.Rect(self.image_sx, self.image_sy, defs.CANNON_W, defs.CANNON_H))
