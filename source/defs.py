"""Zbiór stałych i obrazów"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-function-docstring

import pygame

TITLE = "Scorch Artillery Game"

SCR_WIDTH, SCR_HEIGHT = 1025, 600
CANNON_W, CANNON_H = 65, 46
ANGLE_MIN, ANGLE_MAX = 0, 60
POWER_MIN, POWER_MAX = 20, 100
LEFT, RIGHT = 1, 2
CANNON_IMG_COLS = 6
HOLE_RADIUS = 20
FPS = 30

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
    BLACK = (0, 0, 0)
    LIGHT_GREY = (130, 130, 130)


class Assets:
    """Przechowuje zasoby"""

    @staticmethod
    def load():
        Assets.FONTS = {0.15: pygame.font.Font("assets/ArconRegular.otf", 15),
                        1.90: pygame.font.Font("assets/ExplodeFont.ttf", 90),
                        2.80: pygame.font.Font("assets/PAMPARAY.otf", 80),
                        2.50: pygame.font.Font("assets/PAMPARAY.otf", 50)}
        Assets.ICON = pygame.image.load("assets/icon.png")
        Assets.BULLET_IMG = pygame.image.load("assets/bullet.png")
        Assets.CANNON_IMAGE = {1: pygame.image.load("assets/cannon_left.png"),
                               2: pygame.image.load("assets/cannon_right.png")}
