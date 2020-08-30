import pygame
import random
import os

# initialize pygame
pygame.init()
pygame.mixer.init()

screen_width = 700
screen_height = 400

# background image
pygame.display.set_mode()
bgimg = pygame.image.load("back.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (16, 165, 195)
deep_blue = (9, 126, 149)
off_white = (230, 237, 239)

fps = 40

# Creating Window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Check existence of file
if(not os.path.exists("highscore.txt")):
    with open("highscore.txt", "w") as f:
        f.write("0")
        f.close()

with open("highscore.txt", "r") as f:
    highscore = f.read()

def display_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(deep_blue)
        display_text("Welcome To Snake World", black, 130, 150)
        display_text("Press Space Bar To Play", black, 140, 210)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(fps)


# Creating a game loop
def game_loop():
    pygame.mixer.music.load('back.mp3')
    pygame.mixer.music.play()
    # Game Specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    init_valocity = 5
    valocity_x = 0
    valocity_y = 0
    snake_size = 10
    food_x = random.randint(20, screen_width)
    food_y = random.randint(20, screen_height)
    score = 0
    snake_list = []
    snake_length = 1

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(highscore)
                f.close()

            gameWindow.fill(off_white)
            display_text("Score: " + str(score) + " !!!", red, 50, 100)
            display_text("Press Enter to Continue...", red, 50, 150)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        valocity_x = init_valocity
                        valocity_y = 0

                    if event.key == pygame.K_LEFT:
                        valocity_x = -init_valocity
                        valocity_y = 0

                    if event.key == pygame.K_UP:
                        valocity_y = -init_valocity
                        valocity_x = 0

                    if event.key == pygame.K_DOWN:
                        valocity_y = init_valocity
                        valocity_x = 0

                    # Adding cheat code
                    # if event.key == pygame.K_q:
                    #     score += 10

            snake_x = snake_x + valocity_x
            snake_y = snake_y + valocity_y

            if abs(snake_x-food_x) < 10 and abs(snake_y-food_y) < 10:
                pygame.mixer.music.load('feed.mp3')
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length += 5
                if score > int(highscore):
                    # pygame.mixer.music.load('highscore.mp3')
                    # pygame.mixer.music.play()
                    highscore = str(score)

            gameWindow.fill(blue)
            gameWindow.blit(bgimg, (0, 0))
            display_text("Score: " + str(score) + "  Highscore: " + highscore, off_white, 5, 5)
            pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or \
                snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snake_list, snake_size)

            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

        pygame.display.update()
        # every second at most 30 frames should pass
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()

