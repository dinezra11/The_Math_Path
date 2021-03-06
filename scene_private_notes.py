import pygame
from scene import Scene
import database
from uiComponents import Text, Button, TextInput, CycleButton, ErrorText
from tkinter import *
from tkinter import messagebox


class private_notes(Scene):

    def __init__(self, display, userId):
        super().__init__(display)
        self.userId = userId
        self.background_surf = pygame.image.load('images/mefateah_feedback/background2.jpg')
        self.background_surf = pygame.transform.scale(self.background_surf, (1024, 800))
        self.background_rec = self.background_surf.get_rect(midtop=(1024, 800))

        self.mouse_pos = pygame.mouse.get_pos()

        self.title_font = pygame.font.Font(None, 70)
        self.title_surface = self.title_font.render('PRIVATE NOTES', True, 'Black')
        self.title_rect = self.title_surface.get_rect(midtop=(512, 100))

        self.explanation_font = pygame.font.Font(None, 30)
        self.explanation_surface = self.explanation_font.render(
            "Write an ID in the small box and then write a note about the user.", True, 'Black')
        self.explanation_rect = self.explanation_surface.get_rect(midtop=(512, 175))
        self.explanation2_surface = self.explanation_font.render(
            "It will be visible only to you (not to the parent).", True, 'Black')
        self.explanation2_rect = self.explanation2_surface.get_rect(midtop=(512, 200))
        self.explanation3_surface = self.explanation_font.render(
            "To send and go back to the menu, press on the mail button.", True, 'Red')
        self.explanation3_rect = self.explanation3_surface.get_rect(midtop=(512, 225))

        self.text_box_surf = pygame.image.load('images/mefateah_feedback/blank.png')
        self.text_box_surf = pygame.transform.scale(self.text_box_surf, (600, 150))
        self.text_box_rec = self.text_box_surf.get_rect(midtop=(512, 300))

        self.back_surf = pygame.image.load('images/back.png')
        self.back_surf = pygame.transform.scale(self.back_surf, (150, 150))
        self.back_rec = self.back_surf.get_rect(midtop=(900, 600))

        self.send_button_surf = pygame.image.load('images/mefateah_feedback/send.png')
        self.send_button_surf = pygame.transform.scale(self.send_button_surf, (150, 150))
        self.send_button_rec = self.text_box_surf.get_rect(midtop=(700, 580))

        self.last_line_surf = pygame.image.load('images/mefateah_feedback/last.png')
        self.last_line_rec = self.last_line_surf.get_rect(midtop=(500, 500))

        self.user_text = ''
        self.base_font = pygame.font.Font(None, 32)
        self.user_text_surface = self.base_font.render(self.user_text, True, 'Black')
        self.user_text_rec = self.user_text_surface.get_rect(midtop=(220, 325))

        self.final_text = ''
        self.final_text_surface = self.base_font.render(self.final_text, True, 'Black')
        self.final_text_rec = self.final_text_surface.get_rect(midtop=(220, self.user_text_rec.y + 30))

        self.temp_text1 = ''
        self.temp_text1_surface = self.base_font.render(self.temp_text1, True, 'Black')
        self.temp_text1_rec = self.temp_text1_surface.get_rect(midtop=(240, self.user_text_rec.y - 30))

        self.temp_text2 = ''
        self.temp_text2_surface = self.base_font.render(self.temp_text2, True, 'Black')
        self.temp_text2_rec = self.temp_text2_surface.get_rect(midtop=(240, self.temp_text1_rec.y - 30))

        self.temp_text3 = ''
        self.temp_text3_surface = self.base_font.render(self.temp_text3, True, 'Black')
        self.temp_text3_rec = self.temp_text3_surface.get_rect(midtop=(240, self.temp_text2_rec.y - 30))

        self.temp_text4 = ''
        self.temp_text4_surface = self.base_font.render(self.temp_text4, True, 'Black')
        self.temp_text4_rec = self.temp_text4_surface.get_rect(midtop=(240, self.temp_text3_rec.y - 30))

        self.input_rect = pygame.Rect(435, 260, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('grey')
        self.color = self.color_passive
        self.active = False

        self.child_id = ''
        self.child_id_surface = self.base_font.render(self.child_id, True, (255, 255, 255))

        self.last = False
        self.start_write_note = False
        self.start_state = True
        self.start_write_id = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.userId

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.send_button_rec.collidepoint(event.pos):
                    if database.isIdExists(self.child_id):
                        if self.temp_text1 == '':
                            database.addPrivateNotes(self.user_text, self.userId, int(self.child_id))
                        else:
                            database.addPrivateNotes(self.final_text, self.userId, int(self.child_id))
                        return self.userId
                    else:
                        self.child_id = str(self.child_id)
                        self.active = True
                        Tk().wm_withdraw()  # to hide the main window
                        messagebox.showinfo('Continue', 'Child ID does not exist!')

                if self.back_rec.collidepoint(event.pos):
                    return self.userId

                if self.text_box_rec.collidepoint(event.pos):
                    self.start_write_note = True

                if self.input_rect.collidepoint(event.pos):
                    # self.start_write_id=True
                    self.active = True
                else:
                    self.active = False
                    self.start_write_id = False

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.child_id = self.child_id[:-1]
                    self.child_id_surface = self.base_font.render(self.child_id, True, 'Black')
                else:
                    self.child_id += event.unicode
                    self.child_id_surface = self.base_font.render(self.child_id, True, 'Black')

            if event.type == pygame.KEYDOWN and self.start_write_note:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                    self.user_text_surface = self.base_font.render(self.user_text, True, 'Black')
                elif event.key == pygame.K_RETURN or 570 <= self.user_text_surface.get_width() <= 580:
                    self.next_line()
                    self.user_text_surface = self.base_font.render(self.user_text, True, 'Black')
                    if self.last:
                        return self.userId
                else:
                    if self.last:
                        return self.userId
                    self.user_text += event.unicode
                    self.user_text_surface = self.base_font.render(self.user_text, True, 'Black')
                    if 570 <= self.user_text_surface.get_width() <= 580:
                        self.next_line()
        return True

    def draw(self, display: pygame.Surface):
        if self.start_state:
            display.blit(self.background_surf, (0, 0))
            display.blit(self.back_surf, self.back_rec)
            display.blit(self.title_surface, self.title_rect)
            display.blit(self.explanation_surface, self.explanation_rect)
            display.blit(self.explanation2_surface, self.explanation2_rect)
            display.blit(self.explanation3_surface, self.explanation3_rect)
            display.blit(self.text_box_surf, self.text_box_rec)
            display.blit(self.send_button_surf, self.send_button_rec)
            display.blit(self.user_text_surface, self.user_text_rec)
            display.blit(self.temp_text1_surface, self.temp_text1_rec)
            display.blit(self.temp_text2_surface, self.temp_text2_rec)
            display.blit(self.temp_text3_surface, self.temp_text3_rec)
            display.blit(self.temp_text4_surface, self.temp_text4_rec)
            if self.user_text_rec.y > 415:
                display.blit(self.last_line_surf, self.last_line_rec)
                self.last = True
            pygame.draw.rect(display, self.color, self.input_rect)
            if self.active:
                self.start_write_note = False
                self.color = self.color_active
                display.blit(self.child_id_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
                self.input_rect.w = max(100, self.child_id_surface.get_width() + 10)
            else:
                self.color = self.color_passive
                display.blit(self.child_id_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
                self.input_rect.w = max(100, self.child_id_surface.get_width() + 10)

    def next_line(self):
        self.final_text = self.final_text + self.user_text
        self.temp_text4 = self.temp_text3
        self.temp_text4_rec.x = 220
        self.temp_text4_rec.y += 30
        self.temp_text3 = self.temp_text2
        self.temp_text3_rec.x = 220
        self.temp_text3_rec.y += 30
        self.temp_text2 = self.temp_text1
        self.temp_text2_rec.x = 220
        self.temp_text2_rec.y += 30
        self.temp_text1 = self.user_text
        self.temp_text1_rec.x = 220
        self.temp_text1_rec.y += 30
        self.temp_text1_surface = self.base_font.render(self.temp_text1, True, 'Black')
        self.temp_text2_surface = self.base_font.render(self.temp_text2, True, 'Black')
        self.temp_text3_surface = self.base_font.render(self.temp_text3, True, 'Black')
        self.temp_text4_surface = self.base_font.render(self.temp_text4, True, 'Black')
        self.user_text = ''
        self.user_text_surface = self.base_font.render(self.user_text, True, 'Black')
        self.user_text_rec.x = 220
        self.user_text_rec.y += 30
