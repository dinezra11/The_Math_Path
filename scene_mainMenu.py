import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button
import database

# Scene's Constants:
WHITE = (255, 255, 255)
HEADER_SIZE = 80
FOOTER_SIZE = 160


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
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (70, 70))

        # UI Components initialize
        title = "Welcome {0} {1}".format(self.userObj[1]["name"], self.userObj[1]["last"])
        details = [
            "First Name: {0}".format(self.userObj[1]["name"]),
            "Last Name: {0}".format(self.userObj[1]["last"]),
            "ID: {0}".format(self.userObj[0]),
            "Account Type: {0}".format(self.userObj[1]["type"])
        ]
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), WHITE, title, 36, "fonts/defaultFont.ttf")
        self.detailsText = []
        x = 10
        y = HEADER_SIZE * 2
        for item in details:
            self.detailsText.append(Text((x, y), WHITE, item, 24, "fonts/defaultFont.ttf", alignCenter=False))
            y += 30

        self.btnChooseGame = self.btnLogin = Button((screenSize[0] / 3, HEADER_SIZE + 20, 140, 40),
                                                    ((0, 46, 77), (0, 77, 128)), "Play a Game", "fonts/defaultFont.ttf",
                                                    20, goToScene, ("chooseGame", self.userObj[0]))
        self.btnLogOff = Button((screenSize[0] - 130, screenSize[1] - FOOTER_SIZE / 2, 120, 70),
                                ((0, 46, 77), (0, 77, 128)), "Log Off", "fonts/defaultFont.ttf",
                                28, goToScene, ("start", None))

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.btnChooseGame.update()
        self.btnLogOff.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.blit(self.background, (0, 0))
        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))

        # Draw Middle
        self.titleText.draw(display)
        for item in self.detailsText:
            item.draw(display)

        self.btnChooseGame.draw(display)
        self.btnLogOff.draw(display)

        # Draw Footer
        pygame.draw.rect(display, (0, 0, 0),
                         (5, display.get_size()[1] - FOOTER_SIZE - 5, display.get_size()[0] - 10, FOOTER_SIZE), width=2)
