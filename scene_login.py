import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button, TextInput
import database

# Scene's Constants:
BACKGROUND_COLOR = (0, 128, 255)
TITLE_COLOR = (76, 0, 153)

REGISTER_FORM = [
    "First Name",
    "Last Name",
    "ID",
    "Password",
    "Account Type"
]


class LoginScene(Scene):
    def __init__(self, display: Surface):
        """ Initialize the scene. """
        super().__init__(display)

        def changeState(newState):
            for index in range(1, len(self.inputForm), 2):
                self.inputForm[index].clearText()
            self.state = newState

        def makeRegistration(text: tuple):
            """ Make the registration! Check for input's validation first.
            Valid input = names only letters, ID only digits, ID doesn't exist already.

            :param text:            A tuple which each element represents an input.
            """
            if text[0].getText().isalpha() and text[1].getText().isalpha() and \
                    text[2].getText().isdigit() and not database.isIdExists(text[2].getText()):
                # All input are valid!
                database.addUser(text[0].getText(), text[1].getText(), text[2].getText(), text[3].getText(),
                                 text[4].getText())
                changeState("title")
            else:
                pass  # NEED TO MAKE ERROR MESSAGE HERE

        self.state = "title"  # Scene's states: title, register, login
        screenSize = display.get_size()

        # Title screen ui components:
        self.title = [Text((screenSize[0] / 2, screenSize[1] / 5), TITLE_COLOR,
                           "The Math Path", 56, "fonts/defaultFont.ttf"),
                      Text((screenSize[0] / 2, screenSize[1] / 3.8), (0, 0, 0),
                           "Secondary Title", 24, "fonts/defaultFont.ttf")]
        self.btnLogin = Button((screenSize[0] / 4, screenSize[1] / 2, 200, 70), ((0, 46, 77), (0, 77, 128)),
                               "Login", "fonts/defaultFont.ttf", 28, changeState, "login")
        self.btnRegister = Button((screenSize[0] * 0.75 - 200, screenSize[1] / 2, 200, 70), ((0, 46, 77), (0, 77, 128)),
                                  "Register", "fonts/defaultFont.ttf", 28, changeState, "register")
        self.btnBack = Button((screenSize[0] - 200 - 20, screenSize[1] - 70 - 20, 200, 70), ((0, 46, 77), (0, 77, 128)),
                              "Back", "fonts/defaultFont.ttf", 28, changeState, "title")

        # Register screen ui components:
        x = screenSize[0] / 2
        y = (screenSize[1] / 3.8) * 1.3
        self.inputForm = []
        for i in range(5):
            self.inputForm.append(Text((x, y), (0, 0, 0), REGISTER_FORM[i], 24, "fonts/defaultFont.ttf"))
            y += 20
            if REGISTER_FORM[i] == "Password":
                self.inputForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf", secret=True))
            else:
                self.inputForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf"))
            y += 60

        self.registerButton = Button((x, y, 200, 70), ((0, 46, 77), (0, 77, 128)), "Register", "fonts/defaultFont.ttf",
                                     28, makeRegistration, (
                                         self.inputForm[1], self.inputForm[3], self.inputForm[5],
                                         self.inputForm[7], self.inputForm[9]))

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                for i in range(1, len(self.inputForm), 2):
                    self.inputForm[i].updateText(event)

        # Update rest of the scene:
        if self.state == "title":
            self.btnLogin.update()
            self.btnRegister.update()
        elif self.state == "register":
            self.btnBack.update()
            self.registerButton.update()
            for form in self.inputForm:
                form.update()
        elif self.state == "login":
            self.btnBack.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene. """
        display.fill(BACKGROUND_COLOR)

        for title in self.title:
            title.draw(display)

        if self.state == "title":
            self.btnLogin.draw(display)
            self.btnRegister.draw(display)
        elif self.state == "register":
            self.btnBack.draw(display)
            self.registerButton.draw(display)
            for form in self.inputForm:
                form.draw(display)
        elif self.state == "login":
            self.btnBack.draw(display)
