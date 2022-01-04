""" Test file for general PyGame'
This test script perform a general test for the PyGame engine. It uses build-in tests to make sure all of the
engine's components are legit and valid. """
import unittest
import pygame.tests


class TestMain(unittest.TestCase):
    def test_Game(self):
        pygame.tests.test_utils.test()  # Perform the general unittest for PyGame


if __name__ == '__main__':
    unittest.main()
