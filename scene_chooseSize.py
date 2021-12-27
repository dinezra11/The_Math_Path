import pygame
from scene import Scene
import database


class ChooseSize(Scene):
    def __init__(self, display, userId):
        super().__init__(display)
        self.userId = userId
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

        self.start_button = pygame.image.load('images/Choose Size/start button.png')

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

        # Score Variables:
        self.score_correct = 0
        self.score_wrong = 0

    def update(self):
        if self.update_end_game:
            score = int(self.score_correct / (self.score_correct + self.score_wrong) * 100)
            database.addScore("Choose Size", score, self.userId)
            return self.userId  # Return userId so the system will go back to the user's menu screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.start_button.get_size()
            mousePos = pygame.mouse.get_pos()
            isMouseOn = 380 < mousePos[0] < (380 + buttonSize[0]) and (490 < mousePos[1] < (490 + buttonSize[1]))
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
        font_numquestion = pygame.font.Font(None, 30)
        text_question = 'Question 1:'
        self.numquestion = font_numquestion.render(text_question, False, 'Red')
        display.blit(self.numquestion, (200, 230))
        # """ Images For QUESTION 1"""
        self.one_ball = pygame.image.load('images/Choose Size/Questions/1_blue_ball.png')
        display.blit(self.one_ball, (200, 320))
        self.six_balls = pygame.image.load('images/Choose Size/Questions/6_balls.png')
        display.blit(self.six_balls, (600, 320))

        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_two(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion2 = pygame.font.Font(None, 30)
        text_question = 'Question 2:'
        self.numquestion2 = font_numquestion2.render(text_question, False, 'Red')
        display.blit(self.numquestion2, (200, 230))
        # """ Images For QUESTION 2"""
        self.nine_balls = pygame.image.load('images/Choose Size/Questions/9_balls.png')
        display.blit(self.nine_balls, (200, 320))
        self.four_balls = pygame.image.load('images/Choose Size/Questions/4_balls.png')
        display.blit(self.four_balls, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 750 < mousePos[0] < (750 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 250 < mousePos[0] < (
                               250 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_three(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion3 = pygame.font.Font(None, 30)
        text_question = 'Question 3:'
        self.numquestion3 = font_numquestion3.render(text_question, False, 'Red')
        display.blit(self.numquestion3, (200, 230))
        # """ Images For QUESTION 3"""
        self.ten_balls = pygame.image.load('images/Choose Size/Questions/10_balls.png')
        display.blit(self.ten_balls, (200, 320))
        self.five_balls = pygame.image.load('images/Choose Size/Questions/5_balls.png')
        display.blit(self.five_balls, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 750 < mousePos[0] < (750 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 250 < mousePos[0] < (
                               250 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_four(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion4 = pygame.font.Font(None, 30)
        text_question = 'Question 4:'
        self.numquestion4 = font_numquestion4.render(text_question, False, 'Red')
        display.blit(self.numquestion4, (200, 230))
        # """ Images For QUESTION 4"""
        self.two_balloons = pygame.image.load('images/Choose Size/Questions/2_balloons.png')
        display.blit(self.two_balloons, (200, 320))
        self.three_balloons = pygame.image.load('images/Choose Size/Questions/3_balloons.png')
        display.blit(self.three_balloons, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_five(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion5 = pygame.font.Font(None, 30)
        text_question = 'Question 5:'
        self.numquestion5 = font_numquestion5.render(text_question, False, 'Red')
        display.blit(self.numquestion5, (200, 230))
        # """ Images For QUESTION 5"""
        self.three_balloons1 = pygame.image.load('images/Choose Size/Questions/3_ballons1.png')
        display.blit(self.three_balloons1, (200, 320))
        self.three_balloons2 = pygame.image.load('images/Choose Size/Questions/3_balloons2.png')
        display.blit(self.three_balloons2, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_six(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion6 = pygame.font.Font(None, 30)
        text_question = 'Question 6:'
        self.numquestion6 = font_numquestion6.render(text_question, False, 'Red')
        display.blit(self.numquestion6, (200, 230))
        # """ Images For QUESTION 6"""
        self.many_bears = pygame.image.load('images/Choose Size/Questions/many_bears.png')
        display.blit(self.many_bears, (200, 320))
        self.six_bears = pygame.image.load('images/Choose Size/Questions/6_bears.png')
        display.blit(self.six_bears, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 750 < mousePos[0] < (750 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 250 < mousePos[0] < (
                               250 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_seven(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion7 = pygame.font.Font(None, 30)
        text_question = 'Question 7:'
        self.numquestion7 = font_numquestion7.render(text_question, False, 'Red')
        display.blit(self.numquestion7, (200, 230))
        # """ Images For QUESTION 7"""
        self.four_bears = pygame.image.load('images/Choose Size/Questions/4_bears.png')
        display.blit(self.four_bears, (200, 320))
        self.one_blue_bear = pygame.image.load('images/Choose Size/Questions/1_blue_bear.png')
        display.blit(self.one_blue_bear, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 750 < mousePos[0] < (750 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 250 < mousePos[0] < (
                               250 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_eight(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion8 = pygame.font.Font(None, 30)
        text_question = 'Question 8:'
        self.numquestion8 = font_numquestion8.render(text_question, False, 'Red')
        display.blit(self.numquestion8, (200, 230))
        # """ Images For QUESTION 8"""
        self.one_green_bear = pygame.image.load('images/Choose Size/Questions/1_green_bear.png')
        display.blit(self.one_green_bear, (200, 320))
        self.one_red_bear = pygame.image.load('images/Choose Size/Questions/1_red_bear.png')
        display.blit(self.one_red_bear, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_nine(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion9 = pygame.font.Font(None, 30)
        text_question = 'Question 9:'
        self.numquestion9 = font_numquestion9.render(text_question, False, 'Red')
        display.blit(self.numquestion9, (200, 230))
        # """ Images For QUESTION 9"""
        self.three_bears = pygame.image.load('images/Choose Size/Questions/3_bears.png')
        display.blit(self.three_bears, (200, 320))
        self.six_bears = pygame.image.load('images/Choose Size/Questions/6_bears.png')
        display.blit(self.six_bears, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def level_ten(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        p = 'According the image choose the correct symbol.'
        font_task = pygame.font.Font(None, 35)
        self.task = font_task.render(p, False, 'Black')
        display.blit(self.task, (200, 180))
        font_numquestion10 = pygame.font.Font(None, 30)
        text_question = 'Question 10:'
        self.numquestion10 = font_numquestion10.render(text_question, False, 'Red')
        display.blit(self.numquestion10, (200, 230))
        # """ Images For QUESTION 10"""
        self.two_bears = pygame.image.load('images/Choose Size/Questions/2_bears.png')
        display.blit(self.two_bears, (200, 320))
        self.two_balloons = pygame.image.load('images/Choose Size/Questions/2_balloons.png')
        display.blit(self.two_balloons, (600, 320))
        # """ Math symbols """
        self.left_symbol = pygame.image.load('images/Choose Size/left.png')
        display.blit(self.left_symbol, (250, 620))
        self.equal_symbol = pygame.image.load('images/Choose Size/equal.png')
        display.blit(self.equal_symbol, (500, 620))
        self.right_symbol = pygame.image.load('images/Choose Size/right.png')
        display.blit(self.right_symbol, (750, 620))
        if pygame.mouse.get_pressed()[0]:
            leftButtonSize = self.left_symbol.get_size()
            mousePos = pygame.mouse.get_pos()
            mouseOn = 500 < mousePos[0] < (500 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))
            mouseOff = (250 < mousePos[0] < (250 + leftButtonSize[0]) and (
                    620 < mousePos[1] < (620 + leftButtonSize[1]))) or 750 < mousePos[0] < (
                               750 + leftButtonSize[0]) and (
                               620 < mousePos[1] < (620 + leftButtonSize[1]))
            if mouseOn:
                self.current_level += 1
                self.next_level = True
                self.score_correct += 1
            if mouseOff:
                self.try_again = True
                self.score_wrong += 1

    def correct_answer(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        correct_window = pygame.image.load('images/Choose Size/correct-answer-md.png')
        display.blit(correct_window, (350, 400))

    def wrong_answer(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        wrong_window = pygame.image.load('images/Choose Size/wrong answer.png')
        display.blit(wrong_window, (280, 200))
        display.blit(self.try_again_surface, (100, 150))

    def display_start_screen(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        display.blit(self.title, (380, 180))
        display.blit(self.xpl, (200, 260))
        display.blit(self.xpl1, (200, 280))
        display.blit(self.xpl2, (200, 300))
        display.blit(self.xpl3, (300, 400))
        display.blit(self.start_button, (380, 490))

    def display_end_game(self, display: pygame.Surface):
        display.blit(self.test_surface, (0, 0))
        display.blit(self.end_game1_surface, self.end_game1_rect)
        display.blit(self.end_game2_surface, self.end_game2_rect)

    def current_level_function(self, display: pygame.Surface):
        # """         if self.current_level==1:
        #             self.level_one(display)
        #         if self.current_level == 2:
        #             self.end_game = True """
        if self.current_level == 1:
            self.level_one(display)
        elif self.current_level == 2:
            self.level_two(display)
        elif self.current_level == 3:
            self.level_three(display)
        elif self.current_level == 4:
            self.level_four(display)
        elif self.current_level == 5:
            self.level_five(display)
        elif self.current_level == 6:
            self.level_six(display)
        elif self.current_level == 7:
            self.level_seven(display)
        elif self.current_level == 8:
            self.level_eight(display)
        elif self.current_level == 9:
            self.level_nine(display)
        elif self.current_level == 10:
            self.level_ten(display)
            self.end_game = True

        # """ Images For QUESTION 11"""
        # """ self.one_ball = pygame.image.load('images/Choose Size/Questions/')
        #         display.blit(self.one_ball, (200, 320))
        #         self.six_balls = pygame.image.load('images/Choose Size/Questions/')
        #         display.blit(self.six_balls, (600, 320))
        #         # """ Images For QUESTION 12"""
        #         self.one_ball = pygame.image.load('images/Choose Size/Questions/')
        #         display.blit(self.one_ball, (200, 320))
        #         self.six_balls = pygame.image.load('images/Choose Size/Questions/')
        #         display.blit(self.six_balls, (600, 320)) """
