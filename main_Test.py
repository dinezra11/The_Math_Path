""" Test file for 'uiComponents.py'
'uiComponents.py' contains almost all of the components and elements of the systems.
Therefore, testing this file is extremely important and cover up almost all of the system's functionality. """
import unittest
import pygame.tests


class TestMain(unittest.TestCase):
    def test_Game(self):
        pygame.tests.test_utils.test()  # Perform the general unittest for PyGame


if __name__ == '__main__':
    unittest.main()
