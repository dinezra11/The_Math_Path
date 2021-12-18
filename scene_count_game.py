import pygame
from scene import Scene
import database


class count_game(Scene):

    def __init__(self, display, userId):
        super().__init__(display)
        self.userId = userId
        self.background_surf = pygame.image.load('images/1024x800 background.png')

        self.mouse_pos = pygame.mouse.get_pos()

        self.title_font = pygame.font.Font(None, 100)
        self.title_surface = self.title_font.render('Counting Game', True, 'Black')
        self.title_rect = self.title_surface.get_rect(midtop=(512, 150))

        self.explanation_font = pygame.font.Font(None, 30)
        self.explanation_surface = self.explanation_font.render(
            'In this game you have to count the objects and write the right amount', True, 'Black')
        self.explanation_rect = self.explanation_surface.get_rect(midtop=(512, 250))

        self.start_font = pygame.font.Font(None, 50)
        self.start_surface = self.start_font.render('START GAME', True, 'Black')
        self.start_rect = self.start_surface.get_rect(midtop=(512, 300))

        self.win_font = pygame.font.Font(None, 40)
        self.win_surface = self.win_font.render('YOU ARE RIGHT! PRESS SPACE FOR NEXT LEVEL', True, 'Black')
        self.win_rect = self.win_surface.get_rect(midtop=(512, 300))

        self.end_game1_font = pygame.font.Font(None, 40)
        self.end_game1_surface = self.end_game1_font.render('GOOD JOB, YOU HAVE REACHED THE END OF THE GAME!', True,
                                                            'Black')
        self.end_game1_rect = self.win_surface.get_rect(midtop=(450, 300))

        self.end_game2_font = pygame.font.Font(None, 40)
        self.end_game2_surface = self.end_game2_font.render('PRESS SPACE TO RETURN TO THE MENU', True,
                                                            'Black')
        self.end_game2_rect = self.win_surface.get_rect(midtop=(575, 500))

        self.try_again_font = pygame.font.Font(None, 50)
        self.try_again_surface = self.try_again_font.render('THATS INCORRECT,PRESS SPACE TO TRY AGAIN!', True, 'Black')
        self.try_again_rect = self.start_surface.get_rect(midtop=(175, 300))

        self.eagle_surface = pygame.image.load('images/count_numbers/eagle.png')
        self.eagle_surface = pygame.transform.scale(self.eagle_surface, (100, 100))

        self.monkey_surface = pygame.image.load('images/count_numbers/monkey.png')
        self.monkey_surface = pygame.transform.scale(self.monkey_surface, (100, 100))

        self.cow_surface = pygame.image.load('images/count_numbers/cow.png')
        self.cow_surface = pygame.transform.scale(self.cow_surface, (100, 100))

        self.one_surface = pygame.image.load('images/count_numbers/1.png')
        self.one_surface = pygame.transform.scale(self.one_surface, (100, 100))
        self.two_surface = pygame.image.load('images/count_numbers/2.png')
        self.two_surface = pygame.transform.scale(self.two_surface, (100, 100))
        self.three_surface = pygame.image.load('images/count_numbers/3.png')
        self.three_surface = pygame.transform.scale(self.three_surface, (100, 100))
        self.four_surface = pygame.image.load('images/count_numbers/4.png')
        self.four_surface = pygame.transform.scale(self.four_surface, (100, 100))
        self.five_surface = pygame.image.load('images/count_numbers/5.png')
        self.five_surface = pygame.transform.scale(self.five_surface, (100, 100))
        self.six_surface = pygame.image.load('images/count_numbers/6.png')
        self.six_surface = pygame.transform.scale(self.six_surface, (100, 100))
        self.seven_surface = pygame.image.load('images/count_numbers/7.png')
        self.seven_surface = pygame.transform.scale(self.seven_surface, (100, 100))
        self.eight_surface = pygame.image.load('images/count_numbers/8.png')
        self.eight_surface = pygame.transform.scale(self.eight_surface, (100, 100))
        self.nine_surface = pygame.image.load('images/count_numbers/9.png')
        self.nine_surface = pygame.transform.scale(self.nine_surface, (100, 100))
        self.zero_surface = pygame.image.load('images/count_numbers/0.png')
        self.zero_surface = pygame.transform.scale(self.zero_surface, (100, 100))

        self.start_state = False
        self.current_level = 1
        self.next_level = False
        self.tryAgain = False
        self.clickable = True
        self.end_game = False
        self.update_end_game = False

    def update(self):
        if self.update_end_game:
            database.addScore("Count Game", 0, self.userId)
            return self.userId  # Return userId so the system will go back to the user's menu screen
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
        elif self.end_game:
            self.display_end_game(display)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.update_end_game = True
        else:
            self.current_level_function(display)

    def draw_level_one(self, display: pygame.Surface):

        display.blit(self.background_surf, (0, 0))
        one_explain = pygame.font.Font(None, 50)
        one_explain_surface = one_explain.render('How many eagles can you count?', True, 'Black')
        one_explain_rec = one_explain_surface.get_rect(midtop=(512, 175))
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
                self.current_level += 1
                self.next_level = True
            if mouseOff:
                self.tryAgain = True

    def draw_start_screen(self, display: pygame.Surface):
        display.blit(self.background_surf, (0, 0))
        pygame.draw.rect(display, 'Grey', self.start_rect)
        pygame.draw.rect(display, 'Grey', self.start_rect, 10)
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
        if self.current_level == 1:
            self.draw_level_one(display)
        elif self.current_level == 2:
            self.draw_level_two(display)
        elif self.current_level == 3:
            self.draw_level_three(display)
        elif self.current_level == 4:
            self.end_game = True

    def draw_level_two(self, display: pygame.Surface):

        display.blit(self.background_surf, (0, 0))
        two_explain = pygame.font.Font(None, 50)
        two_explain_surface = two_explain.render('How many monkeys can you count?', True, 'Black')
        two_explain_rec = two_explain_surface.get_rect(midtop=(512, 150))
        display.blit(two_explain_surface, two_explain_rec)
        for i in range(100, 900, 225):
            display.blit(self.monkey_surface, (i, 250))
            display.blit(self.monkey_surface, (i, 450))
        display.blit(self.eight_surface, (450, 600))
        display.blit(self.one_surface, (200, 600))
        display.blit(self.three_surface, (800, 600))
        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.four_surface.get_size()
            mousePos = pygame.mouse.get_pos()
            MouseOn = 450 < mousePos[0] < (450 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))
            mouseOff = (200 < mousePos[0] < (200 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))) or (
                    800 < mousePos[0] < (800 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1])))
            if MouseOn:
                self.current_level += 1
                self.next_level = True
            if mouseOff:
                self.tryAgain = True

    def draw_level_three(self, display: pygame.Surface):

        display.blit(self.background_surf, (0, 0))
        three_explain = pygame.font.Font(None, 50)
        three_explain_surface = three_explain.render('How many cows can you count?', True, 'Black')
        three_explain_rec = three_explain_surface.get_rect(midtop=(512, 150))
        display.blit(three_explain_surface, three_explain_rec)
        display.blit(self.eagle_surface, (100, 250))
        display.blit(self.eagle_surface, (300, 250))
        display.blit(self.eagle_surface, (700, 250))
        display.blit(self.cow_surface, (500, 250))
        display.blit(self.eagle_surface, (250, 450))
        display.blit(self.eagle_surface, (450, 450))
        display.blit(self.cow_surface, (650, 450))
        display.blit(self.five_surface, (450, 600))
        display.blit(self.zero_surface, (200, 600))
        display.blit(self.two_surface, (800, 600))
        if pygame.mouse.get_pressed()[0]:
            buttonSize = self.four_surface.get_size()
            mousePos = pygame.mouse.get_pos()
            MouseOn = 800 < mousePos[0] < (800 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))
            mouseOff = (200 < mousePos[0] < (200 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1]))) or (
                    450 < mousePos[0] < (450 + buttonSize[0]) and (600 < mousePos[1] < (600 + buttonSize[1])))
            if MouseOn:
                self.current_level += 1
                self.next_level = True
            if mouseOff:
                self.tryAgain = True

    def display_end_game(self, display: pygame.Surface):
        display.blit(self.background_surf, (0, 0))
        display.blit(self.end_game1_surface, self.end_game1_rect)
        display.blit(self.end_game2_surface, self.end_game2_rect)
