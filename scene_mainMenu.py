import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button, TextInput, ImageButton
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
            if len(args) == 3:
                main.changeScene(args[0], (args[1], args[2]))
            else:
                main.changeScene(args[0], args[1])

        screenSize = display.get_size()
        self.userObj = database.getUser(userId)  # Get the relevant user's details from the database

        # Mutual account types components initialize:
        title = "Welcome {0} {1}".format(self.userObj[1]["name"], self.userObj[1]["last"])
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (60, 100, 80), title, 36,
                              "fonts/defaultFont.ttf")

        self.btnLogOff = ImageButton((screenSize[0] - 80, screenSize[1] - 75, 70, 60),
                                     "images/Login Scene/LogOut.png", goToScene, ("start", None))
        self.btnFeedback = ImageButton((screenSize[0] - 170, screenSize[1] - 90, 80, 100),
                                       "images/mefateah_feedback/send.png", goToScene,
                                       ("diag_feedback", self.userObj[0]))

        # Initialize screen's view, according to the user's specific account type:
        if self.userObj[1]["type"] == "Child":
            # ----- Initialize CHILD's specific screen components ----- #
            self.backFill = (0, 0, 0)  # The color to be drawn below the background (For transparency effect)
            backColor = "images/Login Scene/blue_background.jpg"

            detailsColor = BLACK
            details = [
                "User's Information:",
                "   First Name: {0}".format(self.userObj[1]["name"]),
                "   Last Name: {0}".format(self.userObj[1]["last"]),
                "   ID: {0}".format(self.userObj[0]),
                "   Account Type: {0}".format(self.userObj[1]["type"]),
                "",
                "   'Link to Parent' code: {0}".format(self.userObj[1]["passlink"])
            ]

            userHelpColor = BLACK  # The color for the help section text
            userHelp = [
                'As a user, you can choose and play any game you wish from the system.',
                'Press on "Play a Game" button to go to the game selection screen. Your score will be saved after you '
                'finish a game.',
                r"""You can watch your recent game's scores or the reviews from the diagnostics by pressing the """
                "buttons at the top.",
                "",
                'Let your parent use your unique "Link to Parent" code so he can link your account to his account.',
                '',
                "You can log off or send a feedback to the game's developers by pressing the icons at the bottom."
            ]

            # Initialize menu buttons:
            btnSize = (190, 30)
            spaceBetweenBtns = 20
            self.buttons = [
                Button(
                    (screenSize[0] / 2 - btnSize[0] * 1.5 - spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                    ((0, 46, 77), (0, 77, 128)), "Play a Game", "fonts/defaultFont.ttf", 18, goToScene,
                    ("chooseGame", self.userObj[0])),
                Button((screenSize[0] / 2 - btnSize[0] / 2, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                       ((0, 46, 77), (0, 77, 128)),
                       "Game's Scores", "fonts/defaultFont.ttf", 18, goToScene,
                       ("viewScores", self.userObj[0])),
                Button(
                    (screenSize[0] / 2 + btnSize[0] / 2 + spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                    ((0, 46, 77), (0, 77, 128)), "Diagnostic's Reviews", "fonts/defaultFont.ttf", 18, goToScene,
                    ('viewMessages', self.userObj[0]))
            ]
        elif self.userObj[1]["type"] == "Parent":
            # ----- Initialize PARENT's specific screen components ----- #
            self.backFill = (200, 200, 200)  # The color to be drawn below the background (For transparency effect)
            backColor = "images/Login Scene/purple_background.jpg"

            # Count children:
            childrenCount = 0
            if self.userObj[1].get("children") is not None:
                childrenCount = len(self.userObj[1].get("children"))

            detailsColor = BLACK
            details = [
                "User's Information:",
                "   First Name: {0}".format(self.userObj[1]["name"]),
                "   Last Name: {0}".format(self.userObj[1]["last"]),
                "   ID: {0}".format(self.userObj[0]),
                "   Account Type: {0}".format(self.userObj[1]["type"]),
                "",
                "   Amount of children: {0}".format(childrenCount)
            ]

            userHelpColor = (200, 0, 200)  # The color for the help section text
            userHelp = [
                "As a parent, you are able to track and view your children's scores and diagnostic's reviews.",
                'Press on "My Children" button view the information about all of your children.',
                'On that screen, you can link a new child to your account using his unique "Link to Parent" code.',
                "",
                "As a parent you can also view a diagnostic's reviews that are written specifically for you.",
                '',
                "You can log off or send a feedback to the game's developers by pressing the icons at the bottom."
            ]

            # Initialize menu buttons:
            btnSize = (190, 30)
            spaceBetweenBtns = 20
            self.buttons = [
                Button(
                    (screenSize[0] / 2 - btnSize[0] * 1.5 - spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                    ((0, 46, 77), (0, 77, 128)), "My Children", "fonts/defaultFont.ttf", 18, goToScene,
                    ("viewChildren", self.userObj)),
                Button(
                    (screenSize[0] / 2 + btnSize[0] / 2 + spaceBetweenBtns, HEADER_SIZE + 10, btnSize[0], btnSize[1]),
                    ((0, 46, 77), (0, 77, 128)), "Diagnostic's Reviews", "fonts/defaultFont.ttf", 18, goToScene,
                    ('viewMessages', self.userObj[0], self.userObj[0]))
            ]
        else:
            # ----- Initialize DIAGNOSTIC's specific screen components ----- #
            self.backFill = (0, 0, 100)  # The color to be drawn below the background (For transparency effect)
            backColor = "images/Login Scene/red_background.jpg"

            # Calculate Statistics:
            self.registeredUsers = database.getAllUsers()
            usersCount = parentsCount = diagCount = 0
            for _, val in self.registeredUsers.items():
                if val["type"] == "Child":
                    usersCount += 1
                elif val["type"] == "Parent":
                    parentsCount += 1
                elif val["type"] == "Diagnostic":
                    diagCount += 1

            detailsColor = (0, 100, 50)
            details = [
                "Diagnostic Interface:",
                "   You are logged in as Dr.{} (id {})".format(self.userObj[1]["last"], self.userObj[0]),
                "",
                "",
                "",
                "General System Statistics:",
                "   Total of diagnostics users: {}".format(diagCount),
                "   Registered regular users: {}".format(usersCount),
                "   Registered parents: {}".format(parentsCount),
                "   Available games to play: 4"
            ]

            userHelpColor = (0, 100, 0)  # The color for the help section text
            userHelp = [
                "As a diagnostic, you have access to the information of all of the users that use the system.",
                'Press on "Search User" to move to the screen where you can find users details and perform operations'
                ' for them.',
                'The available operations are: watch scores, send personal messages and reviews.',
                'Press on "Private Notes" to write and save notes for yourself, or "Add General Advice" to send tips'
                ' and advices',
                'for all of the parents.',
                '',
                "You can log off or send a feedback to the game's developers by pressing the icons at the bottom."
            ]

            # Initialize menu buttons:
            btnSize = (190, 30)
            spaceBetweenBtns = 10
            self.buttons = [
                Button((screenSize[0] - btnSize[0] - 10, HEADER_SIZE + 60, btnSize[0],
                        btnSize[1]), ((0, 46, 77), (0, 77, 128)), "Search User", "fonts/defaultFont.ttf", 18, None,
                       None),
                Button((screenSize[0] - btnSize[0] - 10, HEADER_SIZE + 60 + btnSize[1] + spaceBetweenBtns, btnSize[0],
                        btnSize[1]), ((0, 46, 77), (0, 77, 128)), "Private Notes", "fonts/defaultFont.ttf", 18,
                       goToScene, ("private_notes", self.userObj[0])),
                Button((screenSize[0] - btnSize[0] - 10, HEADER_SIZE + 60 + (btnSize[1] + spaceBetweenBtns) * 2,
                        btnSize[0], btnSize[1]), ((0, 46, 77), (0, 77, 128)), "Add General Advice",
                       "fonts/defaultFont.ttf", 18, goToScene, ("add_tips", self.userObj[0]))
            ]

        # Background and graphics initialize
        self.background = pygame.transform.scale(pygame.image.load(backColor),
                                                 (screenSize[0], screenSize[1]))
        self.background.set_alpha(180)
        self.systemLogo = pygame.transform.scale(
            pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
            (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))

        # Make the details text objects for the center of the screen section:
        self.detailsText = []
        x = 10
        y = HEADER_SIZE * 2
        for item in details:
            self.detailsText.append(Text((x, y), detailsColor, item, 20, "fonts/defaultFont.ttf", alignCenter=False))
            y += 27

        # Make the text objects for the help and info:
        self.infoText = []
        y = display.get_size()[1] - FOOTER_SIZE
        for i in userHelp:
            self.infoText.append(Text((10, y), userHelpColor, i, 16, "fonts/defaultFont.ttf",
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

        for btn in self.buttons:
            btn.update()

        self.btnLogOff.update()
        self.btnFeedback.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill(self.backFill)
        display.blit(self.background, (0, 0))

        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))
        display.blit(self.systemLogo, (display.get_size()[0] - SYSTEMLOGO_SIZE - 10, 10))
        self.titleText.draw(display)

        # Draw Middle
        for item in self.detailsText:
            item.draw(display)

        for btn in self.buttons:
            btn.draw(display)

        self.btnLogOff.draw(display)
        self.btnFeedback.draw(display)

        # Draw Footer
        pygame.draw.rect(display, (0, 0, 0),
                         (5, display.get_size()[1] - FOOTER_SIZE - 5, display.get_size()[0] - 10, FOOTER_SIZE), width=2)
        for info in self.infoText:
            info.draw(display)
