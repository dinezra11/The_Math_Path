""" Import a user interface component from this python file to use in the game's scenes. """
import pygame


class Button:
    """ Button component """
    def __init__(self, rect: tuple, color: tuple, text: str, fontPath: str, fontSize: int, clickFunc=None,
                 clickArg=None):
        """ Initialize button.

        :param rect:        A tuple that represents the measures of the button. (position and size)
                            [x, y, width, height]
        :param color:       A tuple of tuples, each tuple represents a color. ([normal color, on hover color])
        :param text:        The text to print on the button. (string)
        :param fontPath:    The path to the font file.
        :param fontSize:    The size of the font.
        :param clickFunc:   Function. The button will call this function when it is clicked.
        :param clickArg:    The arguments to send as parameters to the function of clickFun.
        """
        if len(rect) != 4:
            self.rect = (0, 0, 0, 0)  # Default values if the given parameter is invalid (Should be a tuple of 4)
        else:
            self.rect = rect

        if len(color) != 2:
            self.color = ((0, 0, 0), (0, 0, 0))  # Default values if the given parameter is invalid
        else:
            self.color = color

        loadFont = pygame.font.Font(fontPath, fontSize)
        self.text = loadFont.render(text, True, (255, 255, 255))

        # Calculate text position:
        self.textPos = self.text.get_rect()
        self.textPos.center = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)

        self.clickFunc = clickFunc
        self.clickArg = clickArg
        self.isHover = False
        Button.clickable = True  # Indicates whether the button is clickable or not (STATIC field for all of the objects)

    def update(self):
        """ Update method. """
        mousePos = pygame.mouse.get_pos()
        self.isHover = self.rect[0] < mousePos[0] < (self.rect[0] + self.rect[2]) and \
                       self.rect[1] < mousePos[1] < (self.rect[1] + self.rect[3])

        if pygame.mouse.get_pressed()[0] and self.clickFunc is not None:
            if self.isHover and Button.clickable:
                Button.clickable = False
                if self.clickArg is None:
                    self.clickFunc()
                else:
                    self.clickFunc(self.clickArg)
        else:  # Prevent the button to be double clicked on the same user's click
            Button.clickable = True

    def draw(self, display: pygame.display):
        """ Draw method. """
        if self.isHover:
            drawColor = self.color[1]
        else:
            drawColor = self.color[0]

        pygame.draw.rect(display, drawColor, self.rect)
        display.blit(self.text, self.textPos)


class CycleButton(Button):
    """ CycleButton component -> A button for options - each click changes the option. """
    def __init__(self, rect: tuple, color: tuple, options: tuple, fontPath: str, fontSize: int):
        """ Initialize button.

                :param rect:        A tuple that represents the measures of the button. (position and size)
                                    [x, y, width, height]
                :param color:       A tuple of tuples, each tuple represents a color. ([normal color, on hover color])
                :param options:     A tuple of options. (string)
                :param fontPath:    The path to the font file.
                :param fontSize:    The size of the font.
                """
        super().__init__(rect, color, options[0], fontPath, fontSize)

        self.options = options
        self.currentOption = 0
        self.font = pygame.font.Font(fontPath, fontSize)

    def update(self):
        """ Update method. (override) """
        mousePos = pygame.mouse.get_pos()
        self.isHover = self.rect[0] < mousePos[0] < (self.rect[0] + self.rect[2]) and \
                       self.rect[1] < mousePos[1] < (self.rect[1] + self.rect[3])

        if pygame.mouse.get_pressed()[0]:
            if self.isHover and Button.clickable:
                # Button clicked! Change the text:
                Button.clickable = False
                self.currentOption += 1
                if self.currentOption >= len(self.options):
                    self.currentOption = 0

                self.text = self.font.render(self.options[self.currentOption], True, (255, 255, 255))
        else:  # Prevent the button to be double clicked on the same user's click
            Button.clickable = True

    def getText(self):
        return self.options[self.currentOption]


class Text:
    """ Text component """
    def __init__(self, position: tuple, color: tuple, text: str, size: int = 12, fontPath: str = None):
        """ Initialize text.

        :param position:        A tuple that represents the position of the text. (x, y)
        :param color:           The color of the text. (Represented as (R,G,B))
        :param text:            The text to print. (string)
        :param size:            Size of the font. (int) (Default = 12px)
        :param fontPath:        Path to the font. (string) (Default = system's default font)
        """
        loadFont = pygame.font.Font(fontPath, size)

        self.text = loadFont.render(text, True, color)
        self.position = self.text.get_rect()
        self.position.center = position

    def update(self):
        """ Update method. """
        pass

    def draw(self, display: pygame.display):
        display.blit(self.text, self.position)


class TextInput:
    """ TextInput component """
    def __init__(self, position: tuple, size: int = 12, fontPath: str = None, secret=False):
        """ Initialize text input.

        :param position:        A tuple that represents the position of the text input field.
                                        (x, y)
        :param size:            Size of the font. (int) (Default = 12px)
        :param fontPath:        Path to the font. (string) (Default = system's default font)
        :param secret:          Indicates whether the text should be hidden or not.
                                For example: pass
        """
        self.font = pygame.font.Font(fontPath, size)
        self.textStr = ""
        self.textRender = self.font.render(self.textStr, True, (0, 0, 0))
        self.rect = (position[0], position[1], 200, self.font.size("   ")[1])

        self.isActive = False
        self.isSecret = secret

    def update(self):
        """ Update method. """
        mousePos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            isHover = self.rect[0] < mousePos[0] < (self.rect[0] + self.rect[2]) and \
                      self.rect[1] < mousePos[1] < (self.rect[1] + self.rect[3])
            if isHover:
                self.isActive = True
            else:
                self.isActive = False

    def updateText(self, key):
        if self.isActive:
            if key.key == pygame.K_BACKSPACE:
                self.textStr = self.textStr[:-1]
            else:
                key = key.unicode
                if ('a' <= key.lower() <= 'z') or ('0' <= key <= '9') or (key in "!@#$%^&*"):
                    self.textStr += key

            if self.isSecret:
                # Draw only * instead of real text:
                secretText = ""
                for i in range(len(self.textStr)):
                    secretText += "*"
                self.textRender = self.font.render(secretText, True, (0, 0, 0))
            else:
                # Draw the text:
                self.textRender = self.font.render(self.textStr, True, (0, 0, 0))

    def clearText(self):
        self.textStr = ""
        self.textRender = self.font.render("", True, (0, 0, 0))

    def getText(self):
        return self.textStr

    def draw(self, display: pygame.Surface):
        """ Draw method. """
        pygame.draw.rect(display, (255, 255, 255), self.rect)  # Draw the input's box
        if self.isActive:
            pygame.draw.rect(display, (0, 0, 0), self.rect, width=2)  # Draw the box's border, only if it is active

        display.blit(self.textRender, self.rect)
