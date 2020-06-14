"""Test modułu game"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=line-too-long

import unittest
import pygame

import game
import defs
import terrain


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

        # potrzebne do poprawnej inicjalizacji graczy
        pygame.init()
        defs.Assets.load()

    def test_defaults(self):
        """Sprawdzenie poprawnej inicjalizacji obiektu"""
        self.assertTrue(self.game.running)
        self.assertFalse(self.game.playing)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.bullet_flying)

        self.assertIsNone(self.game.bullet)
        self.assertIsNone(self.game.current_player)
        self.assertIsNone(self.game.idle_player)

        self.assertIsInstance(self.game.terrain, terrain.Terrain)

    def test_new_game(self):
        """Sprawdzenie poprawnego rozpoczęcia gry"""
        self.game.new_game()
        self.assertIsNotNone(self.game.terrain.surface)     # sprawdzenie czy powstała powierzchnia terenu
        self.assertEqual(len(self.game.players), 2)     # sprawdzenie czy dodano dwóch graczy
        # sprawdzenie pozycji obu graczy
        self.assertEqual(self.game.players[0].x, defs.LEFT_PLR_X)
        self.assertEqual(self.game.players[1].x, defs.RIGHT_PLR_X)


if __name__ == "__main__":
    unittest.main()
