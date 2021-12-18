import pygame
from random import randint
from scene import Scene
from uiComponents import Button, Text
import database

# Constants:
HEARTICON_SIZE = 30  # Size of the heart's image
HUD_POS = (5, 5)  # Starting position of UI (score and remaining lives)
NEWANSWER_EVENT = pygame.USEREVENT  # Holder for the event of dropping a new answer
NEWANSWER_COOLDOWN = 1500  # The time in ms for new answer to be dropped


class Player:
    def __init__(self, yPos, width, height, screenBorders: tuple):
        """ Player class.

        :param yPost:           Starting y position.
        :param width:           Width of the player's rectangle.
        :param height:          Height of the player's rectangle.
        :param screenBorders:   A tuple that represents the border of the screen. (To limit player's movement)
        """
        self.position = [0, yPos]
        self.size = (width, height)
        self.screenBorders = screenBorders

    def update(self):
        # Set the center of the player to match the X coordinate of the user's mouse
        mousePos = pygame.mouse.get_pos()
        self.position[0] = mousePos[0] - self.size[0] / 2

        # Apply screen's borders
        if self.position[0] < self.screenBorders[0]:
            self.position[0] = self.screenBorders[0]
        if self.position[0] + self.size[0] > self.screenBorders[1]:
            self.position[0] = self.screenBorders[1] - self.size[0]

    def draw(self, display):
        pygame.draw.rect(display, (102, 51, 153), (self.position[0], self.position[1], self.size[0], self.size[1]))


class Answer:
    def __init__(self, correctAnswer, currentScore):
        """ Answer class. The collision between the answer object and the player object will be detected during game.

        :param correctAnswer:           The correct answer of the current question.
        """
        # Set difficulty level:
        level = currentScore // 5 + 1

        if randint(1, 2) == 2:  # There is 0.5 probability for correct answer
            self.text = correctAnswer
        else:  # There is 0.5 probability for wrong answer. Randomly generate the answer object
            if level < 4:
                self.text = randint(0, 15)
            else:
                self.text = randint(0, 100)

        self.renderText = Answer.loadFont.render(str(self.text), True, (0, 0, 0))
        self.position = [randint(0, Answer.screenSize[0] - 50), 0]

        if level == 1:
            self.speed = 5
        elif level == 2:
            self.speed = randint(5, 8)
        else:
            self.speed = randint(5, 10)

    def update(self):
        # Update position
        self.position[1] += self.speed

    def draw(self, display):
        display.blit(self.renderText, self.position)


def generateQuestion(currentScore):
    """ Generate a new question!
    Randomly generate an arithmetic expression problem.
    Return a tuple which consists of a string and integer. (The question and the valid answer)
    """

    expression = ""  # The generated arithmetic expression
    answer = None  # The correct answer

    level = currentScore // 5 + 1  # Set the difficulty level

    # Generate operands
    if level < 4:
        operands = (randint(0, 10), randint(0, 10))  # Only numbers 0-10 at levels 1-3
    elif 4 < level < 6:
        operands = (randint(0, 20), randint(0, 10))  # Only numbers 0-20 at levels 4-6
    else:
        operands = (randint(0, 100), randint(0, 10))  # For the rest of the levels: first operand 0-100, second 0-10

    # Generate operator
    if level == 1:
        operator = 0  # Only '+' operator at level 1
    elif level == 2:
        operator = randint(0, 1)  # Only '+' and '-' operators at level 2
    else:
        operator = randint(0, 2)  # For the rest of the levels - operators '+' '-' '*' are valid

    if operator == 0:
        expression = "{} + {} = ?".format(operands[0], operands[1])
        answer = operands[0] + operands[1]
    if operator == 1:
        expression = "{} - {} = ?".format(operands[0], operands[1])
        answer = operands[0] - operands[1]
    if operator == 2:
        expression = "{} * {} = ?".format(operands[0], operands[1])
        answer = operands[0] * operands[1]

    return expression, answer


