import pygame

import defs


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, v_dx, v_dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = defs.bullet_img
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
        self.time += 0.015
        dist_x = self.vel_x * self.time
        dist_y = (self.vel_y * self.time) + ((-4.9 * (self.time**2))/2)

        if (0 < self.rect.right or self.rect.left < defs.SCR_WIDTH) and self.rect.top < defs.SCR_HEIGHT:
            self.rect.centerx = round(dist_x + self.start_x)
            self.rect.centery = round(self.start_y - dist_y)
        else:
            self.game.bullet_flying = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
# import pygame
# import math
#
# import defs
#
#
# class Bullet:
#     def __init__(self, x, y, radius, color):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.color = color
#
#     def draw(self, win):
#         pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
#         pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)
#
#     @staticmethod
#     def ballPath(startx, starty, power, ang, time):
#         angle = ang
#         velx = math.cos(angle) * power
#         vely = math.sin(angle) * power
#
#         distX = velx * time
#         distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)
#
#         newx = round(distX + startx)
#         newy = round(starty - distY)
#
#         return (newx, newy)