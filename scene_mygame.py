import pygame
import random
from scene import Scene


class MyGame(Scene):
    # ***********************************************************************************************************
    def __init__(self, display):
        super().__init__(display)
        self.score = 0
        self.operand1 = random.randint(0,10)
        self.operand2 = random.randint(0,10)
        self.correctanswer =  (self.operand1) * (self.operand2)
        self.wronganswer1, self.wronganswer2, self.wronganswer3 = random.sample(range(0, 100), 3)
        self.answers = [self.wronganswer1, self.wronganswer2, self.wronganswer3]
        for i in range(3):
            while self.correctanswer == self.answers[i]:
                self.answers[i] = random.randint(0, 100)

        self.expression1 = (" * ")
        self.statement = (" = ")
        self.q = ("?")
        self.mathstring = str(self.operand1) + str(self.expression1) + str(self.operand2) + str(self.statement) + (self.q)

        self.BACKGROUND_COLOR = (0, 128, 255)
        self.green = (0, 255, 0)
        blue = (0, 0, 128)
        self.color = blue
        self.x = 400
        self.y = 400
        self.display_surface = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption('Show math expressions')
        self.font = pygame.font.Font('fonts/defaultFont.ttf', 32)
        # init the math question
        self.text = self.font.render(self.mathstring, True, self.green, self.color)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x // 2, 75)
        # init the math answer 1   (the correct answer ---> it will be switched with another answer randomly)
        self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
        self.textRect2 = self.text2.get_rect()
        self.textRect2.center = (self.x // 2, 150)
        self.rect2place = 150
        # init the math answer 2
        self.text3 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
        self.textRect3 = self.text3.get_rect()
        self.textRect3.center = (self.x // 2, 200)
        self.rect3place = 200
        # init the math answer 3
        self.text4 = self.font.render(str(self.wronganswer2), True, self.green, self.color)
        self.textRect4 = self.text4.get_rect()
        self.textRect4.center = (self.x // 2, 250)
        self.rect4place = 250
        # init the math answer 4
        self.text5 = self.font.render(str(self.wronganswer3), True, self.green, self.color)
        self.textRect5 = self.text5.get_rect()
        self.textRect5.center = (self.x // 2, 300)
        self.rect5place = 300
        # init exit button
        self.text6 = self.font.render(" Exit ", True, self.green, self.color)
        self.textRect6 = self.text6.get_rect()
        self.textRect6.center = ((self.x // 2), 20)
        # init next button
        self.text7 = self.font.render(" Next ", True, self.green, self.color)
        self.textRect7 = self.text7.get_rect()
        self.textRect7.center = (self.x - 45, 20)

        # i have to do function that swap the correct answer rectangle with one of the wrong answers

    # ***********************************************************************************************************
    def update(self):
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # -------------------------------if clicked on Exit-----------------------------------------
        mouse_pos = pygame.mouse.get_pos()
        if self.textRect6.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.color = (255, 255, 0)
                return False
        # -------------------------------if clicked on Next------------------------------------------
        mouse_pos = pygame.mouse.get_pos()
        if self.textRect7.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.operand1 = random.randint(0, 10)
                self.operand2 = random.randint(0, 10)
                self.correctanswer = (self.operand1) * (self.operand2)
                self.wronganswer1, self.wronganswer2, self.wronganswer3 = random.sample(range(0, 100), 3)
                self.answers = [self.wronganswer1, self.wronganswer2, self.wronganswer3]
                for i in range(3):
                    while self.correctanswer == self.answers[i]:
                        self.answers[i] = random.randint(0, 100)
                self.expression1 = (" * ")
                self.statement = (" = ")
                self.q = ("?")
                self.mathstring = str(self.operand1) + str(self.expression1) + str(self.operand2) + str(self.statement) + (self.q)
                # init the math question
                self.text = self.font.render(self.mathstring, True, self.green, self.color)
                self.textRect = self.text.get_rect()
                self.textRect.center = (self.x // 2, 75)
                # init the math answer 1   (the correct answer ---> it will be switched with another answer randomly)
                self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                self.textRect2 = self.text2.get_rect()
                self.textRect2.center = (self.x // 2, 150)
                self.rect2place = 150
                # init the math answer 2
                self.text3 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
                self.textRect3 = self.text3.get_rect()
                self.textRect3.center = (self.x // 2, 200)
                self.rect3place = 200
                # init the math answer 3
                self.text4 = self.font.render(str(self.wronganswer2), True, self.green, self.color)
                self.textRect4 = self.text4.get_rect()
                self.textRect4.center = (self.x // 2, 250)
                self.rect4place = 250
                # init the math answer 4
                self.text5 = self.font.render(str(self.wronganswer3), True, self.green, self.color)
                self.textRect5 = self.text5.get_rect()
                self.textRect5.center = (self.x // 2, 300)
                self.rect5place = 300

                # ----change the correct answer location-------
                randnumber = random.randint(1, 4)
                if randnumber == 2:
                    self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                    self.textRect2 = self.text2.get_rect()
                    self.textRect2.center = (self.x // 2, 200)
                    self.rect2place = 200

                    self.text3 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
                    self.textRect3 = self.text3.get_rect()
                    self.textRect3.center = (self.x // 2, 150)
                    self.rect3place = 150
                if randnumber == 3:
                    self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                    self.textRect2 = self.text2.get_rect()
                    self.textRect2.center = (self.x // 2, 250)
                    self.rect2place = 250

                    self.text4 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
                    self.textRect4 = self.text4.get_rect()
                    self.textRect4.center = (self.x // 2, 150)
                    self.rect4place = 150
                if randnumber == 4:
                    self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                    self.textRect2 = self.text2.get_rect()
                    self.textRect2.center = (self.x // 2, 300)
                    self.rect2place = 300

                    self.text5 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
                    self.textRect5 = self.text5.get_rect()
                    self.textRect5.center = (self.x // 2, 150)
                    self.rect5place = 150

        # -------------------------------if clicked on one of the answers---------------------------------------------
        # ----if clicked on the correct answer---------
        mouse_pos = pygame.mouse.get_pos()
        if self.textRect2.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                white = (255, 255, 255)
                self.text2 = self.font.render(str(self.correctanswer), True, self.green, white)
                self.textRect2 = self.text2.get_rect()
                self.textRect2.center = (self.x // 2, self.rect2place)
                self.score += 1
                # should be automatic click on next button
            # --if clicked on one of the wrong answers----------------------
        elif self.textRect3.collidepoint(mouse_pos) or self.textRect4.collidepoint(mouse_pos) or self.textRect5.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # fill the correct answer rectangle with white
                white = (255, 255, 255)
                self.text2 = self.font.render(str(self.correctanswer), True, self.green, white)
                self.textRect2 = self.text2.get_rect()
                self.textRect2.center = (self.x // 2, self.rect2place)
                # fill the wrong answers rectangle with red
                red = (255, 0, 0)
                self.text3 = self.font.render(str(self.wronganswer1), True, self.green, red)
                self.textRect3 = self.text3.get_rect()
                self.textRect3.center = (self.x // 2, self.rect3place)

                self.text4 = self.font.render(str(self.wronganswer2), True, self.green, red)
                self.textRect4 = self.text4.get_rect()
                self.textRect4.center = (self.x // 2, self.rect4place)

                self.text5 = self.font.render(str(self.wronganswer3), True, self.green, red)
                self.textRect5 = self.text5.get_rect()
                self.textRect5.center = (self.x // 2, self.rect5place)

                # have to add automatic click on next button
        return True

    # ***********************************************************************************************************
    def draw(self, display: pygame.Surface):
        self.display_surface.fill(self.BACKGROUND_COLOR)
        self.display_surface.blit(self.text, self.textRect)
        self.display_surface.blit(self.text2, self.textRect2)
        self.display_surface.blit(self.text3, self.textRect3)
        self.display_surface.blit(self.text4, self.textRect4)
        self.display_surface.blit(self.text5, self.textRect5)
        self.display_surface.blit(self.text6, self.textRect6)
        self.display_surface.blit(self.text7, self.textRect7)

        pass
