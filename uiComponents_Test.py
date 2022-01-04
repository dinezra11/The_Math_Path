""" Test file for 'uiComponents.py'
'uiComponents.py' contains almost all of the components and elements of the systems.
Therefore, testing this file is extremely important and cover up almost all of the system's functionality. """
import unittest
import pygame
import uiComponents


class TestUiComponents(unittest.TestCase):
    def test_button(self):
        """ Test script for 'Button' component.

        The script will open a window with a buttons.
        The buttons should normally be red.
        When mouse is hover a button - the button should be green.
        When you click on the button - a click sound should be heard.

        If anything of the above doesn't work - the test is considered as failed. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((200, 200))
        gameClock = pygame.time.Clock()

        # Creating the Button
        btnTest = [uiComponents.Button((10, 10, 80, 80), ((255, 0, 0), (0, 255, 0)), "", "fonts/defaultFont.ttf",
                                       12, lambda: True),
                   uiComponents.Button((100, 10, 80, 80), ((255, 0, 0), (0, 255, 0)), "", "fonts/defaultFont.ttf",
                                       12, lambda: True),
                   uiComponents.Button((10, 100, 80, 80), ((255, 0, 0), (0, 255, 0)), "", "fonts/defaultFont.ttf",
                                       12, lambda: True),
                   uiComponents.Button((100, 100, 80, 80), ((255, 0, 0), (0, 255, 0)), "", "fonts/defaultFont.ttf",
                                       12, lambda: True)
                   ]
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            for btn in btnTest:
                btn.update()
                btn.draw(gameDisplay)

            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()

    def test_imageButton(self):
        """ Test script for 'ImageButton' component.

        The script will open a window with an Image Button.
        The button should make a sound on click, and be a little bit transparent on hover.

        If anything of the above doesn't work - the test is considered as failed. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((200, 200))
        gameClock = pygame.time.Clock()

        # Creating the Button
        btnTest = uiComponents.ImageButton((10, 10, 80, 80), "images/Settings/icon.png", lambda: None)
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            gameDisplay.fill((0, 0, 0))
            btnTest.update()
            btnTest.draw(gameDisplay)

            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()

    def test_cycleButton(self):
        """ Test script for 'CycleButton' component.

        The script will open a window with a cycle-button.
        The button should switch option when clicked.

        If it doesn't work - the test is considered as failed. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((200, 200))
        gameClock = pygame.time.Clock()

        # Creating the Button
        options = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        btnTest = uiComponents.CycleButton((10, 10, 80, 80), ((255, 0, 0), (0, 255, 0)), options,
                                           "fonts/defaultFont.ttf", 12)
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            btnTest.update()
            btnTest.draw(gameDisplay)

            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()

    def test_errorText(self):
        """ Test script for 'ErrorText' component.

        The script will open an empty window.
        Each time the user click on the mouse, an error message should pop.

        If it doesn't work - the test is considered as failed. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((200, 200))
        gameClock = pygame.time.Clock()

        # Creating the ErrorText
        txtTest = uiComponents.ErrorText((100, 100), 12, "fonts/defaultFont.ttf")
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            if pygame.mouse.get_pressed()[0] is True:
                txtTest.pop("Button clicked, error popped! :)", 100)  # Pop the error

            gameDisplay.fill((0, 0, 0))
            txtTest.update()
            txtTest.draw(gameDisplay)

            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()

    def test_textInput(self):
        """ Test script for 'TextInput' component.

        The script will open a window with a text box.
        The user should be able to toggle the text box on click, and write characters into it.
        If the text box isn't toggled, and the user press the keyboard - nothing should happen.

        Total of 3 text boxes. The 3rd one is initialized as SECRET. (For hiding passwords)

        If it doesn't work - the test is considered as failed. """
        # Initialize PyGame and the display:
        pygame.init()
        gameDisplay = pygame.display.set_mode((250, 250))
        gameClock = pygame.time.Clock()

        # Creating the ErrorText
        txtTest = [uiComponents.TextInput((10, 20), 12, "fonts/defaultFont.ttf"),
                   uiComponents.TextInput((10, 120), 12, "fonts/defaultFont.ttf"),
                   uiComponents.TextInput((10, 200), 12, "fonts/defaultFont.ttf", secret=True)
                   ]
        loop = True

        while loop:
            # Keyboard Event check:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.KEYDOWN:
                    for txt in txtTest:
                        txt.updateText(event)

            gameDisplay.fill((0, 0, 0))
            for txt in txtTest:
                txt.update()
                txt.draw(gameDisplay)

            pygame.display.update()
            gameClock.tick(30)  # FPS

        pygame.quit()


if __name__ == '__main__':
    unittest.main()
