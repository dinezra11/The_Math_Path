import pygame
from scene import Scene
from uiComponents import Text, Button
from database import getScore

# Scene's Constants:
HEADER_SIZE = 80
SYSTEMLOGO_SIZE = 70


class View:
    """ A class that represents a single view for a single score entry. """

    def __init__(self, position: tuple, size: tuple, data):
        """ Initialize the View.

        :param position:        The (x, y) position of the view's box.
        :param size:            The size of the view's box.
        :param data:            The data from the database that needs to be shown.
        """
        self.position = position
        self.size = size

        recordTime = data["time"].split()
        self.text = [
            Text((position[0] + 5, position[1] + 2), (0, 0, 0), recordTime[0], 14,
                 "fonts/defaultFont.ttf", alignCenter=False),  # Date
            Text((position[0] + 5, position[1] + 22), (0, 0, 0), recordTime[1][:8], 14,
                 "fonts/defaultFont.ttf", alignCenter=False),  # Time
            Text((position[0] + 5, position[1] + size[1] - 38), (0, 0, 0), "Game: {}".format(data["type"]), 14,
                 "fonts/defaultFont.ttf", alignCenter=False),  # Game's Name
            Text((position[0] + 5, position[1] + size[1] - 20), (0, 0, 0), "Score: {}".format(data["score"]), 14,
                 "fonts/defaultFont.ttf", alignCenter=False)  # Score
        ]

        iconPath = "images/Game's Icons"
        if data["type"] == "Catch the Answer":
            iconPath += "/catch answer icon.jpg"
        elif data["type"] == "Choose Size":
            iconPath += "/choose size icon.png"
        elif data["type"] == "Math Expressions":
            iconPath += "/math expressions icon.png"
        elif data["type"] == "Count Game":
            iconPath += "/count game icon.png"
        else:
            iconPath += "/notFound.jpg"  # Default icon image, in case of wrongly game's name
        self.image = pygame.transform.scale(pygame.image.load(iconPath), (size[1] - 10, size[1] - 10))
        self.image.set_alpha(90)
        self.background = pygame.Surface((size[0], size[1]))
        self.background.set_alpha(55)
        self.background.fill((255, 255, 255))

    def draw(self, display):
        """ Draw the View. """
        # Draw background (and borders) of View
        display.blit(self.background, self.position)
        pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1], self.size[0], self.size[1]), width=2)

        # Draw image (and borders)
        display.blit(self.image, (self.position[0] + self.size[0] - (self.size[1] - 5), self.position[1] + 5))
        pygame.draw.rect(display, (0, 0, 0),
                         (self.position[0] + self.size[0] - (self.size[1] - 5), self.position[1] + 5, self.size[1] - 10,
                          self.size[1] - 10), width=1)

        # Draw the data as a text on the view's box
        for txt in self.text:
            txt.draw(display)


class ViewScores(Scene):
    def __init__(self, display, userId):
        """ Initialize the scene.

        :param:     display -> The display where to draw the scene.
        """
        import main  # Import main to get access to changeScene function (and avoid circular import)
        super().__init__(display)

        def goToScene(args: tuple):
            """ Change to another scene.

            :param args:            What scene needs to be displayed next.
            """
            main.changeScene(args[0], args[1])

        def nextPage(action):
            """ Go to next or previous page, according to 'action' parameter. """
            if action == "next":
                self.currentPage += 1
            else:
                self.currentPage -= 1

            # Keep currentPage in the correct limit
            if self.currentPage < 0:
                self.currentPage = 0
            elif len(self.views) < self.currentPage * 5:
                self.currentPage -= 1

        screenSize = display.get_size()

        # Background's Initialize
        if type(userId) is not tuple:
            self.userId = userId  # The scene will show the scores of this specific user
            self.returnID = userId
            self.background = pygame.transform.scale(pygame.image.load("images/Login Scene/blue_background.jpg"),
                                                     (screenSize[0], screenSize[1]))
        else:
            self.userId = userId[0]
            self.returnID = userId[1]
            self.background = pygame.transform.scale(pygame.image.load("images/Login Scene/purple_background.jpg"),
                                                     (screenSize[0], screenSize[1]))
        self.background.set_alpha(180)
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (200, 200, 200), "Game Scores Statistics",
                              36, "fonts/defaultFont.ttf")
        self.currentPage = 0
        self.buttons = [
            Button((screenSize[0] - 200 - 20, screenSize[1] - 90, 200, 70), ((0, 46, 77), (0, 77, 128)), "Back",
                   "fonts/defaultFont.ttf", 28, goToScene, ("mainMenu", self.returnID)),
            Button((screenSize[0] - 55, screenSize[1] / 2, 50, 50), ((0, 46, 77), (0, 77, 128)), "->",
                   "fonts/defaultFont.ttf", 28, nextPage, "next"),
            Button((5, screenSize[1] / 2, 50, 50), ((0, 46, 77), (0, 77, 128)), "<-", "fonts/defaultFont.ttf", 28,
                   nextPage, "previous")
        ]

        # Initialize data from DB
        data = getScore(self.userId)  # Get the scores of this user from the database
        viewBoxSize = (screenSize[0] * 0.75, screenSize[1] / 8)
        self.views = []
        if data is not None:
            xPos = (screenSize[0] - viewBoxSize[0]) / 2
            startYpos = yPos = HEADER_SIZE + 20
            for d in data:
                if yPos >= startYpos + 5 * (viewBoxSize[1] + 5):
                    yPos = startYpos

                self.views.append(View((xPos, yPos), viewBoxSize, d))
                yPos += viewBoxSize[1] + 5

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.returnID

        self.buttons[0].update()
        if len(self.views) > (self.currentPage + 1) * 5:
            self.buttons[1].update()
        if self.currentPage != 0:
            self.buttons[2].update()

        return True  # Continue with the game's loop

    def draw(self, display: pygame.Surface):
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

        # Draw Data
        for i in range(self.currentPage * 5, (self.currentPage + 1) * 5):
            if i >= len(self.views):
                break

            self.views[i].draw(display)

        # Draw Buttons
        self.buttons[0].draw(display)
        if len(self.views) > (self.currentPage + 1) * 5:
            self.buttons[1].draw(display)
        if self.currentPage != 0:
            self.buttons[2].draw(display)
