import pygame
from scene import Scene
from uiComponents import Button


def toggleSettings():
    Settings.showSettings = not Settings.showSettings


class Settings(Scene):
    showSettings = False  # Show the settings screen

    def __init__(self, display):
        def musicSwitch():
            if self.isMusicOn:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

            self.isMusicOn = not self.isMusicOn

        def blueFilterSwitch():
            self.blueFilterOn = not self.blueFilterOn

        screenSize = display.get_size()
        self.size = (700, 250)
        self.position = (screenSize[0] / 2 - self.size[0] / 2, screenSize[1] / 2 - self.size[1] / 2)
        self.background = pygame.transform.scale(pygame.image.load("images/Settings/background.png"),
                                                 self.size)

        # Blue Light Filter variables:
        self.blueLightSurface = pygame.Surface((screenSize[0], screenSize[1]))
        self.blueLightSurface.fill((100, 100, 0))
        self.blueLightSurface.set_alpha(100)

        # Settings variables:
        self.isMusicOn = True  # Is the music background on?
        self.blueFilterOn = False  # Does the user want to apply the blue-light-filter mode?

        # Buttons:
        self.btnFilter = Button(
            (self.position[0] + self.size[0] / 2 - 85 - 150, self.position[1] + self.size[1] / 2 - 25, 170, 30),
            ((0, 46, 77), (0, 77, 128)), "Blue-Light Filter", "fonts/defaultFont.ttf", 20, blueFilterSwitch)
        self.btnMusic = Button(
            (self.position[0] + self.size[0] / 2 - 85 + 150, self.position[1] + self.size[1] / 2 - 25, 170, 30),
            ((0, 46, 77), (0, 77, 128)), "Music On/Off", "fonts/defaultFont.ttf", 20, musicSwitch)
        self.btnBack = Button((self.position[0] + self.size[0] / 2 - 50, self.position[1] + self.size[1] - 70, 100, 30),
                              ((0, 46, 77), (0, 77, 128)), "Back", "fonts/defaultFont.ttf", 20, toggleSettings)

        # Music Initialization:
        pygame.mixer.music.load("audio/music/backgroundMusic.mp3")
        pygame.mixer.music.play(-1)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                toggleSettings()

        self.btnFilter.update()
        self.btnMusic.update()
        self.btnBack.update()

    def draw(self, display: pygame.Surface):
        display.blit(self.background, self.position)
        self.btnFilter.draw(display)
        self.btnMusic.draw(display)
        self.btnBack.draw(display)
