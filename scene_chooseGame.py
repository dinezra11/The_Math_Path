import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Text, Button

# Scene's Constants:
BACKGROUND_COLOR = (102, 51, 0)
HEADER_COLOR = (246, 195, 36)
FOOTER_COLOR = (96, 96, 96)
WHITE = (255, 255, 255)
HEADER_SIZE = 45


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
            main.changeScene(args[0], args[1])

        screenSize = display.get_size()
        self.userId = userId

        self.titleText = Text((display.get_size()[0] / 2, 20), WHITE, "Choose a Game", 24, "fonts/defaultFont.ttf")
        self.btnBack = self.btnLogin = Button((screenSize[0] - 250, screenSize[1] / 2, 200, 70),
                                                    ((0, 46, 77), (0, 77, 128)), "Back", "fonts/defaultFont.ttf",
                                                    28, goToScene, ("mainMenu", self.userId))

        self.btnGame = [
            Button((100, HEADER_SIZE + 20, 300, 70),
                   ((0, 46, 77), (0, 77, 128)), "Count Game", "fonts/defaultFont.ttf",
                   28, goToScene, ("game_countGame", None)),
            Button((100, HEADER_SIZE + 120, 300, 70),
                   ((0, 46, 77), (0, 77, 128)), "Choose Size", "fonts/defaultFont.ttf",
                   28, goToScene, ("game_chooseSize", None)),
            Button((100, HEADER_SIZE + 220, 300, 70),
                   ((0, 46, 77), (0, 77, 128)), "Math Expressions", "fonts/defaultFont.ttf",
                   28, goToScene, ("game_mathExp", None))
        ]

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.btnBack.update()
        for btn in self.btnGame:
            btn.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        display.fill(BACKGROUND_COLOR)
        display.fill(HEADER_COLOR, (0, 0, display.get_size()[0], HEADER_SIZE))
        display.fill(FOOTER_COLOR, (0, display.get_size()[1] - HEADER_SIZE, display.get_size()[0], HEADER_SIZE))
        self.titleText.draw(display)
        self.btnBack.draw(display)

        for btn in self.btnGame:
            btn.draw(display)
