"""Moduł zawierający definicję klasy gracza oraz kalsy pocisku"""
import pygame
import math

import defs


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, side):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.side = side
        self.barrel_angle = 0
        self.power = 40
        self.image_sx, self.image_sy = 0, 0
        self.rect = pygame.Rect(x, y, defs.CANNON_W, defs.CANNON_H)
        self.image = defs.cannon_image[self.side]
        self.mask = pygame.mask.from_surface(self.image)

    def do_move(self):
        """Metoda odpowiedzialna za rejestrację ruchu gracza"""
        keys_state = pygame.key.get_pressed()
        if (keys_state[pygame.K_LEFT] and self.side == defs.LEFT) or (
                keys_state[pygame.K_RIGHT] and self.side == defs.RIGHT):
            if self.barrel_angle < defs.ANGLE_MAX:
                self.barrel_angle += 1
        if (keys_state[pygame.K_RIGHT] and self.side == defs.LEFT) or (
                keys_state[pygame.K_LEFT] and self.side == defs.RIGHT):
            if self.barrel_angle > defs.ANGLE_MIN:
                self.barrel_angle -= 1
        if keys_state[pygame.K_UP]:
            if self.power < defs.POWER_MAX:
                self.power += 1
        if keys_state[pygame.K_DOWN]:
            if self.power > defs.POWER_MIN:
                self.power -= 1
        if keys_state[pygame.K_SPACE]:
            return self.shoot()

    def shoot(self):
        """Metoda odpowiedzialna za obliczenie parametrów strzału"""
        radian = self.barrel_angle * math.pi / 180
        v_dy = math.sin(radian) * self.power
        sx, sy, v_dx = 0, 0, 0
        if self.side == defs.LEFT:
            v_dx = math.cos(radian) * self.power
            sx = (64 - 31) * math.cos(radian) + (27 - 31) * math.sin(radian) + 31 + self.rect.left
            sy = (27 - 31) * math.cos(radian) - (64 - 31) * math.sin(radian) + 31 + self.rect.top
        elif self.side == defs.RIGHT:
            v_dx = -math.cos(radian) * self.power
            sx = (0 - 34) * math.cos(radian) - (27 - 31) * math.sin(radian) + 34 + self.rect.left
            sy = (27 - 31) * math.cos(radian) + (0 - 34) * math.sin(radian) + 31 + self.rect.top
        # print("SHOOT!")
        # print(sx, sy, v_dx, v_dy)
        return (sx, sy), (v_dx, v_dy) # 1. krotka - początkowe położenie pocisku; 2. krotka - prędkości według osi X i Y

    def draw(self, surface):
        """Metoda rysująca gracza na ekranie"""
        self.image_sx = (self.barrel_angle % defs.CANNON_IMG_COLS) * defs.CANNON_W
        self.image_sy = (self.barrel_angle // defs.CANNON_IMG_COLS) * defs.CANNON_H
        plr_surface = pygame.Surface((defs.CANNON_W, defs.CANNON_H))
        plr_surface.fill(defs.TRANSPARENT_COLOR)
        plr_surface.set_colorkey(defs.TRANSPARENT_COLOR)
        plr_surface.blit(self.image, (0, 0),
                     pygame.Rect(self.image_sx, self.image_sy, defs.CANNON_W, defs.CANNON_H))

        surface.blit(plr_surface, (self.x, self.y))
        # self.mask = pygame.mask.from_surface(plr_surface)

        if self.game.current_player == self:
            self.game.info_to_screen("Angle: {}".format(self.barrel_angle), self.x, 10)
            self.game.info_to_screen("Power: {}".format(self.power), self.x, 22)
