import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button, TextInput, CycleButton, ErrorText
import database
import random

# Scene's Constants:
TITLE_COLOR = (76, 0, 153)  # Title text color (RGB)
ERROR_DELAY = 1000  # Error display time (in milliseconds)

REGISTER_FORM = [
    "First Name",
    "Last Name",
    "ID",
    "Password",
    "Account Type"
]
LOGIN_FORM = [
    "ID",
    "Password"
]


class CloudObject:
    """ This class represents a single cloud object. The cloud should 'levitate' on the screen.
    Used for graphics and UI purposes. """

    def __init__(self, displaySize: tuple):
        CloudObject.displaySize = displaySize
        CloudObject.image = pygame.image.load('images/Login Scene/cloud.png')
        self.img = self.speed = self.position = None
        self.randomInit()

    def randomInit(self, firstInit=True):
        scale = random.randrange(4, 10)
        self.img = pygame.transform.scale(CloudObject.image, (840 / scale, 859 / scale))
        self.speed = random.randrange(1, 5)
        if firstInit:
            # First init - random position
            self.position = (random.randrange(0, CloudObject.displaySize[0]),
                             random.randrange(0, CloudObject.displaySize[1] // 3))
        else:
            # Renewed cloud - random Y coordinate (X is fixed)
            self.position = (-self.img.get_size()[1], random.randrange(0, CloudObject.displaySize[1] // 3))

    def update(self):
        self.position = (self.position[0] + self.speed, self.position[1])

        if self.position[0] >= CloudObject.displaySize[0]:
            self.randomInit(False)

    def draw(self, display: Surface):
        display.blit(self.img, self.position)


class ArithmeticObject:
    """ This class represents a single arithmetic object. This object should appear and dissapear on the screen.
    Used for graphics and UI purposes. """

    def __init__(self, displaySize: tuple):
        ArithmeticObject.displaySize = displaySize
        self.font = self.text = self.position = self.alpha = self.alphaChange = self.active = None
        self.randomInit()

    def randomInit(self):
        item = random.randrange(0, 14)
        if item == 10:
            item = '+'
        elif item == 11:
            item = '-'
        elif item == 12:
            item = '*'
        elif item == 13:
            item = '%'
        self.font = pygame.font.Font('fonts/defaultFont.ttf', random.randrange(50, 120))
        self.text = self.font.render(str(item), True,
                                     (random.randrange(100, 255), random.randrange(100, 255),
                                      random.randrange(100, 255)))
        self.position = (random.randrange(50, ArithmeticObject.displaySize[0] - 50),
                         random.randrange(50, ArithmeticObject.displaySize[1] - 50))
        self.alpha = 0
        self.text.set_alpha(0)
        self.alphaChange = random.randrange(2, 10)
        self.active = True

    def update(self):
        self.alpha += self.alphaChange
        self.text.set_alpha(self.alpha)

        if self.alpha >= 255:
            self.alphaChange *= -1
        if self.alpha < 0:
            self.active = False
            self.randomInit()

    def draw(self, display: Surface):
        if self.active:
            display.blit(self.text, self.position)


class LoginScene(Scene):
    def __init__(self, display: Surface):
        """ Initialize the scene. """
        import main  # Import main to get access to changeScene function (and avoid circular import)
        super().__init__(display)

        def changeState(newState):
            for index in range(1, len(self.inputForm) - 2, 2):
                self.inputForm[index].clearText()
            self.state = newState

        def makeRegistration(text: tuple):
            """ Make the registration! Check for input's validation first.
            Valid input = names only letters, ID only digits, ID doesn't exist already.

            :param text:            A tuple which each element represents an input.
            """
            try:
                if not text[0].getText().isalpha():
                    raise ValueError("First name must only contain letters.")
                if not text[1].getText().isalpha():
                    raise ValueError("Last name must only contain letters.")
                if not text[2].getText().isdigit():
                    raise ValueError("ID must only contain digits.")
                if database.isIdExists(text[2].getText()):
                    raise ValueError("A user with this ID already registered to the system. Please login.")

                # No exception raised - All input are valid!
                database.addUser(text[0].getText(), text[1].getText(), text[2].getText(), text[3].getText(),
                                 text[4].getText())
                changeState("title")
            except ValueError as ve:
                self.errorObj.pop(str(ve), ERROR_DELAY)  # Pop error message
            except Exception:
                self.errorObj.pop("Connection Error! Please check internet connection.", ERROR_DELAY)
            else:
                # No exception raised after adding user - create "good" error message:
                self.errorObj.pop("Account registered successfully! :)", ERROR_DELAY)

        def attemptLogin(text: tuple):
            """ Attempt to login! Check for input's validation first.
            Valid input = ID only digits.

            :param text:            A tuple which each element represents an input.
            """
            try:
                if text[0].getText() == "" or text[1].getText() == "":
                    raise ValueError("Please fill all the fields before submit.")
                if not text[0].getText().isdigit():
                    raise ValueError("ID must be digits only.")
                if not database.isIdExists(text[0].getText()):
                    raise ValueError("No user with this ID exists. Please register first.")
                if database.validateLogin(text[0].getText(), text[1].getText()):
                    # All input valid! Logged in. Move to the next scene:
                    main.changeScene("mainMenu", text[0].getText())
                else:
                    raise ValueError("The ID and password don't match.")
            except ValueError as ve:
                self.errorObj.pop(str(ve), ERROR_DELAY)  # Pop error message
            except Exception:
                self.errorObj.pop("Connection Error! Please check internet connection.", ERROR_DELAY)

        self.state = "title"  # Scene's states: title, register, login
        screenSize = display.get_size()

        # Create Error Message object:
        self.errorObj = ErrorText((screenSize[0] / 2, 20), 24, "fonts/defaultFont.ttf")

        # Background's graphics:
        self.background = pygame.transform.scale(pygame.image.load('images/Login Scene/blue_background.jpg'),
                                                 (screenSize[0], screenSize[1]))
        self.foregroundGrass = pygame.transform.scale(pygame.image.load('images/Login Scene/grass.png'),
                                                      (screenSize[0], screenSize[1] / 2))
        self.foregroundArithmetic = []
        for i in range(3):
            self.foregroundArithmetic.append(ArithmeticObject(screenSize))
        self.foregroundClouds = []
        for i in range(5):
            self.foregroundClouds.append(CloudObject(screenSize))

        # Title screen ui components:
        self.title = [Text((screenSize[0] / 2, screenSize[1] / 5), TITLE_COLOR,
                           "The Math Path", 80, "fonts/defaultFont.ttf"),
                      Text((screenSize[0] / 2, screenSize[1] / 3.8), (0, 0, 0),
                           "A system for dealing with Dyscalculia", 24, "fonts/defaultFont.ttf")]
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

            if i == 4:  # Last element in the form will be a cycling button:
                self.inputForm.append(CycleButton((x - 100, y, 200, 70), ((0, 46, 77), (0, 77, 128)),
                                                  ("Child", "Parent", "Tutor"), "fonts/defaultFont.ttf", 28))
            else:
                if REGISTER_FORM[i] == "Password":
                    self.inputForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf", secret=True))
                else:
                    self.inputForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf"))

            y += 60

        self.registerButton = Button((x - 100, y + 20, 200, 70), ((0, 46, 77), (0, 77, 128)), "Register",
                                     "fonts/defaultFont.ttf", 28, makeRegistration, (
                                         self.inputForm[1], self.inputForm[3], self.inputForm[5], self.inputForm[7],
                                         self.inputForm[9]))

        # Login screen ui components:
        x = screenSize[0] / 2
        y = (screenSize[1] / 3.8) * 1.3
        self.loginForm = []
        for i in range(2):
            self.loginForm.append(Text((x, y), (0, 0, 0), LOGIN_FORM[i], 24, "fonts/defaultFont.ttf"))
            y += 20

            if LOGIN_FORM[i] == "Password":
                self.loginForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf", secret=True))
            else:
                self.loginForm.append(TextInput((x - 100, y), 24, "fonts/defaultFont.ttf"))

            y += 60

        self.loginButton = Button((x - 100, y + 20, 200, 70), ((0, 46, 77), (0, 77, 128)), "Login",
                                  "fonts/defaultFont.ttf", 28, attemptLogin, (self.loginForm[1], self.loginForm[3]))

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                for i in range(1, len(self.inputForm) - 2, 2):
                    self.inputForm[i].updateText(event)
                for i in range(1, len(self.loginForm), 2):
                    self.loginForm[i].updateText(event)

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
            self.loginButton.update()
            for form in self.loginForm:
                form.update()

        # Update Error Object:
        self.errorObj.update()

        # Update Foreground Animations:
        for i in self.foregroundArithmetic:
            i.update()
        for cloud in self.foregroundClouds:
            cloud.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene. """
        display.blit(self.background, (0, 0))
        display.blit(self.foregroundGrass, (0, display.get_size()[1] - self.foregroundGrass.get_size()[1]))
        for i in self.foregroundArithmetic:
            i.draw(display)
        for cloud in self.foregroundClouds:
            cloud.draw(display)

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
            self.loginButton.draw(display)
            for form in self.loginForm:
                form.draw(display)

        # Draw Error Object:
        self.errorObj.draw(display)
