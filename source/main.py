import pygame, math, defs, random
import numpy as np
from collections import deque

pygame.init()

# resolution
scr_width, scr_height = 1025, 600
res = (1025, 600)
# max and min barrel elevation
barrel_angle_max, barrel_angle_min = 60, 0
# max and min power
max_power, min_power = 300, 30

# game screen
screen = pygame.display.set_mode((scr_width, scr_height))
# game name
pygame.display.set_caption("Scorch")
# game icon
icon = pygame.image.load(r"assets\icon.png")
pygame.display.set_icon(icon)

cannon_image_left = pygame.image.load(r"assets\cannon\cannon_left.png")
cannon_image_right = pygame.image.load(r"assets\cannon\cannon_right.png")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)


class Player:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side
        self.barrel_angle = 0
        self.power = 150
        self.image_sx, self.image_sy = 0, 0
        if self.side == defs.left:
            self.image = cannon_image_left
        else:
            self.image = cannon_image_right

    def do_move(self):
        keys_state = pygame.key.get_pressed()
        if (keys_state[pygame.K_LEFT] and self.side == defs.left) or (keys_state[pygame.K_RIGHT] and self.side == defs.right):
            if self.barrel_angle < barrel_angle_max:
                self.barrel_angle = self.barrel_angle + 1
                self.draw(screen)
                # pygame.display.flip()
        elif (keys_state[pygame.K_RIGHT] and self.side == defs.left) or (keys_state[pygame.K_LEFT] and self.side == defs.right):
            if self.barrel_angle > barrel_angle_min:
                self.barrel_angle = self.barrel_angle - 1
                self.draw(screen)
                # pygame.display.flip()
        elif keys_state[pygame.K_UP]:
            if self.power < max_power:
                self.power = self.power + 1
                # pygame.display.flip()
        elif keys_state[pygame.K_DOWN]:
            if self.power > min_power:
                self.power = self.power - 1
                # pygame.display.flip()
        elif keys_state[pygame.K_SPACE]:
            return self.shoot()

    def shoot(self):
        print("SHOOT!")
        return 1

    def draw(self, surface):
        self.image_sx = (self.barrel_angle%defs.cannon_img_cols) * defs.cannon_w
        self.image_sy = (self.barrel_angle//defs.cannon_img_cols) * defs.cannon_h
        surface.blit(self.image, (self.x, self.y), pygame.Rect(self.image_sx, self.image_sy, defs.cannon_w, defs.cannon_h))


class Terrain:
    def __init__(self, width, height, roughness):
        self.width = width
        self.height = height
        self.roughness = roughness
        self.surface = None

        self.heights = [0]*self.width
        self.q = deque()
        self.transparent_color = None
        self.ground_color = None
        self.base_color = None

    def generate(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(defs.transparent_color, pygame.RLEACCEL)
        self.surface.set_at((0, 0), defs.terrain_color)
        self.surface.set_at((1, 0), defs.transparent_color)
        self.surface.set_at((2, 0), defs.base_color)
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
        min = np.min(data)
        max = np.max(data)
        range = max - min
        new_range = new_upper_bound - new_lower_bound

        return [(a - min) * new_range // range + new_lower_bound for a in data]

    # dodawanie płaskiego terenu jako osobna metoda?
    def add_flat(self):
        pass


def info_to_screen(msg, x, y):
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, [x, y])
    # pygame.display.flip()


def draw_players(given_players):
    for player in given_players:
        player.draw(screen)
        # pygame.display.flip()


terrain = Terrain(scr_width, scr_height, 200)
terrain.generate()
players = [Player(34, terrain.heights[34]-46, defs.left), Player(906, terrain.heights[921]-46, defs.right)]
current_player = players[0]

# main loop
running = True
while running:
    clock.tick(30)

    screen.fill((186, 233, 255))  # background color
    screen.blit(terrain.surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    shoot = current_player.do_move()
    if shoot:
        pygame.time.delay(600)
        if current_player == players[0]:
            current_player = players[1]
        else:
            current_player = players[0]

        if len(players) <= 1:
            game_over = True
    draw_players(players)
    info_to_screen("Angle: " + str(current_player.barrel_angle), current_player.x, 10)
    info_to_screen("Power: " + str(current_player.power), current_player.x, 22)

    pygame.display.flip()
