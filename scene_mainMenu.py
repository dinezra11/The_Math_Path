from pygame import Surface
from scene import Scene


class MainMenu(Scene):
    def __init__(self, display, userId: str):
        """ Initialize the scene.

        :param display:             The display where to draw the scene.
        :param userId:              User's id. (string)
        """
        super().__init__(display)
        pass

    def update(self):
        """ Update the scene. """

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        pass