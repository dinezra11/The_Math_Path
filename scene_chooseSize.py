import pygame
from scene import Scene
import database


class ChooseSize(Scene):
    def __init__(self, display):
        super().__init__(display)
        self.test_surface = pygame.image.load('images/1024x800 background.png')

        # """ Prints the title"""
        font_title = pygame.font.Font(None, 100)
        self.title = font_title.render('SizeMe', False, 'Blue')

        # """ Prints the 1st line of the explain of the game."""
        font_xpl = pygame.font.Font(None, 30)
        x = 'Welcome to SizeMe!'
        self.xpl = font_xpl.render(x, False, 'Black')

        # """ Prints the 2nd line of the explain of the game."""
        font_xpl1 = pygame.font.Font(None, 30)
        y = 'Here we will learn the size value of the objects'
        self.xpl1 = font_xpl1.render(y, False, 'Black')

        # """ Prints the 3rd line of the explain of the game."""
        font_xpl2 = pygame.font.Font(None, 30)
        z = 'that will appear in front of us.'
        self.xpl2 = font_xpl2.render(z, False, 'Black')

        # """ Printing the instruction of START button """
        s = 'To start the game press on "START".'
        font_xpl3 = pygame.font.Font(None, 35)
        self.xpl3 = font_xpl3.render(s, False, 'Black')

        self.start_button = pygame.image.load('images/start button.png')

        self.page1 = pygame.image.load('images/board.jpg')

        self.end_game1_font = pygame.font.Font(None, 40)
        self.end_game1_surface = self.end_game1_font.render('GOOD JOB, YOU HAVE REACHED THE END OF THE GAME!', True,
                                                            'Black')
        self.end_game1_rect = self.end_game1_surface.get_rect(midtop=(450, 300))

        self.end_game2_font = pygame.font.Font(None, 40)
        self.end_game2_surface = self.end_game2_font.render('PRESS SPACE TO RETURN TO THE MENU', True,
                                                            'Black')
        self.end_game2_rect = self.end_game2_surface.get_rect(midtop=(575, 500))

        self.try_again_font = pygame.font.Font(None, 50)
        self.try_again_surface = self.try_again_font.render('THATS INCORRECT,PRESS SPACE TO TRY AGAIN!', True, 'Black')

        self.state = False
        self.current_level = 1
        self.next_level = False
        self.try_again = False
        self.end_game = False
        self.update_end_game = False

    def update(self):
        if self.update_end_game:
            database.addScore("Choose Size", 0)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.start_button.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn = 380 < mousePos[0] < (380 + buttonSize[0]) and (420 < mousePos[1] < (420 + buttonSize[1]))
            if isMouseOn:
                self.state = True

        return True

    def draw(self, display: pygame.Surface):
        if not self.state:
            self.display_start_screen(display)
        elif self.next_level:
            self.correct_answer(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.next_level = False
        elif self.try_again:
            self.wrong_answer(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.try_again = False
        elif self.end_game:
            self.display_end_game(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.update_end_game = True
        else:
            self.current_level_function(display)

    def level_one(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        self.one_ball = pygame.image.load('images/1 ball.png')
        display.blit(self.one_ball, (200, 360))
        self.six_balls = pygame.image.load('images/6 balls.png')
        display.blit(self.six_balls, (824, 360))

        self.left_symbol = pygame.image.load('images/left.png')
        display.blit(self.left_symbol, (250, 500))
        self.equal_symbol = pygame.image.load('images/equal.png')
        display.blit(self.equal_symbol, (500, 500))
        self.right_symbol = pygame.image.load('images/right.png')
        display.blit(self.right_symbol, (750, 500))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    500 < mousePos[1] < (500 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    500 < mousePos[1] < (500 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               500 < mousePos[1] < (500 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
            if mouseOff:
                self.try_again = True

    def correct_answer(self, display: pygame.Surface):
        display.blit(self.test_surface,(0,0))
        correct_window = pygame.image.load('images/correct-answer-md.png')
        display.blit(correct_window,(350, 400))

    def wrong_answer(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        wrong_window = pygame.image.load('images/wrong answer.png')
        display.blit(wrong_window,(280, 200))
        display.blit(self.try_again_surface, (100, 150))

    def display_start_screen(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        display.blit(self.title, (380, 180))
        display.blit(self.xpl, (200, 260))
        display.blit(self.xpl1, (200, 280))
        display.blit(self.xpl2, (200, 300))
        display.blit(self.xpl3, (300, 400))
        display.blit(self.start_button, (380, 420))

    def display_end_game(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        display.blit(self.end_game1_surface, self.end_game1_rect)
        display.blit(self.end_game2_surface, self.end_game2_rect)

    def current_level_function(self,display:pygame.Surface):
        if self.current_level==1:
            self.level_one(display)
        if self.current_level == 2:
            self.end_game = True

