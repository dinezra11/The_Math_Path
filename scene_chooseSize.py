from scene import Scene
import pygame
import pygame.display


class ChooseSize(Scene):
    def __init__(self, display):
        """ Initialize the scene.

        :param:     display -> The display where to draw the scene.
        """
        super().__init__(display)
        self.test_surface = pygame.image.load('images/1024x800 background.png')

        self.state = False
        self.state_left = False
        self.state_right = False
        self.state_equal = False

        """ Prints the title"""
        font_title = pygame.font.Font(None, 100)
        self.title = font_title.render('SizeMe', False, 'Blue')

        """ Prints the 1st line of the explain of the game"""
        font_xpl = pygame.font.Font(None, 30)
        x = 'Welcome to SizeMe!'
        self.xpl = font_xpl.render(x, False, 'Black')

        """ Prints the 2nd line of the explain of the game"""
        font_xpl1 = pygame.font.Font(None, 30)
        y = 'Here we will learn the size value of the objects'
        self.xpl1 = font_xpl1.render(y, False, 'Black')

        """ Prints the 3rd line of the explain of the game"""
        font_xpl2 = pygame.font.Font(None, 30)
        z = 'that will appear in front of us.'
        self.xpl2 = font_xpl2.render(z, False, 'Black')

        """ Printing the instruction of START button """
        s = 'To start the game press on "START".'
        font_xpl3 = pygame.font.Font(None, 35)
        self.xpl3 = font_xpl3.render(s, False, 'Black')

        self.start_button = pygame.image.load('images/start button.png')

        self.page1 = pygame.image.load('images/board.jpg')

        pass

    """New Page 1 for game"""

    def newpage(self, display: pygame.Surface):
        display.blit(self.page1, (0, 0))
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
        """pressinig on left corner correct answer"""
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn1 = 250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                        500 < mousePos[1] < (500 + leftButtonSize[1]))
            if isMouseOn1:
                print('Correct answer!')
                # self.state_left = True
        """pressin mid/right options wrong answer"""
        if pygame.mouse.get_pressed()[0]:
            equalButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn1 = 500 < mousePos[0] < (500 + equalButtonSize[0]) and (
                        500 < mousePos[1] < (500 + equalButtonSize[1]))
            if isMouseOn1:
                print('Wrong Answer!')
                # self.state_equal = True
        if pygame.mouse.get_pressed()[0]:
            rightButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn1 = 750 < mousePos[0] < (750 + rightButtonSize[0]) and (
                        500 < mousePos[1] < (500 + rightButtonSize[1]))
            if isMouseOn1:
                print('Wrong Answer!')
                # self.state_right = True

    def correct_answer(self, display: pygame.Surface):
        correct_window = pygame.image.load('images/correct-answer-md.png')
        display.blit(self.correct_answer(512, 400))

    def wrong_answer(self, display: pygame.Surface):
        wrong_window = pygame.image.load('images/wrong answer.png')
        display.blit(self.wrong_answer(512, 400))

    def update(self):
        """ Update the scene. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.start_button.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn = 380 < mousePos[0] < (380 + buttonSize[0]) and (420 < mousePos[1] < (420 + buttonSize[1]))
            if isMouseOn:
                self.state = True

        # if pygame.mouse.get_pressed()[0]:
        #     left_button_Size = self.left_symbol.get_size()
        #     mousePos1 = pygame.mouse.get_pos()
        #     isMouseOn1 = 300 < mousePos1[0] < (300 + left_button_Size[0]) and (500 < mousePos1[1] < (500 + left_button_Size[1]))
        #     if isMouseOn1:
        #         self.state_left = True
        pass

        return True

    def draw(self, display: pygame.Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.blit(self.test_surface, (0, 0))
        display.blit(self.title, (380, 180))
        display.blit(self.xpl, (200, 260))
        display.blit(self.xpl1, (200, 280))
        display.blit(self.xpl2, (200, 300))
        display.blit(self.xpl3, (300, 400))
        display.blit(self.start_button, (380, 420))
        if self.state:
            self.newpage(display)
        if self.state_left:
            self.correct_answer(display)
        pass
