import pygame.event
from pygame import Surface
from scene import Scene
from uiComponents import Button
import database


class DeleteUserApprove(Scene):
    def __init__(self, display: Surface, userID: tuple):
        """ Initialize the scene.

        :param display:             The screen's display, where to draw the components on.
        :param userID:              A tuple of user's ID -> (user to delete, the user that engaged that screen)
        """
        import main  # Import main to get access to changeScene function (and avoid circular import)

        def goToScene(args: tuple):
            """ Change to another scene.

            :param args:            What scene needs to be displayed next.
            """
            main.changeScene(args[0], args[1])

        def deleteUser():
            """ Use deleteUser() function from database.py to delete a user. """
            database.deleteUser(self.deleteID)
            goToScene(("mainMenu", self.currentUserID))

        super().__init__(display)
        screenSize = display.get_size()
        self.deleteID = userID[0]  # ID of the user to delete
        self.currentUserID = userID[1]  # ID of the user that engaged that screen (a parent or a diagnostic user)

        self.foreground = pygame.transform.scale(pygame.image.load("images/Settings/deleteUserForeground.png"),
                                                 screenSize)
        self.btnYes = Button((screenSize[0] / 2 - 100 - 200, screenSize[1] / 2 - 35, 200, 70),
                             ((0, 46, 77), (0, 77, 128)),
                             "Yes", "fonts/defaultFont.ttf", 28, deleteUser)
        self.btnNo = Button((screenSize[0] / 2 - 100 + 200, screenSize[1] / 2 - 35, 200, 70),
                            ((0, 46, 77), (0, 77, 128)),
                            "No", "fonts/defaultFont.ttf", 28, goToScene, ("mainMenu", self.currentUserID))

    def update(self):
        """ Update the scene.
        Also take care of events and user's input.
        Return False when need to quit the game, True otherwise. """
        # Keyboard Event check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.currentUserID

        self.btnYes.update()
        self.btnNo.update()

        return True

    def draw(self, display: Surface):
        """ Draw the scene. """
        display.blit(self.foreground, (0, 0))
        self.btnYes.draw(display)
        self.btnNo.draw(display)