class CatchGame(Scene):
    def __init__(self, display, userId):
        """ Initialize the scene.

        :param:     display -> The display where to draw the scene.
        """

        def changeGameState(newState):
            self.state = newState

        screenSize = display.get_size()
        self.userId = userId
        Answer.screenSize = screenSize
        Answer.loadFont = pygame.font.Font("fonts/defaultFont.ttf", 30)
        self.state = "intro"  # Possible game's stats: intro, play, end, exit

        # Intro initialize
        self.introBackground = pygame.transform.scale(pygame.image.load("images/Catch the Answer/introBackground.jpg"),
                                                      (screenSize[0], screenSize[1]))
        self.btnPlay = Button((650, 570, 200, 70),
                              ((0, 46, 77), (0, 77, 128)), "Start", "fonts/defaultFont.ttf",
                              28, changeGameState, "play")

        # Play initialize
        self.playBackground = pygame.transform.scale(pygame.image.load("images/Catch the Answer/gameBackground.jpg"),
                                                     (screenSize[0], screenSize[1]))
        self.score = 0
        self.player = Player(screenSize[1] - 50, 140, 10, (0, screenSize[0]))
        self.scoreText = Text((HUD_POS[0], HUD_POS[1]), (255, 255, 255), "Score: 0", 36, "fonts/defaultFont.ttf",
                              alignCenter=False)

        self.question = generateQuestion(self.score)
        self.questionText = Text((screenSize[0] / 2, 50), (100, 100, 100), self.question[0], 40,
                                 "fonts/defaultFont.ttf")
        self.answer = [Answer(self.question[1], self.score)]
        pygame.time.set_timer(NEWANSWER_EVENT, NEWANSWER_COOLDOWN)  # Set the timer for the new answer event

        self.lives = 3
        self.heartIcon = pygame.transform.scale(pygame.image.load("images/Catch the Answer/heart.png"),
                                                (HEARTICON_SIZE, HEARTICON_SIZE))

        # End initialize
        self.endBackground = pygame.transform.scale(pygame.image.load("images/Catch the Answer/endBackground.jpg"),
                                                    (screenSize[0], screenSize[1]))
        self.endButton = Button((650, 570, 200, 70), ((0, 46, 77), (0, 77, 128)), "Back to Menu",
                                "fonts/defaultFont.ttf", 28, changeGameState, "exit")

    def update(self):
        """ Update the scene. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == NEWANSWER_EVENT:  # The event for new answer to be shown
                self.answer.append(Answer(self.question[1], self.score))

        if self.state == "intro":
            self.btnPlay.update()
        elif self.state == "play":
            if self.lives == 0:
                self.state = "end"

            self.player.update()

            for i in range(len(self.answer)):
                self.answer[i].update()
                # Check collisions:
                ansSize = self.answer[i].renderText.get_height()
                if self.answer[i].position[1] + ansSize >= self.player.position[1]:
                    if self.player.position[0] <= self.answer[i].position[0] <= self.player.position[0] + \
                            self.player.size[0]:
                        # Collide with player!
                        if self.question[1] == self.answer[i].text:
                            # Caught correct answer!
                            self.score += 1
                            self.scoreText.changeText(str("Score: {}".format(self.score)))
                            self.question = generateQuestion(self.score)
                            self.questionText.changeText(self.question[0])
                        else:
                            # Caught wrong answer!
                            self.lives -= 1

                        del self.answer[i]
                        break
                    elif self.answer[i].position[1] >= Answer.screenSize[1]:
                        # Answer left the screen!
                        if self.question[1] == self.answer[i].text:
                            # Missed correct answer!
                            self.lives -= 1

                        del self.answer[i]
                        break
        elif self.state == "end":
            self.endButton.update()
        elif self.state == "exit":
            database.addScore("Catch the Answer", self.score, self.userId)
            return self.userId  # Return userId so the system will go back to the user's menu screen

        return True

    def draw(self, display: pygame.Surface):
        """ Draw the scene.

        :param:     display -> The display where to draw the scene.
        """
        if self.state == "intro":
            display.blit(self.introBackground, (0, 0))
            self.btnPlay.draw(display)
        elif self.state == "play":
            display.blit(self.playBackground, (0, 0))
            self.player.draw(display)
            for ans in self.answer:
                ans.draw(display)
            self.scoreText.draw(display)
            self.questionText.draw(display)

            heartX = HUD_POS[0]
            for i in range(self.lives):
                display.blit(self.heartIcon, (heartX, HUD_POS[1] + 50))
                heartX += HEARTICON_SIZE + 5
        elif self.state == "end":
            display.blit(self.endBackground, (0, 0))
            self.scoreText.draw(display)
            self.endButton.draw(display)
