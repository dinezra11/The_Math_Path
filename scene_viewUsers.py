import pygame
from scene import Scene
from uiComponents import Text, TextInput, Button, ImageButton, ErrorText
from database import addMessage
from exportExcel import exportUsers

# Scene's Constants:
HEADER_SIZE = 80
SYSTEMLOGO_SIZE = 70
WHITE = (255, 255, 255)


class View:
    """ A class that represents a single view for a single user. """

    def __init__(self, position: tuple, size: tuple, data, goToScene, diagId):
        """ Initialize the View.

        :param position:        The (x, y) position of the view's box.
        :param size:            The size of the view's box.
        :param data:            The data from the database that needs to be shown. (dictionary)
        :param goToScene:       The function that change scenes.
        :param diagId:          The id of the diagnostic that engaged this screen.
        """

        def sendMessage():
            """ Send a private message to a specific user."""
            msg = self.text[4].getText()
            try:
                if msg == "":
                    raise Exception("Can't send an empty message.")
                addMessage("{} {}".format(diagId[1]["name"], diagId[1]["last"]), msg, data[0])
            except Exception as e:
                View.errorObj.pop(str(e), 1000)  # Pop error message
            else:
                self.text[4].clearText()

        View.errorObj = ErrorText((1024 / 2, 20), 24, "fonts/defaultFont.ttf")  # Error object
        self.position = position
        self.size = size
        self.data = data

        # Initialize view's text
        textSize = 18
        self.text = [
            Text(((position[0] + size[0]) / 2, position[1] + 15), (0, 0, 0),
                 "Full Name: {} {}".format(data[1]["name"], data[1]["last"]), 24, "fonts/defaultFont.ttf",
                 alignCenter=True),  # User's name
            Text((position[0] + 5, position[1] + 15 + 10), (0, 0, 0), "ID: {}".format(data[0]), textSize,
                 "fonts/defaultFont.ttf", alignCenter=False),  # User's ID
            Text((position[0] + 5, position[1] + 15 + 50), (0, 0, 0), "This user is a {}".format(data[1]["type"]),
                 textSize, "fonts/defaultFont.ttf", alignCenter=False),  # User's type
            Text((position[0] + 5, position[1] + size[1] - 55), (100, 100, 100), "Write a review/message to this user:",
                 textSize, "fonts/defaultFont.ttf", alignCenter=False),  # Private message title
            TextInput((position[0] + 30, position[1] + size[1] - 30), textSize,
                      "fonts/defaultFont.ttf", length=700, limit=70)  # Input for sending a message
        ]
        if self.data[1]["type"] == "Child":
            if self.data[1].get("parent") is None:
                self.text.append(
                    Text((position[0] + 5, position[1] + 15 + 30), (0, 0, 0), "Parent: Unknown", textSize,
                         "fonts/defaultFont.ttf", alignCenter=False))  # Child's parent is UNKNOWN
            else:
                self.text.append(
                    Text((position[0] + 5, position[1] + 15 + 30), (0, 0, 0), "Parent: {}".format(data[1]["parent"]),
                         textSize, "fonts/defaultFont.ttf", alignCenter=False))  # Child's parent is KNOWN

        # Initialize view's buttons
        btnSize = size[1] / 3
        self.btnScores = ImageButton(
            (position[0] + size[0] - btnSize - 5, position[1] + size[1] - btnSize - 5, btnSize, btnSize),
            "images/viewChildren Scene icons/scores icon.png", goToScene, ("viewScores", data[0], diagId[0], True))
        self.btnSend = ImageButton(
            (position[0] + size[0] - (btnSize - 5) * 3, position[1] + size[1] - btnSize + 10, btnSize, btnSize),
            "images/mefateah_feedback/send.png", sendMessage)
        btnSize -= 30
        self.btnDelete = ImageButton(
            (position[0] + size[0] - btnSize - 5, position[1] + 10, btnSize, btnSize),
            "images/Settings/deleteUserIcon.png", goToScene, ("deleteUser", data[0], diagId[0]))

        # Initialize view's background
        self.background = pygame.Surface((size[0], size[1]))
        self.background.set_alpha(55)
        self.background.fill((255, 255, 255))

    def update(self):
        """ Update view's buttons. """
        if self.data[1]["type"] == "Child":
            self.btnScores.update()

        self.text[4].update()
        self.btnSend.update()
        self.btnDelete.update()

        View.errorObj.update()

    def draw(self, display):
        """ Draw the View. """
        # Draw background (and borders) of View
        display.blit(self.background, self.position)
        pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1], self.size[0], self.size[1]), width=2)

        # Draw buttons Icons:
        if self.data[1]["type"] == "Child":
            self.btnScores.draw(display)
        self.btnSend.draw(display)
        self.btnDelete.draw(display)

        # Draw the data as a text on the view's box
        for txt in self.text:
            txt.draw(display)

        View.errorObj.draw(display)


