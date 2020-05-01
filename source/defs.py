"""Zbiór stałych i obrazów"""

import pygame

SCR_WIDTH, SCR_HEIGHT = 1025, 600
CANNON_W, CANNON_H = 65, 46
ANGLE_MIN, ANGLE_MAX = 0, 60
POWER_MIN, POWER_MAX = 30, 300
LEFT, RIGHT = 0, 1
CANNON_IMG_COLS = 6
TRANSPARENT_COLOR = (0, 0, 0)
TERRAIN_COLOR = (50, 160, 80)
BASE_COLOR = (107, 110, 108)

icon = pygame.image.load("assets/icon.png")
cannon_image_left = pygame.image.load("assets/cannon/cannon_left.png")
cannon_image_right = pygame.image.load("assets/cannon/cannon_right.png")
