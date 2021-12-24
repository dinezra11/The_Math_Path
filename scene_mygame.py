import pygame
import random
from scene import Scene
import database


class MyGame(Scene):
    # ***********************************************************************************************************
    def __init__(self, display, userId):
        super().__init__(display)
        # to click one time in the right answer
        self.can_click_on_right_answer = 1
        self.userId = userId
        self.score = 0
        self.total = 0
        self.operand1 = random.randint(0, 10)
        self.operand2 = random.randint(0, 10)
        self.correctanswer = self.operand1 * self.operand2
        # to insure different answers that are close to correct answer----
        self.wronganswer1_plus_minus = random.randint(1, 2)
        if self.wronganswer1_plus_minus == 1:
            self.wronganswer1 = self.correctanswer + 1
        elif self.wronganswer1_plus_minus == 2:
            self.wronganswer1 = self.correctanswer - 1

        self.wronganswer2_plus_minus = random.randint(1, 2)
        if self.wronganswer2_plus_minus == 1:
            self.wronganswer2 = self.correctanswer + 2
        elif self.wronganswer2_plus_minus == 2:
            self.wronganswer2 = self.correctanswer - 2

        self.wronganswer3_plus_minus = random.randint(1, 2)
        if self.wronganswer3_plus_minus == 1:
            self.wronganswer3 = self.correctanswer + 3
        elif self.wronganswer3_plus_minus == 2:
            self.wronganswer3 = self.correctanswer - 3

        self.expression1 = " * "
        self.statement = " = "
        self.q = "?"
        self.mathstring = str(self.operand1) + self.expression1 + str(self.operand2) + self.statement + self.q

        self.BACKGROUND_COLOR = (0, 128, 255)
        self.green = (0, 255, 0)
        blue = (0, 0, 128)
        self.color = blue
        self.x = 1024
        self.y = 800
        self.display_surface = display
        self.font = pygame.font.Font('fonts/defaultFont.ttf', 32)
        # init the math question
        self.text = self.font.render(self.mathstring, True, self.green, self.color)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x // 2, 80)
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
        # init score/total button
        self.slashstr = "/"
        self.strscore = "Score/Total: " + str(self.score) + self.slashstr + str(self.total)
        self.text8 = self.font.render(self.strscore, True, self.green, self.color)
        self.textRect8 = self.text8.get_rect()
        self.textRect8.center = (self.x // 2, self.y - 70)
        # init level button
        self.level = 1
        self.strlevel = "Level: " + str(self.level) + " of 3"
        self.text9 = self.font.render(self.strlevel, True, self.green, self.color)
        self.textRect9 = self.text9.get_rect()
        self.textRect9.center = (100, self.y - 70)
        # init note (with the background)!!!
        self.image = pygame.image.load("images/scene_mygame.png")
        # init END GAME background
        self.end_image = pygame.image.load("images/scene_mygame_end_game.png")

    # ***********************************************************************************************************
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.addScore("Math Expressions (x)", self.score, self.userId)  # Save in DB
                return self.userId  # Return userId so the system will go back to the user's menu screen
            # -------------------------------if clicked on Exit-----------------------------------------
            elif self.textRect6.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.color = (255, 255, 0)
                    database.addScore("Math Expressions (x)", self.score, self.userId)  # Save in DB
                    return self.userId  # Return userId so the system will go back to the user's menu screen
            # -------------------------------if clicked on Next------------------------------------------
            elif self.textRect7.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.can_click_on_right_answer = 1
                    # check if leveled up after 10 questions
                    # the game ends after 30 questions
                    if self.total == 31:
                        # init exit button
                        self.text6 = self.font.render(" Exit ", True, self.green, self.color)
                        self.textRect6 = self.text6.get_rect()
                        self.textRect6.center = ((self.x // 2), 20)
                        if self.textRect6.collidepoint(mouse_pos):
                            if pygame.mouse.get_pressed()[0]:
                                database.addScore("Math Expressions (x)", self.score, self.userId)  # Save in DB
                                return self.userId  # Return userId so the system will go back to the user's menu screen
                        return True
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.total += 1
                    if self.total == 11 or self.total == 21:
                        if (self.score/self.total) >= 0.8:
                            self.level += 1
                    # init operand for each level of 3
                    if self.level == 1:
                        self.operand1 = random.randint(1, 10)
                        self.operand2 = random.randint(1, 10)
                    elif self.level == 2:
                        self.operand1 = random.randint(10, 20)
                        self.operand2 = random.randint(1, 10)
                    elif self.level == 3:
                        self.operand1 = random.randint(10, 20)
                        self.operand2 = random.randint(10, 20)

                    self.correctanswer = self.operand1 * self.operand2

                    # to insure different answers that are close to correct answer-----
                    self.wronganswer1_plus_minus = random.randint(1, 2)
                    if self.wronganswer1_plus_minus == 1:
                        self.wronganswer1 = self.correctanswer + 1
                    elif self.wronganswer1_plus_minus == 2:
                        self.wronganswer1 = self.correctanswer - 1

                    self.wronganswer2_plus_minus = random.randint(1, 2)
                    if self.wronganswer2_plus_minus == 1:
                        self.wronganswer2 = self.correctanswer + 2
                    elif self.wronganswer2_plus_minus == 2:
                        self.wronganswer2 = self.correctanswer - 2

                    self.wronganswer3_plus_minus = random.randint(1, 2)
                    if self.wronganswer3_plus_minus == 1:
                        self.wronganswer3 = self.correctanswer + 3
                    elif self.wronganswer3_plus_minus == 2:
                        self.wronganswer3 = self.correctanswer - 3

                    self.expression1 = " * "
                    self.statement = " = "
                    self.q = "?"
                    self.mathstring = str(self.operand1) + self.expression1 + str(self.operand2) + self.statement +\
                                      self.q
                    # init the math question
                    self.text = self.font.render(self.mathstring, True, self.green, self.color)
                    self.textRect = self.text.get_rect()
                    self.textRect.center = (self.x // 2, 80)
                    # init the math answer 1 (the correct answer ---> it will be switched with another answer randomly)
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
                    # init score/total button
                    self.slashstr = "/"
                    self.strscore = "Score/Total: " + str(self.score) + self.slashstr + str(self.total)
                    self.text8 = self.font.render(self.strscore, True, self.green, self.color)
                    self.textRect8 = self.text8.get_rect()
                    self.textRect8.center = (self.x // 2, self.y - 70)
                    # init level button
                    self.strlevel = "Level: " + str(self.level) + " of 3"
                    self.text9 = self.font.render(self.strlevel, True, self.green, self.color)
                    self.textRect9 = self.text9.get_rect()
                    self.textRect9.center = (100, self.y - 70)

                    # ----change the correct answer location-------
                    self.randnumber = random.randint(2, 4)
                    if self.randnumber == 2:
                        self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                        self.textRect2 = self.text2.get_rect()
                        self.textRect2.center = (self.x // 2, 200)
                        self.rect2place = 200

                        self.text3 = self.font.render(str(self.wronganswer1), True, self.green, self.color)
                        self.textRect3 = self.text3.get_rect()
                        self.textRect3.center = (self.x // 2, 150)
                        self.rect3place = 150
                    elif self.randnumber == 3:
                        self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                        self.textRect2 = self.text2.get_rect()
                        self.textRect2.center = (self.x // 2, 250)
                        self.rect2place = 250

                        self.text4 = self.font.render(str(self.wronganswer2), True, self.green, self.color)
                        self.textRect4 = self.text4.get_rect()
                        self.textRect4.center = (self.x // 2, 150)
                        self.rect4place = 150
                    elif self.randnumber == 4:
                        self.text2 = self.font.render(str(self.correctanswer), True, self.green, self.color)
                        self.textRect2 = self.text2.get_rect()
                        self.textRect2.center = (self.x // 2, 300)
                        self.rect2place = 300

                        self.text5 = self.font.render(str(self.wronganswer3), True, self.green, self.color)
                        self.textRect5 = self.text5.get_rect()
                        self.textRect5.center = (self.x // 2, 150)
                        self.rect5place = 150
                    return True

            # -------------------------------if clicked on one of the answers------------------------------------------
            # ----if clicked on the correct answer---------
            elif self.textRect2.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    if self.can_click_on_right_answer == 1:
                        white = (255, 255, 255)
                        self.text2 = self.font.render(str(self.correctanswer), True, self.green, white)
                        self.textRect2 = self.text2.get_rect()
                        self.textRect2.center = (self.x // 2, self.rect2place)
                        self.score += 1
                        return True
            # --if clicked on one of the wrong answers----------------------
            elif self.textRect3.collidepoint(mouse_pos) or self.textRect4.collidepoint(mouse_pos) or \
                    self.textRect5.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.can_click_on_right_answer = 0
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
                    return True

        return True

    # ***********************************************************************************************************
    def draw(self, display: pygame.Surface):
        self.display_surface.fill(self.BACKGROUND_COLOR)
        if self.total == 31:
            self.display_surface.blit(self.end_image, (0, 0))
            self.display_surface.blit(self.text6, self.textRect6)
        else:
            self.display_surface.blit(self.image, (0, 0))
            self.display_surface.blit(self.text, self.textRect)
            self.display_surface.blit(self.text2, self.textRect2)
            self.display_surface.blit(self.text3, self.textRect3)
            self.display_surface.blit(self.text4, self.textRect4)
            self.display_surface.blit(self.text5, self.textRect5)
            self.display_surface.blit(self.text6, self.textRect6)
            self.display_surface.blit(self.text7, self.textRect7)
            self.display_surface.blit(self.text8, self.textRect8)
            self.display_surface.blit(self.text9, self.textRect9)
        # pass
