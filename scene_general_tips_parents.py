import pygame
from scene import Scene
import database


class general_tips_parents(Scene):

    def __init__(self, display, userId):
        super().__init__(display)
        self.userId = userId
        self.background_surf = pygame.image.load('images/general_tips/1.png')
        self.background_surf = pygame.transform.scale(self.background_surf, (1024, 800))
        self.background_rec = self.background_surf.get_rect(midtop=(1024, 800))

        self.first_surf = pygame.image.load('images/general_tips/2.png')
        self.first_surf = pygame.transform.scale(self.first_surf, (1024, 800))
        self.first_rec = self.first_surf.get_rect(midtop=(1024, 800))

        self.second_surf = pygame.image.load('images/general_tips/3.png')
        self.second_surf = pygame.transform.scale(self.second_surf, (1024, 800))
        self.second_rec = self.second_surf.get_rect(midtop=(1024, 800))

        self.third_surf = pygame.image.load('images/general_tips/4.png')
        self.third_surf = pygame.transform.scale(self.third_surf, (1024, 800))
        self.third_rec = self.third_surf.get_rect(midtop=(1024, 800))

        self.fourth_surf = pygame.image.load('images/general_tips/5.png')
        self.fourth_surf = pygame.transform.scale(self.fourth_surf, (1024, 800))
        self.fourth_rec = self.fourth_surf.get_rect(midtop=(1024, 800))

        self.five_surf = pygame.image.load('images/general_tips/6.png')
        self.five_surf = pygame.transform.scale(self.five_surf, (1024, 800))
        self.five_rec = self.five_surf.get_rect(midtop=(1024, 800))

        self.end_surf = pygame.image.load('images/general_tips/end.png')
        self.end_surf = pygame.transform.scale(self.end_surf, (1024, 800))
        self.end_rec = self.end_surf.get_rect(midtop=(1024, 800))

        self.back_surf = pygame.image.load('images/back.png')
        self.back_surf = pygame.transform.scale(self.back_surf, (150, 150))
        self.back_rec = self.back_surf.get_rect(midtop=(900, 600))

        self.back2_surf = pygame.image.load('images/general_tips/back.png')
        self.back2_surf = pygame.transform.scale(self.back2_surf, (50, 50))
        self.back2_rec = self.back2_surf.get_rect(midtop=(500, 700))

        self.current_level = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.userId
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_rec.collidepoint(event.pos):
                    return self.userId
                if self.back2_rec.collidepoint(event.pos):
                    self.current_level-=1
                else:
                    self.current_level += 1
        return True

    def draw(self, display: pygame.Surface):
        if self.current_level==0:
            display.blit(self.background_surf, (0, 0))
            display.blit(self.back_surf, self.back_rec)
        elif self.current_level == 1:
            self.draw_level_one(display)
        elif self.current_level == 2:
            self.draw_level_two(display)
        elif self.current_level == 3:
            self.draw_level_three(display)
        elif self.current_level == 4:
            self.draw_level_four(display)
        elif self.current_level == 5:
            self.draw_level_five(display)
        elif self.current_level == 6:
            self.draw_end(display)


    def draw_level_one(self, display: pygame.Surface):
        display.blit(self.first_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)
        display.blit(self.back2_surf, self.back2_rec)
    def draw_level_two(self, display: pygame.Surface):
        display.blit(self.second_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)
        display.blit(self.back2_surf, self.back2_rec)
    def draw_level_three(self, display: pygame.Surface):
        display.blit(self.third_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)
        display.blit(self.back2_surf, self.back2_rec)
    def draw_level_four(self, display: pygame.Surface):
        display.blit(self.fourth_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)
        display.blit(self.back2_surf, self.back2_rec)
    def draw_level_five(self, display: pygame.Surface):
        display.blit(self.five_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)
        display.blit(self.back2_surf, self.back2_rec)
    def draw_end(self, display: pygame.Surface):
        display.blit(self.end_surf, (0, 0))
        display.blit(self.back_surf, self.back_rec)