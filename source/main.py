"""Moduł główny programu"""

from game import *


def main():
    pygame.init()
    defs.Assets.load()

    pygame.display.set_caption(defs.TITLE)
    pygame.display.set_icon(defs.Assets.ICON)

    clock = pygame.time.Clock()

    game = Game(defs.SCR_WIDTH, defs.SCR_HEIGHT, clock)

    while game.running:
        game.start_screen()
        game.new_game()
        game.game_loop()
        game.go_screen()


if __name__ == "__main__":
    main()
