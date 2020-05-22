"""Zbiór stałych i obrazów"""

import pygame

SCR_WIDTH, SCR_HEIGHT = 1025, 600
CANNON_W, CANNON_H = 65, 46
ANGLE_MIN, ANGLE_MAX = 0, 60
POWER_MIN, POWER_MAX = 20, 100
LEFT, RIGHT = 0, 1
CANNON_IMG_COLS = 6

TERRAIN_ROUGHNESS = 200

BACKGROUND_COLOR = (186, 233, 255)
TRANSPARENT_COLOR = (255, 255, 255)
TERRAIN_COLOR = (50, 160, 80)
BASE_COLOR = (107, 110, 108)

LEFT_PLR_X = 34  # współrzędna x lewego gracza
RIGHT_PLR_X = 906  # współrzędna x prawego gracza

icon = pygame.image.load("assets/icon.png")
bullet_img = pygame.image.load("assets/bullet.png")
cannon_image = {0: pygame.image.load("assets/cannon_left.png"), 1: pygame.image.load("assets/cannon_right.png")}
