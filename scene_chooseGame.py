import pygame.event
from random import randint
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button, CycleButton

# Scene's Constants:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEADER_SIZE = 80
SYSTEMLOGO_SIZE = 70


class GameIcon:
    """ A small game's icon to show on the menu. """

    def __init__(self, fileName, caption, position: tuple, func, newSceneName):
        """ Initialize the game's icon.

        :param fileName:        The name of the image file.
        :param caption:         A small text to be shown below the icon.
        :param position:        The position of the icon.
        :param func:            The function to change scene.
        :param newSceneName     The name of the new scene to be showed when click on this icon.
        """
        self.img = pygame.image.load("images/Game's Icons/{0}".format(fileName))
        self.img = pygame.transform.smoothscale(self.img, (150, 150))
        self.position = position
        self.caption = Text((self.position[0] + 150 / 2, self.position[1] + 150 + 15), WHITE, caption, 24,
                            "fonts/defaultFont.ttf")
        self.func = func
        self.newSceneName = newSceneName
        GameIcon.clickable = True  # Indicates whether the button is clickable or not (STATIC field for all of the objects)

    def update(self):
        mousePos = pygame.mouse.get_pos()
        isHover = self.position[0] < mousePos[0] < (self.position[0] + 150) and \
                  self.position[1] < mousePos[1] < (self.position[1] + 150)

        if isHover:
            self.img.set_alpha(100)
        else:
            self.img.set_alpha(255)

        if pygame.mouse.get_pressed()[0]:
            if isHover and GameIcon.clickable:
                Button.clickable = False
                self.func(self.newSceneName)
        else:  # Prevent the button to be double clicked on the same user's click
            GameIcon.clickable = True

    def draw(self, display):
        display.blit(self.img, (self.position[0], self.position[1]))
        self.caption.draw(display)


class ChooseGame(Scene):
    def __init__(self, display: Surface, userId: str):
        """ Initialize the scene.

        :param display:             The display where to draw the scene.
        :param userId:              User's id. (string)
        """
        import main  # Import main to get access to changeScene function (and avoid circular import)
        super().__init__(display)

        def goToScene(args: tuple):
            """ Change to another scene.

            :param args:            What scene needs to be displayed next.
            """
            if args[0] == "game_mathExp":
                mode = self.gameMode.getText()
                if mode == "+":
                    args = ("game_mathExp_plus", args[1])
                elif mode == "-":
                    args = ("game_mathExp_minus", args[1])
                else:
                    args = ("game_mathExp_power", args[1])

            main.changeScene(args[0], args[1])

        def playRandom():
            """ Play a random game. """
            generatedGame = randint(0, 5)
            if generatedGame == 0:
                goToScene(("game_catchGame", self.userId))
            elif generatedGame == 1:
                goToScene(("game_chooseSize", self.userId))
            elif generatedGame == 2:
                goToScene(("game_mathExp_power", self.userId))
            elif generatedGame == 3:
                goToScene(("game_mathExp_plus", self.userId))
            elif generatedGame == 4:
                goToScene(("game_mathExp_minus", self.userId))
            else:
                goToScene(("game_countGame", self.userId))

        screenSize = display.get_size()
        self.userId = userId

        self.background = pygame.transform.scale(pygame.image.load("images/Login Scene/blue_background.jpg"),
                                                 (screenSize[0], screenSize[1]))
        self.background.set_alpha(120)
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (200, 200, 200), "Choose a Game", 36,
                              "fonts/defaultFont.ttf")
        self.btnBack = Button((screenSize[0] - 210, screenSize[1] - 80, 200, 70),
                              ((0, 46, 77), (0, 77, 128)), "Back", "fonts/defaultFont.ttf",
                              28, goToScene, ("mainMenu", self.userId))
        self.btnRandom = Button((screenSize[0] / 2 - 110, screenSize[1] - 110, 220, 50),
                                ((0, 46, 77), (0, 77, 128)), "Random Game", "fonts/defaultFont.ttf",
                                28, playRandom, None)

        self.btnGame = [
            GameIcon("catch answer icon.jpg", "Catch the Answer", (100, HEADER_SIZE + 20), goToScene,
                     ("game_catchGame", self.userId)),
            GameIcon("math expressions icon.png", "Math Expressions", (350, HEADER_SIZE + 20), goToScene,
                     ("game_mathExp", self.userId)),
            GameIcon("choose size icon.png", "Choose Size", (600, HEADER_SIZE + 20), goToScene,
                     ("game_chooseSize", self.userId)),
            GameIcon("count game icon.png", "Count Game", (100, HEADER_SIZE + 250), goToScene,
                     ("game_countGame", self.userId))
        ]

        self.gameModeText = Text((350, HEADER_SIZE + 20 + 180), (200, 200, 200), "Game Mode:", 16,
                                 "fonts/defaultFont.ttf", alignCenter=False)
        self.gameMode = CycleButton((450, HEADER_SIZE + 20 + 180, 20, 20), ((0, 46, 77), (0, 77, 128)), ("+", "-", "*"),
                                    "fonts/defaultFont.ttf", 18)

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.userId

        self.btnBack.update()
        self.btnRandom.update()
        self.gameMode.update()
        for btn in self.btnGame:
            btn.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill(BLACK)
        display.blit(self.background, (0, 0))
        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))
        display.blit(self.systemLogo, (display.get_size()[0] - SYSTEMLOGO_SIZE - 10, 10))
        self.titleText.draw(display)
        self.gameModeText.draw(display)

        for btn in self.btnGame:
            btn.draw(display)

        self.btnBack.draw(display)
        self.btnRandom.draw(display)
        self.gameMode.draw(display)
