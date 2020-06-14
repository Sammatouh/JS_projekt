"""Test modułu player"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=line-too-long

import unittest
import pygame

import player
import game
import defs


class PlayerTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        defs.Assets.load()
        self.game = game.Game()
        self.player = player.Player(self.game, 50, 420, defs.LEFT)

    def test_defaults(self):
        self.assertIsInstance(self.player.game, game.Game)
        self.assertEqual(self.player.x, 50)
        self.assertEqual(self.player.y, 420)
        self.assertEqual(self.player.side, 1)
        self.assertEqual(self.player.barrel_angle, 0)
        self.assertEqual(self.player.power, 40)
        self.assertIsInstance(self.player.rect, pygame.Rect)
        self.assertIs(self.player.image, defs.Assets.CANNON_IMAGE[1])
        self.assertIsInstance(self.player.mask, pygame.mask.MaskType)


if __name__ == "__main__":
    unittest.main()
