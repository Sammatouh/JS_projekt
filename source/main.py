"""Moduł główny programu"""
# pylint: disable=no-member

import pygame

import defs
from game import Game


def main():
    """Funkcja uruchamiająca grę"""
    pygame.init()
    defs.Assets.load()

    pygame.display.set_caption(defs.TITLE)
    pygame.display.set_icon(defs.Assets.ICON)

    game = Game()

    while game.running:
        game.start_screen()
        game.new_game()
        game.game_loop()
        game.go_screen()


if __name__ == "__main__":
    main()
