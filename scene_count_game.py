""" Base class for the scenes. This is only the template for all of the scenes of the system.
To program a new scene, simply create a new class and inherit from this base class.

Methods:
    1. initialize() - Initializes the scene's variables and components.
    2. update() - Updates the scene each given frames. (The FPS will be defined on the main python file)
    3. draw(display) - Draws the scene to the screen. (type(display) = pygame.display)
"""
import pygame
from scene import Scene
import random



class count_game(Scene):

    def __init__(self, display):
        super().__init__(display)
        self.background_surf = pygame.image.load('count_numbers/background.jpg')

        self.mouse_pos = pygame.mouse.get_pos()

        self.title_font = pygame.font.Font(None, 100)
        self.title_surface = self.title_font.render('Counting Game', True, 'Black')
        self.title_rect = self.title_surface.get_rect(midtop=(512, 50))

        self.explanation_font = pygame.font.Font(None, 30)
        self.explanation_surface = self.explanation_font.render(
            'In this game you have to count the objects and write the right amount', True, 'Black')
        self.explanation_rect = self.explanation_surface.get_rect(midtop=(512, 150))

        self.start_font = pygame.font.Font(None, 50)
        self.start_surface = self.start_font.render('START GAME', True, 'Black')
        self.start_rect = self.start_surface.get_rect(midtop=(512, 300))

        self.win_font = pygame.font.Font(None, 40)
        self.win_surface = self.win_font.render('YOU ARE RIGHT! PRESS SPACE FOR NEXT LEVEL', True, 'Black')
        self.win_rect = self.win_surface.get_rect(midtop=(512, 300))

        self.try_again_font = pygame.font.Font(None, 50)
        self.try_again_surface = self.try_again_font.render('THATS WRONG ANSWER! SPACE TO TRY AGAIN!', True, 'Black')
        self.try_again_rect = self.start_surface.get_rect(midtop=(200, 300))

        self.eagle_surface = pygame.image.load('count_numbers/eagle.png')
        self.eagle_surface = pygame.transform.scale(self.eagle_surface, (100, 100))

        self.one_surface = pygame.image.load('count_numbers/1.png')
        self.one_surface = pygame.transform.scale(self.one_surface, (100, 100))
        self.two_surface = pygame.image.load('count_numbers/2.png')
        self.two_surface = pygame.transform.scale(self.two_surface, (100, 100))
        self.three_surface = pygame.image.load('count_numbers/3.png')
        self.three_surface = pygame.transform.scale(self.three_surface, (100, 100))
        self.four_surface = pygame.image.load('count_numbers/4.png')
        self.four_surface = pygame.transform.scale(self.four_surface, (100, 100))
        self.five_surface = pygame.image.load('count_numbers/5.png')
        self.five_surface = pygame.transform.scale(self.five_surface, (100, 100))
        self.six_surface = pygame.image.load('count_numbers/6.png')
        self.six_surface = pygame.transform.scale(self.six_surface, (100, 100))
        self.seven_surface = pygame.image.load('count_numbers/7.png')
        self.seven_surface = pygame.transform.scale(self.seven_surface, (100, 100))
        self.eight_surface = pygame.image.load('count_numbers/8.png')
        self.eight_surface = pygame.transform.scale(self.eight_surface, (100, 100))
        self.nine_surface = pygame.image.load('count_numbers/9.png')
        self.nine_surface = pygame.transform.scale(self.nine_surface, (100, 100))
        self.zero_surface = pygame.image.load('count_numbers/0.png')
        self.zero_surface = pygame.transform.scale(self.zero_surface, (100, 100))

        self.start_state = False
        self.current_level = 1
        self.next_level = False
        self.tryAgain = False
        self.clickable = True


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(event.pos):
                    self.start_state = True

        return True

    def draw(self, display: pygame.Surface):
        if not self.start_state:
            self.draw_start_screen(display)
        elif self.next_level:
            self.display_win(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.next_level = False
        elif self.tryAgain:
            self.display_try_again(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.tryAgain = False
        else:
            self.current_level_function(display)

    def draw_level_one(self, display: pygame.Surface):

        display.blit(self.background_surf, (0, 0))
        one_explain = pygame.font.Font(None, 50)
        one_explain_surface = one_explain.render('How many eagles can you count?', True, 'Black')
        one_explain_rec = one_explain_surface.get_rect(midtop=(512, 150))
        display.blit(one_explain_surface, one_explain_rec)
        for i in range(100, 900, 225):
            display.blit(self.eagle_surface, (i, 300))
        display.blit(self.four_surface, (200, 600))
        display.blit(self.five_surface, (450, 600))
        display.blit(self.seven_surface, (800, 600))
        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.four_surface.get_size()
            mousePos = pygame.mouse.get_pos()
            MouseOn = 200 < mousePos[0] < (200 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))
            mouseOff = (450 < mousePos[0] < (450 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))) or (
                    800 < mousePos[0] < (800 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1])))
            if MouseOn:
                self.next_level = True
                self.current_level += 1
            if mouseOff:
                self.tryAgain = True

    def draw_start_screen(self, display: pygame.Surface):
        display.blit(self.background_surf, (0, 0))
        pygame.draw.rect(display, 'Pink', self.start_rect)
        pygame.draw.rect(display, 'Pink', self.start_rect, 10)
        display.blit(self.title_surface, self.title_rect)
        display.blit(self.explanation_surface, self.explanation_rect)
        display.blit(self.start_surface, self.start_rect)

    def display_win(self, display: pygame.Surface):
        display.blit(self.background_surf, (0, 0))
        display.blit(self.win_surface, self.win_rect)

    def display_try_again(self, display: pygame.Surface):
        display.blit(self.background_surf, (0, 0))
        display.blit(self.try_again_surface, self.try_again_rect)

    def current_level_function(self, display: pygame.Surface):
        # display.blit(self.background_surf, (0, 0))
        if self.current_level == 1:
            self.draw_level_one(display)