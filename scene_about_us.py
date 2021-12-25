import pygame
from scene import Scene
import database


class Aboutus(Scene):
    # ***********************************************************************************************************
    def __init__(self, display):
        self.white = (255, 255, 255)
        self.x = 1024
        self.width = 1024
        self.hight = 800
        self.display_surface = pygame.display.set_mode((self.width, self.hight))
        self.image = pygame.image.load("images/about-us.png")
        # init an exit button
        self.blue = (0, 0, 128)
        self.grey = (127, 127, 127)
        self.red = (255, 0, 0)
        self.font = pygame.font.Font('fonts/defaultFont.ttf', 32)
        self.text = self.font.render(" Exit ", True, self.blue, self.grey)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x - 45, 20)
    # ***********************************************************************************************************
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # if clicked on exit------------------------
            elif self.textRect.collidepoint(mouse_pos):
                self.text = self.font.render(" Exit ", True, self.blue, self.red)
                self.textRect = self.text.get_rect()
                self.textRect.center = (self.x - 45, 20)
                if pygame.mouse.get_pressed()[0]:
                    return False  # Return userId so the system will go back to the user's menu screen
        return True

    # ***********************************************************************************************************
    def draw(self, display: pygame.Surface):
        self.display_surface.fill(self.white)
        # copying the image surface object
        # to the display surface object at
        # (0, 0) coordinate.
        self.display_surface.blit(self.image, (0, 0))
        # display exit button
        self.display_surface.blit(self.text, self.textRect)
        # pygame.display.update()
        pass
