""" Main file of the system! """
import pygame
import traceback  # for showing the traceback on the console while error handling
from scene_login import LoginScene
from scene_mainMenu import MainMenu
from scene_chooseGame import ChooseGame
from scene_chooseSize import ChooseSize
from scene_count_game import count_game
from scene_mygame import MyGame
from scene_mygame_plus import MyGame_plus
from scene_mygame_minus import MyGame_minus
from scene_catchGame import CatchGame
from scene_viewScores import ViewScores
from scene_viewMessages import ViewMessages
from scene_viewChildren import ViewChildren
from scene_viewUsers import ViewUsers
from scene_diag_feedback import diag_feedback
from scene_about_us import Aboutus
from scene_add_tips import add_tips
from scene_private_notes import private_notes

# Global constants and variables
WIN_WIDTH = 1024
WIN_HEIGHT = 800
WIN_TITLE = "The Math Path"

# Initialize PyGame and the display:
pygame.init()
gameDisplay = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(WIN_TITLE)
pygame.display.set_icon(pygame.image.load("images/Login Scene/Welcome Screen/System Logo.png"))
gameClock = pygame.time.Clock()

# Scenes variables
SCENES = {
    # Menus Scenes:
    'start': LoginScene,
    'mainMenu': MainMenu,
    'chooseGame': ChooseGame,

    # Mini-Games Scenes:
    'game_countGame': count_game,
    'game_chooseSize': ChooseSize,
    'game_mathExp_power': MyGame,  # Arithmetic Game Type: *
    'game_mathExp_plus': MyGame_plus,  # Arithmetic Game Type: +
    'game_mathExp_minus': MyGame_minus,  # Arithmetic Game Type: -
    'game_catchGame': CatchGame,

    # Statistics and Data Scenes:
    'viewScores': ViewScores,
    'viewMessages': ViewMessages,
    'viewChildren': ViewChildren,
    'viewUsers': ViewUsers,

    # Other Scenes:
    'diag_feedback': diag_feedback,
    'about': Aboutus,
    'add_tips': add_tips,
    'private_notes': private_notes
}
currentScene = None  # This variable will hold the object of the current scene!


def changeScene(newScene="", args=None):
    """ Change the current screen to the desired one.
    End the game if newScene='endGame'.
    Do nothing if the desired scene doesn't exist in SCENES's dictionary.
    """
    global currentScene
    fadeSurface = pygame.Surface(gameDisplay.get_size())
    fadeSurface.fill((0, 0, 0))

    def fadeOut():
        for i in range(0, 255, 10):
            currentScene.draw(gameDisplay)
            fadeSurface.set_alpha(i)
            gameDisplay.blit(fadeSurface, (0, 0))
            pygame.display.update()
            gameClock.tick(60)

    def fadeIn():
        for i in range(255, 0, -10):
            currentScene.draw(gameDisplay)
            fadeSurface.set_alpha(i)
            gameDisplay.blit(fadeSurface, (0, 0))
            pygame.display.update()
            gameClock.tick(60)

    if newScene == "endGame":
        # Safely close pygame and quit the game:
        fadeOut()
        pygame.quit()
        quit()
    elif newScene in SCENES:
        # Fade out and in to the new scene:
        fadeOut()
        del currentScene
        if args is None:
            currentScene = SCENES[newScene](gameDisplay)
        else:
            currentScene = SCENES[newScene](gameDisplay, args)
        fadeIn()


def update():
    """ Update the screen according to the current scene. End the game when need to quit the game completely. """
    result = currentScene.update()
    if result is False:
        if type(currentScene) is LoginScene:  # If game was attempted to be closed from first scene - Quit the system.
            changeScene("endGame")
            return False
        else:  # If game was attempted to be closed from any other scene - Return to title screen.
            changeScene("start")  # End the game's loop
    elif result is not True:  # Scene returned userId instead of boolean value. Return to main menu AFTER logging in
        changeScene("mainMenu", result)
        return True

    return True  # Continue with the game's loop


def draw():
    """ Draw the current scene. """
    currentScene.draw(gameDisplay)
    pygame.display.update()


# GAME STARTS HERE #
try:
    currentScene = SCENES['start'](gameDisplay)  # Initialize the first default scene

    # Game's Loop:
    while update():
        draw()
        gameClock.tick(30)  # FPS
except Exception as e:  # Handle default exceptions (The exceptions that haven't been caught by the scene's class)
    print("Error occurred.")  # need to make new error scene (detailed one)
    traceback.print_exc()  # for debugging
finally:
    # Quit the game. Close PyGame safely:
    pygame.quit()
    quit()
