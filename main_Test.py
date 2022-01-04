""" Test file for general 'PyGame'
This test script perform a general test for the PyGame engine. It uses build-in tests to make sure all of the
engine's components are legit and valid. """
import unittest
import pygame
import pygame.tests


class TestMain(unittest.TestCase):
    def test_Game(self):
        """ General unittest for PyGame Engine. """
        pygame.tests.test_utils.test()  # Perform the general unittest for PyGame

    def test_fillColor(self):
        """ Test script for background fill color.
        Click on the window's screen to change color. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((250, 250))
        gameClock = pygame.time.Clock()
        color = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 0), (0, 100, 100), (50, 0, 80), (0, 0, 0)
                 ]
        index = 0
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    index += 1

            if index == len(color) - 1:
                loop = False

            gameDisplay.fill(color[index])
            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()


if __name__ == '__main__':
    unittest.main()