class ViewUsers(Scene):
    def __init__(self, display, dictionaryOfUsers: tuple):
        """ Initialize the scene.

        :param display:                  The display where to draw the scene.
        :param dictionaryOfUsers:        A tuple, first element is the dictionary of the diagnostic, second
                                         element is a dictionary of all of the registered users.
        """
        import main  # Import main to get access to changeScene function (and avoid circular import)
        super().__init__(display)

        def goToScene(args: tuple):
            """ Change to another scene.

            :param args:            What scene needs to be displayed next.
            """
            if len(args) == 3:
                main.changeScene(args[0], (args[1], args[2]))
            elif len(args) == 4:
                main.changeScene(args[0], (args[1], args[2], args[3]))
            else:
                main.changeScene(args[0], args[1])

        def nextPage(action):
            """ Go to next or previous page, according to 'action' parameter. """
            self.views[self.currentPage].text[4].clearText()  # Clear the input for private message
            if action == "next":
                self.currentPage += 1
            else:
                self.currentPage -= 1

            # Keep currentPage in the correct limit
            if self.currentPage < 0:
                self.currentPage = 0
            elif self.currentPage >= len(self.views):
                self.currentPage = len(self.views) - 1

        def updateViewList(sFilter=None):
            # Initialize list of children
            if sFilter is None:
                searchFilter = self.input.getText()
            else:
                searchFilter = sFilter
            self.currentPage = 0
            self.views = []

            viewBoxSize = (screenSize[0] * 0.9, screenSize[1] / 4)
            for id, details in self.registeredUsers.items():
                if details["type"] == "Diagnostic":
                    continue  # Don't include diagnostics in the list

                if searchFilter in id or searchFilter in details["name"] or searchFilter in details["last"]:
                    self.views.append(
                        View((screenSize[0] / 2 - viewBoxSize[0] / 2, screenSize[1] / 2), viewBoxSize, (id, details),
                             goToScene, self.diagDict))

            self.countFound = Text((screenSize[0] / 2 - screenSize[0] * 0.9 / 2, screenSize[1] / 2 - 120),
                                   (0, 0, 0), "Users found: {}".format(len(self.views)), 20,
                                   "fonts/defaultFont.ttf", alignCenter=False)

        screenSize = display.get_size()
        self.diagDict = dictionaryOfUsers[0]
        self.registeredUsers = dictionaryOfUsers[1]

        # Background's Initialize
        self.background = pygame.transform.scale(pygame.image.load("images/Login Scene/red_background.jpg"),
                                                 (screenSize[0], screenSize[1]))
        self.background.set_alpha(180)
        self.systemLogo = pygame.transform.scale(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"),
                                                 (SYSTEMLOGO_SIZE, SYSTEMLOGO_SIZE))
        self.titleText = Text((display.get_size()[0] / 2, HEADER_SIZE / 2), (200, 200, 200), "Search User",
                              36, "fonts/defaultFont.ttf")
        self.help = pygame.image.load("images/viewChildren Scene icons/viewUsersHelp.png")

        self.btnBack = Button((screenSize[0] - 200 - 20, screenSize[1] - 90, 200, 70), ((0, 46, 77), (0, 77, 128)),
                              "Back", "fonts/defaultFont.ttf", 28, goToScene, ("mainMenu", self.diagDict[0]))

        # Initialize the views objects
        self.views = []
        self.currentPage = 0
        self.btnNextView = Button((screenSize[0] / 2 - 25 + 50, screenSize[1] / 2 + screenSize[1] / 4 + 10, 50, 50),
                                  ((0, 46, 77), (0, 77, 128)), "->",
                                  "fonts/defaultFont.ttf", 28, nextPage, "next")
        self.btnBackView = Button((screenSize[0] / 2 - 25 - 50, screenSize[1] / 2 + screenSize[1] / 4 + 10, 50, 50),
                                  ((0, 46, 77), (0, 77, 128)), "<-",
                                  "fonts/defaultFont.ttf", 28, nextPage, "previous")

        # Initialize filter input objects
        self.searchText = Text((screenSize[0] / 2 - screenSize[0] * 0.9 / 2, screenSize[1] / 2 - 80), (200, 200, 200),
                               "Filter:", 20, "fonts/defaultFont.ttf", alignCenter=False)
        self.input = TextInput((screenSize[0] / 2 - screenSize[0] * 0.9 / 2 + 60, screenSize[1] / 2 - 80), 20,
                               "fonts/defaultFont.ttf")
        self.btnFilter = Button((screenSize[0] / 2 - screenSize[0] * 0.9 / 2, screenSize[1] / 2 - 45, 100, 30),
                                ((0, 46, 77), (0, 77, 128)), "Search", "fonts/defaultFont.ttf", 20, updateViewList,
                                None)
        self.export = Button((screenSize[0] / 2 - screenSize[0] * 0.9 / 2 + 400, screenSize[1] / 2 - 45, 180, 28),
                             ((0, 46, 77), (0, 77, 128)), "Export To Excel", "fonts/defaultFont.ttf", 20,
                             exportUsers, None)

        updateViewList("")  # At the start of the scene, show all users without any filter

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.diagDict[0]
            if event.type == pygame.KEYDOWN:
                self.input.updateText(event)
                self.views[self.currentPage].text[4].updateText(event)

        self.btnBack.update()
        self.input.update()
        self.btnFilter.update()
        self.export.update()
        if self.currentPage + 1 < len(self.views):
            self.btnNextView.update()
        if self.currentPage != 0:
            self.btnBackView.update()

        if self.currentPage < len(self.views):
            self.views[self.currentPage].update()

        return True  # Continue with the game's loop

    def draw(self, display: pygame.Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill((0, 0, 100))
        display.blit(self.background, (0, 0))

        # Draw Header
        pygame.draw.rect(display, (0, 0, 0), (5, 5, display.get_size()[0] - 10, HEADER_SIZE), width=2)
        display.blit(self.systemLogo, (10, 10))
        display.blit(self.systemLogo, (display.get_size()[0] - SYSTEMLOGO_SIZE - 10, 10))
        self.titleText.draw(display)
        display.blit(self.help, (0, HEADER_SIZE - 15))

        # Draw Data
        if self.currentPage < len(self.views):
            self.views[self.currentPage].draw(display)
        self.countFound.draw(display)
        self.searchText.draw(display)
        self.input.draw(display)

        # Draw Buttons
        self.btnBack.draw(display)
        self.btnFilter.draw(display)
        self.export.draw(display)
        if self.currentPage + 1 < len(self.views):
            self.btnNextView.draw(display)
        if self.currentPage != 0:
            self.btnBackView.draw(display)
