from game import *


def main():
    pygame.init()
    pygame.display.set_caption("Scorch")
    pygame.display.set_icon(defs.icon)

    clock = pygame.time.Clock()
    clock.tick(30)
    font = pygame.font.SysFont(None, 18)
    game = Game(defs.SCR_WIDTH, defs.SCR_HEIGHT, clock, font)

    game.game_loop()


if __name__ == "__main__":
    main()
