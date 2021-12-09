import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button
import database

# Scene's Constants:
BACKGROUND_COLOR = (102, 51, 0)
HEADER_COLOR = (246, 195, 36)
FOOTER_COLOR = (96, 96, 96)
WHITE = (255, 255, 255)
HEADER_SIZE = 45


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

        title = "Welcome {0} {1}".format(self.userObj[1]["name"], self.userObj[1]["last"])
        details = [
            "First Name: {0}".format(self.userObj[1]["name"]),
            "Last Name: {0}".format(self.userObj[1]["last"]),
            "ID: {0}".format(self.userObj[0])
        ]
        self.titleText = Text((display.get_size()[0] / 2, 20), WHITE, title, 24, "fonts/defaultFont.ttf")
        self.detailsText = []
        x = display.get_size()[0] / 2
        y = HEADER_SIZE * 2
        for item in details:
            self.detailsText.append(Text((x, y), WHITE, item, 24, "fonts/defaultFont.ttf"))
            y += 30

        self.btnChooseGame = self.btnLogin = Button((screenSize[0] - 250, screenSize[1] / 2, 200, 70),
                                                    ((0, 46, 77), (0, 77, 128)), "Play a Game", "fonts/defaultFont.ttf",
                                                    28, goToScene, ("chooseGame", self.userObj[0]))

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.btnChooseGame.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill(BACKGROUND_COLOR)
        display.fill(HEADER_COLOR, (0, 0, display.get_size()[0], HEADER_SIZE))
        display.fill(FOOTER_COLOR, (0, display.get_size()[1] - HEADER_SIZE, display.get_size()[0], HEADER_SIZE))
        self.titleText.draw(display)
        for item in self.detailsText:
            item.draw(display)

        self.btnChooseGame.draw(display)
