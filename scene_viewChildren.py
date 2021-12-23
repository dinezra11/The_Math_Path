import pygame
from scene import Scene
from uiComponents import Text, TextInput, Button, ImageButton
from database import addChildToParent

# Scene's Constants:
HEADER_SIZE = 80
SYSTEMLOGO_SIZE = 70
WHITE = (255, 255, 255)


class View:
    """ A class that represents a single view for a single child entry. """

    def __init__(self, position: tuple, size: tuple, data, goToScene, parentId):
        """ Initialize the View.

        :param position:        The (x, y) position of the view's box.
        :param size:            The size of the view's box.
        :param data:            The data from the database that needs to be shown.
        :param goToScene:       The function that change scenes.
        :param parentId:        The id of the parent the engaged this screen.
        """
        self.position = position
        self.size = size

        self.text = [
            Text((position[0] + 5, position[1] + 2), (0, 0, 0), "{}".format(data["full_name"]), 14,
                 "fonts/defaultFont.ttf", alignCenter=False),  # Name
        ]

        btnSize = size[1] / 2
        self.btnScores = ImageButton(
            (position[0] + size[0] - btnSize - 5, position[1] + size[1] - btnSize - 5, btnSize, btnSize),
            "images/viewChildren Scene icons/scores icon.png", goToScene, ("viewScores", data["id"], parentId))
        self.btnMessages = ImageButton(
            (position[0] + size[0] - btnSize * 2 - 10, position[1] + size[1] - btnSize - 5, btnSize, btnSize),
            "images/viewChildren Scene icons/messages icon.png", goToScene, ("viewMessages", data["id"], parentId))

        self.background = pygame.Surface((size[0], size[1]))
        self.background.set_alpha(55)
        self.background.fill((255, 255, 255))

    def update(self):
        """ Update view's buttons. """
        self.btnScores.update()
        self.btnMessages.update()

    def draw(self, display):
        """ Draw the View. """
        # Draw background (and borders) of View
        display.blit(self.background, self.position)
        pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1], self.size[0], self.size[1]), width=2)

        # Draw buttons Icons:
        self.btnScores.draw(display)
        self.btnMessages.draw(display)

        # Draw the data as a text on the view's box
        for txt in self.text:
            txt.draw(display)


class ViewChildren(Scene):
    def __init__(self, display, userDict):
        """ Initialize the scene.

        :param display:         The display where to draw the scene.
        :param userDict:        The dictionary of the current user's data.
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

        def initializeChildList():
            # Initialize list of children
            data = []
            self.views = []

            if userDict[1].get("children") is None:
                return

            for _, child in userDict[1].get("children").items():  # Get the children of this user
                data.append(child)
            viewBoxSize = (180, 60)
            if data is not None:
                startX = xPos = 50
                yPos = HEADER_SIZE + 80
                for d in data:
                    self.views.append(View((xPos, yPos), viewBoxSize, d, goToScene, self.userDict[0]))

                    xPos += viewBoxSize[0] + 5
                    if xPos > startX + (viewBoxSize[0] + 5) * 2:
                        xPos = startX
                        yPos += viewBoxSize[1] + 10

        def addChild():
            """ Attempt to add a child to a parent's account!
            Check if the link password is valid to the child's ID. """
            if self.inputForm[2].getText() == "" or self.inputForm[4].getText() == "":
                return  # Do nothing if the form isn't fully filled

            amountOfChildren = 0
            if self.userDict[1].get("children") is not None:
                amountOfChildren = len(self.userDict[1]["children"])

            if amountOfChildren < 15:  # Max amount of children for parent is 15
                result = addChildToParent(self.inputForm[2].getText(), self.inputForm[4].getText(), self.userDict[0],
                                          "{} {} ({})".format(self.userDict[1]["name"], self.userDict[1]["last"],
                                                              self.userDict[0]))

                if result is True:
                    # Operation executed successfully
                    main.changeScene("mainMenu", self.userDict[0])
                else:
                    # Error
                    pass

        screenSize = display.get_size()
        self.userDict = userDict  # The scene will show the children of this specific parent

        # Background's Initialize
        self.background = pygame.transform.scale(pygame.image.load("images/Login Scene/purple_background.jpg"),
                                                 (screenSize[0], screenSize[1]))
        self.background.set_alpha(180)
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (200, 200, 200), "My Children",
                              36, "fonts/defaultFont.ttf")
        if userDict[1].get("children") is None:
            self.secondaryTitle = Text((50, HEADER_SIZE + 30), (0, 0, 0),
                                       "Amount of Children: 0", 20,
                                       "fonts/defaultFont.ttf", alignCenter=False)
        else:
            self.secondaryTitle = Text((50, HEADER_SIZE + 30), (0, 0, 0),
                                       "Amount of Children: {}".format(len(userDict[1]["children"])), 20,
                                       "fonts/defaultFont.ttf", alignCenter=False)
        self.currentPage = 0
        self.btnBack = Button((screenSize[0] - 200 - 20, screenSize[1] - 90, 200, 70), ((0, 46, 77), (0, 77, 128)),
                              "Back", "fonts/defaultFont.ttf", 28, goToScene, ("mainMenu", self.userDict[0]))

        # Get the children of the user and initialize the views objects
        self.views = []
        initializeChildList()

        # "Add a Child" components:
        self.inputForm = [
            # Form's Title Text:
            Text((screenSize[0] - 200 + 70, HEADER_SIZE + 80), (0, 0, 0), " Add a Child", 26,
                 "fonts/defaultFont.ttf", alignCenter=True),
            # Input for child's ID:
            Text((screenSize[0] - 200 + 70, HEADER_SIZE + 110), WHITE, "Child's ID:", 14,
                 "fonts/defaultFont.ttf", alignCenter=True),
            TextInput((screenSize[0] - 300 + 70, HEADER_SIZE + 120), 14, "fonts/defaultFont.ttf"),
            # Input for child's link password:
            Text((screenSize[0] - 200 + 70, HEADER_SIZE + 150), WHITE, "Link Password:", 14,
                 "fonts/defaultFont.ttf", alignCenter=True),
            TextInput((screenSize[0] - 300 + 70, HEADER_SIZE + 160), 14, "fonts/defaultFont.ttf")
        ]
        self.btnAdd = Button((screenSize[0] - 200 - 65 + 70, HEADER_SIZE + 210, 130, 30),
                             ((0, 46, 77), (0, 77, 128)), "Add", "fonts/defaultFont.ttf", 20, addChild)

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.userDict[0]
            if event.type == pygame.KEYDOWN:
                self.inputForm[2].updateText(event)
                self.inputForm[4].updateText(event)

        self.btnBack.update()
        self.btnAdd.update()
        self.inputForm[2].update()
        self.inputForm[4].update()

        for v in self.views:
            v.update()

        return True  # Continue with the game's loop

    def draw(self, display: pygame.Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill((200, 200, 200))
        display.blit(self.background, (0, 0))

        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))
        display.blit(self.systemLogo, (display.get_size()[0] - SYSTEMLOGO_SIZE - 10, 10))
        self.titleText.draw(display)

        # Draw Data
        self.secondaryTitle.draw(display)
        for v in self.views:
            v.draw(display)
        for iForm in self.inputForm:
            iForm.draw(display)

        # Draw Buttons
        self.btnBack.draw(display)
        self.btnAdd.draw(display)
