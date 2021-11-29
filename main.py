""" Main file of the system! """
import pygame
from scene_login import LoginScene
from scene_mainMenu import MainMenu
from scene_chooseGame import ChooseGame
from scene_chooseSize import ChooseSize
from scene_count_game import count_game
from scene_mygame import MyGame

# Global constants and variables
WIN_WIDTH = 1024
WIN_HEIGHT = 800
WIN_TITLE = "The Math Path"

# Initialize PyGame and the display:
pygame.init()
gameDisplay = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(WIN_TITLE)
gameClock = pygame.time.Clock()

# Scenes variables
SCENES = {
    'start': LoginScene,
    'mainMenu': MainMenu,
    'chooseGame': ChooseGame,
    'game_countGame': count_game,
    'game_chooseSize': ChooseSize,
    'game_mathExp': MyGame
}
currentScene = SCENES['start'](gameDisplay)


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
    if currentScene.update():
        return True # Continue with the game's loop
    else:
        changeScene("endGame") # End the game's loop
        return False


def draw():
    """ Draw the current scene. """
    currentScene.draw(gameDisplay)
    pygame.display.update()


# Game Loop:
while update():
    draw()
    gameClock.tick(30) # FPS

# Quit the game. Close PyGame safely:
pygame.quit()
quit()
