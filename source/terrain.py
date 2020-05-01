"""Moduł odpowiedzialny za generację terenu"""

from collections import deque
import math
import random

import numpy as np
import pygame

import defs


class Terrain:
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

    def generate(self):
        """Metoda generująca teren za pomocą algorytmu midpoint displacement"""

        self.surface = pygame.Surface((self.width, self.height))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(defs.TRANSPARENT_COLOR, pygame.RLEACCEL)
        self.surface.set_at((0, 0), defs.TERRAIN_COLOR)
        self.surface.set_at((1, 0), defs.TRANSPARENT_COLOR)
        self.surface.set_at((2, 0), defs.BASE_COLOR)
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

        # płaski kawałek terenu dla graczy  !wymaga poprawki
        if self.heights[34] < self.heights[84]:
            x_1 = 34
        else:
            x_1 = 84
        if self.heights[921] < self.heights[971]:
            x_2 = 921
        else:
            x_2 = 971
        for x in range(34, 84):
            pixels[x, 0:self.heights[x_1]] = self.transparent_color
            pixels[x, self.heights[x_1]:self.heights[x]] = self.base_color
            self.heights[x] = self.heights[x_1]
        for x in range(921, 971):
            pixels[x, 0:self.heights[x_2]] = self.transparent_color
            pixels[x, self.heights[x_2]:self.heights[x]] = self.base_color
            self.heights[x] = self.heights[x_2]

    def normalize(self, data, new_lower_bound, new_upper_bound):
        """Metoda ograniczająca wysokości terenu"""

        min = np.min(data)
        max = np.max(data)
        range = max - min
        new_range = new_upper_bound - new_lower_bound

        return [(a - min) * new_range // range + new_lower_bound for a in data]

    # dodawanie płaskiego terenu jako osobna metoda?
    def add_flat(self):
        pass
