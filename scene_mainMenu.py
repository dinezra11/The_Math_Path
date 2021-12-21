import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button
import database

# Scene's Constants:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEADER_SIZE = 80
FOOTER_SIZE = 160
SYSTEMLOGO_SIZE = 70


class MainMenu(Scene):
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
            main.changeScene(args[0], args[1])

        screenSize = display.get_size()
        self.userObj = database.getUser(userId)  # Get the relevant user's details from the database

        # Background and graphics initialize
        if self.userObj[1]["type"] == "Parent":
            backColor = "images/Login Scene/purple_background.jpg"
        elif self.userObj[1]["type"] == "Diagnostic":
            backColor = "images/Login Scene/red_background.jpg"
        else:
            backColor = "images/Login Scene/blue_background.jpg"
        self.background = pygame.transform.scale(pygame.image.load(backColor),
                                                 (screenSize[0], screenSize[1]))
        self.background.set_alpha(180)
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))

        # UI Components initialize
        title = "Welcome {0} {1}".format(self.userObj[1]["name"], self.userObj[1]["last"])
        details = [
            "User's Information:",
            "   First Name: {0}".format(self.userObj[1]["name"]),
            "   Last Name: {0}".format(self.userObj[1]["last"]),
            "   ID: {0}".format(self.userObj[0]),
            "   Account Type: {0}".format(self.userObj[1]["type"]),
            "",
            "   'Link to Parent' code: {0}".format(self.userObj[1]["passlink"])
        ]
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (60, 100, 80), title, 36,
                              "fonts/defaultFont.ttf")
        self.detailsText = []
        x = 10
        y = HEADER_SIZE * 2
        for item in details:
            self.detailsText.append(Text((x, y), BLACK, item, 20, "fonts/defaultFont.ttf", alignCenter=False))
            y += 27

        self.btnLogOff = Button((screenSize[0] - 130, screenSize[1] - FOOTER_SIZE / 2, 120, 70),
                                ((0, 46, 77), (0, 77, 128)), "Log Off", "fonts/defaultFont.ttf",
                                28, goToScene, ("start", None))

        # Initialize menu buttons:
        btnSize = (190, 30)
        spaceBetweenBtns = 20
        self.btnChooseGame = Button(
            (screenSize[0] / 2 - btnSize[0] * 1.5 - spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
            ((0, 46, 77), (0, 77, 128)), "Play a Game", "fonts/defaultFont.ttf", 18, goToScene,
            ("chooseGame", self.userObj[0]))
        self.btnScores = Button((screenSize[0] / 2 - btnSize[0] / 2, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                                ((0, 46, 77), (0, 77, 128)),
                                "Game's Scores", "fonts/defaultFont.ttf", 18, goToScene,
                                ("viewScores", self.userObj[0]))
        self.btnReviews = Button(
            (screenSize[0] / 2 + btnSize[0] / 2 + spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
            ((0, 46, 77), (0, 77, 128)), "Diagnostic's Reviews", "fonts/defaultFont.ttf", 18, goToScene,
            ('viewMessages', self.userObj[0]))

        # Initialize help and info contents:
        if self.userObj[1]["type"] == "Child":
            userHelp = [
                'As a user, you can choose and play any game you wish from the system.',
                'Press on "Play a Game" button to go to the game selection screen. Your score will be saved after you '
                'finish a game.',
                '',
                r"""You can watch your recent game's scores or the reviews from the diagnostics by pressing the"""
                "buttons at the top.",
                "",
                'Let your parent use your unique "Link to Parent" code so he can link your account to his account.'
            ]
        else:
            userHelp = []

        # Make the text objects for the help and info:
        self.infoText = []
        y = display.get_size()[1] - FOOTER_SIZE
        for i in userHelp:
            self.infoText.append(Text((10, y), BLACK, i, 16, "fonts/defaultFont.ttf",
                                      alignCenter=False))
            y += 20

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.btnChooseGame.update()
        self.btnScores.update()
        self.btnReviews.update()
        self.btnLogOff.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill((0, 0, 0))
        display.blit(self.background, (0, 0))

        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))
        display.blit(self.systemLogo, (display.get_size()[0] - SYSTEMLOGO_SIZE - 10, 10))
        self.titleText.draw(display)

        # Draw Middle
        for item in self.detailsText:
            item.draw(display)

        self.btnChooseGame.draw(display)
        self.btnScores.draw(display)
        self.btnReviews.draw(display)
        self.btnLogOff.draw(display)

        # Draw Footer
        pygame.draw.rect(display, (0, 0, 0),
                         (5, display.get_size()[1] - FOOTER_SIZE - 5, display.get_size()[0] - 10, FOOTER_SIZE), width=2)
        for info in self.infoText:
            info.draw(display)
