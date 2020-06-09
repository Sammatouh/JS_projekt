import pygame

import defs


class Bullet:
    def __init__(self, game, x, y, v_dx, v_dy):
        self.image = defs.Assets.BULLET_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_x = v_dx
        self.vel_y = v_dy
        self.start_x = x
        self.start_y = y
        self.time = 0
        self.game = game
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.time += defs.TIME_STEP
        dist_x = self.vel_x * self.time
        dist_y = (self.vel_y * self.time) + ((-4.9 * (self.time**2))/2)

        if (0 < self.rect.right or self.rect.left < defs.SCR_WIDTH) and self.rect.top < defs.SCR_HEIGHT:
            self.rect.centerx = round(dist_x + self.start_x)
            self.rect.centery = round(self.start_y - dist_y)
        else:
            self.game.bullet_flying = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
