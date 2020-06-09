"""Moduł główny programu"""

from game import *


def main():
    pygame.init()
    defs.Assets.load()

    pygame.display.set_caption("Scorch-Artillery-Game")
    pygame.display.set_icon(defs.Assets.ICON)

    clock = pygame.time.Clock()
    clock.tick(30)
    game = Game(defs.SCR_WIDTH, defs.SCR_HEIGHT, clock)

    while game.running:
        game.new_game()
        game.game_loop()


if __name__ == "__main__":
    main()
