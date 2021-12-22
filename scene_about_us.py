import pygame
from scene import Scene
import database


class Aboutus(Scene):
    # ***********************************************************************************************************
    def __init__(self, display):
        self.white = (255, 255, 255)
        self.width = 1024
        self.hight = 800
        self.display_surface = pygame.display.set_mode((self.width, self.hight))
        self.image = pygame.image.load("images/about-us.png")

    # ***********************************************************************************************************
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    # ***********************************************************************************************************
    def draw(self, display: pygame.Surface):
        self.display_surface.fill(self.white)
        # copying the image surface object
        # to the display surface object at
        # (0, 0) coordinate.
        self.display_surface.blit(self.image, (0, 0))
       # pygame.display.update()

        pass






