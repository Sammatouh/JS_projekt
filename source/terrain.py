"""Moduł odpowiedzialny za generację terenu"""
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-function-args
# pylint: disable=c-extension-no-member
# pylint: disable=no-member
# pylint: disable=line-too-long

from collections import deque
import math
import random

import numpy as np
import pygame

import defs


class Terrain:
    """Klasa reprezentująca teren"""
    def __init__(self, game, roughness):
        self.width = game.width
        self.height = game.height
        self.roughness = roughness
        self.surface = None

        self.heights = [0]*self.width
        self.q = deque()
        self.transparent_color = None
        self.ground_color = None
        self.base_color = None

        self.mask = None

    def generate(self):
        """Metoda generująca teren za pomocą algorytmu midpoint displacement"""
        self.surface = pygame.Surface((self.width, self.height))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(defs.Colors.TRANSPARENT_COLOR, pygame.RLEACCEL)
        self.surface.set_at((0, 0), defs.Colors.TERRAIN_COLOR)
        self.surface.set_at((1, 0), defs.Colors.TRANSPARENT_COLOR)
        self.surface.set_at((2, 0), defs.Colors.BASE_COLOR)
        pixels = pygame.surfarray.pixels2d(self.surface)
        self.ground_color = pixels[0, 0]
        self.transparent_color = pixels[1, 0]
        self.base_color = pixels[2, 0]
        self.heights[0] = random.randint(0, self.height-(self.height//7))
        self.heights[self.width - 1] = random.randint(0, self.height-(self.height//7))
        self.q.append((0, self.width - 1, self.roughness))

        while len(self.q) != 0:
            left, right, randomness = self.q.popleft()
            center = (left + right + 1)//2
            self.heights[center] = (self.heights[left] + self.heights[right])//2
            self.heights[center] = self.heights[center] + random.randint(-randomness, randomness)

            if right - left > 2:
                self.q.append((left, center, math.floor(randomness//2)))
                self.q.append((center, right, math.floor(randomness)//2))

        self.heights = self.normalize(self.heights, self.height//7, self.height - (self.height//7))

        for x in range(self.width):
            pixels[x, 0:self.heights[x]] = self.transparent_color
            pixels[x, self.heights[x]:self.height] = self.ground_color

        # płaski kawałek terenu dla graczy
        if self.heights[defs.LEFT_PLR_X] < self.heights[defs.LEFT_PLR_X + defs.CANNON_W]:
            x_1 = defs.LEFT_PLR_X
        else:
            x_1 = defs.LEFT_PLR_X + defs.CANNON_W
        if self.heights[defs.RIGHT_PLR_X] < self.heights[defs.RIGHT_PLR_X + defs.CANNON_W]:
            x_2 = defs.RIGHT_PLR_X
        else:
            x_2 = defs.RIGHT_PLR_X + defs.CANNON_W
        for x in range(defs.LEFT_PLR_X, defs.LEFT_PLR_X + defs.CANNON_W):
            pixels[x, 0:self.heights[x_1]] = self.transparent_color
            pixels[x, self.heights[x_1]:self.heights[x]] = self.base_color
            self.heights[x] = self.heights[x_1]
        for x in range(defs.RIGHT_PLR_X, defs.RIGHT_PLR_X + defs.CANNON_W):
            pixels[x, 0:self.heights[x_2]] = self.transparent_color
            pixels[x, self.heights[x_2]:self.heights[x]] = self.base_color
            self.heights[x] = self.heights[x_2]

        self.mask = pygame.mask.from_surface(self.surface)

    def normalize(self, data, new_lower_bound, new_upper_bound):
        """Metoda ograniczająca wysokości terenu"""
        my_min = np.min(data)
        my_max = np.max(data)
        my_range = my_max - my_min
        new_range = new_upper_bound - new_lower_bound

        return [(a - my_min) * new_range // my_range + new_lower_bound for a in data]

    def make_hole(self, x, y, rad):
        """Tworzy dziurę w miejscu uderzenia pocisku"""
        pixels = pygame.surfarray.pixels2d(self.surface)
        w, h = pixels.shape
        cl, cr, ct, cb = x-rad, x+rad, y-rad, y+rad
        if cl < 0:
            cl = 0
        if cr >= w:
            cr = w-1
        if ct < 0:
            ct = 0
        if cb >= h:
            cb = h-1
        for i in range(cl, cr):
            for j in range(ct, cb):
                if((i-x)**2 + (j-y)**2) < rad**2:
                    pixels[i, j] = self.transparent_color

        self.mask = pygame.mask.from_surface(self.surface)
