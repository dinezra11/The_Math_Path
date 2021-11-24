""" Base class for the scenes. This is only the template for all of the scenes of the system.
To program a new scene, simply create a new class and inherit from this base class.

Methods:
    1. initialize() - Initializes the scene's variables and components.
    2. update() - Updates the scene each given frames. (The FPS will be defined on the main python file)
    3. draw(display) - Draws the scene to the screen. (type(display) = pygame.display)
"""
import pygame


class Scene:
    def __init__(self, display):
        """ Initialize the scene.

        :param:     display -> The display where to draw the scene.
        """
        pass

    def update(self):
        """ Update the scene. """
        pass

    def draw(self, display: pygame.Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        pass
