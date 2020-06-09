"""Zbiór stałych i obrazów"""

import pygame

SCR_WIDTH, SCR_HEIGHT = 1025, 600
CANNON_W, CANNON_H = 65, 46
ANGLE_MIN, ANGLE_MAX = 0, 60
POWER_MIN, POWER_MAX = 20, 100
LEFT, RIGHT = 0, 1
CANNON_IMG_COLS = 6
HOLE_RADIUS = 20

TIME_STEP = 0.012

TERRAIN_ROUGHNESS = 200

MAGIC_1 = 33
MAGIC_2 = 31
MAGIC_3 = -4

LEFT_PLR_X = 34  # współrzędna x lewego gracza
RIGHT_PLR_X = 906  # współrzędna x prawego gracza


class Colors:
    """Paleta kolorów"""
    BACKGROUND_COLOR = (186, 233, 255)
    TRANSPARENT_COLOR = (255, 255, 255)
    TERRAIN_COLOR = (50, 160, 80)
    BASE_COLOR = (107, 110, 108)


class Assets:
    """Przechowuje zasoby"""

    @staticmethod
    def load():
        Assets.DEFAULT_FONT = pygame.font.SysFont(None, 18)
        Assets.ICON = pygame.image.load("assets/icon.png")
        Assets.BULLET_IMG = pygame.image.load("assets/bullet.png")
        Assets.CANNON_IMAGE = {0: pygame.image.load("assets/cannon_left.png"), 1: pygame.image.load("assets/cannon_right.png")}
