import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text
import database

# Scene's Constants:
BACKGROUND_COLOR = (102, 51, 0)
HEADER_COLOR = (246, 195, 36)
FOOTER_COLOR = (96, 96, 96)

WHITE = (255, 255, 255)


class MainMenu(Scene):
    def __init__(self, display: Surface, userId: str):
        """ Initialize the scene.

        :param display:             The display where to draw the scene.
        :param userId:              User's id. (string)
        """
        super().__init__(display)
        self.userObj = database.getUser(userId)  # Get the relevant user's details from the database

        title = "Welcome {0} {1}".format(self.userObj[1]["name"], self.userObj[1]["last"])
        self.titleText = Text((display.get_size()[0] / 2, 20), WHITE, title, 24, "fonts/defaultFont.ttf")

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill(BACKGROUND_COLOR)
        display.fill(HEADER_COLOR, (0, 0, display.get_size()[0], 45))
        display.fill(FOOTER_COLOR, (0, display.get_size()[1] - 45, display.get_size()[0], 45))
        self.titleText.draw(display)
