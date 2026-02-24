import pygame
import random

pygame.init()

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)

# ================= WINDOW =================
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# ================= FUNCTIONS =================
def text_screen(text, color, x, y, font_use):
    screen_text = font_use.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))


def draw_grid():
    for x in range(0, SCREEN_WIDTH, 30):
        pygame.draw.line(gameWindow, GRAY, (x, 50), (x, SCREEN_HEIGHT))
    for y in range(50, SCREEN_HEIGHT, 30):
        pygame.draw.line(gameWindow, GRAY, (0, y), (SCREEN_WIDTH, y))


def plot_snake(snk_list, snake_size):
    for i, (x, y) in enumerate(snk_list):
        if i == len(snk_list) - 1:
            pygame.draw.rect(gameWindow, DARK_GREEN, [x, y, snake_size, snake_size])
        else:
            pygame.draw.rect(gameWindow, GREEN, [x, y, snake_size, snake_size])


# ================= WELCOME SCREEN =================
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((30, 30, 30))
        text_screen("SNAKE GAME", GREEN, 300, 200, big_font)
        text_screen("Press SPACE to Play", WHITE, 280, 300, font)
        text_screen("Use Arrow Keys", WHITE, 310, 350, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# ================= GAME LOOP =================
def gameloop():
    exit_game = False
    game_over = False

    snake_x = 60
    snake_y = 90
    velocity_x = 0
    velocity_y = 0

    snake_size = 30
    init_velocity = 5

    fps = 15              # 🔥 SLOW INITIAL SPEED
    max_fps = 40          # 🔥 SPEED LIMIT

    snk_list = []
    snk_length = 1

    food_x = random.randrange(0, SCREEN_WIDTH - snake_size, 30)
    food_y = random.randrange(60, SCREEN_HEIGHT - snake_size, 30)

    score = 0

    while not exit_game:
        if game_over:
            gameWindow.fill(WHITE)
            text_screen("GAME OVER", RED, 320, 200, big_font)
            text_screen(f"Score : {score * 10}", BLACK, 360, 280, font)
            text_screen("Press ENTER to Restart", BLACK, 250, 340, font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # ===== EAT FOOD =====
            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 1
                food_x = random.randrange(0, SCREEN_WIDTH - snake_size, 30)
                food_y = random.randrange(60, SCREEN_HEIGHT - snake_size, 30)
                snk_length += 5

                # 🔥 INCREASE SPEED GRADUALLY
                if fps < max_fps:
                    fps += 1

            # ===== DRAWING =====
            gameWindow.fill((245, 245, 245))

            # Top bar
            pygame.draw.rect(gameWindow, DARK_GRAY, [0, 0, SCREEN_WIDTH, 50])
            text_screen(f"Score : {score * 10}", WHITE, 10, 10, font)
            text_screen(f"Speed : {fps}", WHITE, 200, 10, font)

            draw_grid()

            # Food
            pygame.draw.circle(
                gameWindow,
                RED,
                (food_x + snake_size // 2, food_y + snake_size // 2),
                snake_size // 2
            )

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Collision with self
            if head in snk_list[:-1]:
                game_over = True

            # Wall collision
            if snake_x < 0 or snake_x > SCREEN_WIDTH - snake_size or snake_y < 50 or snake_y > SCREEN_HEIGHT - snake_size:
                game_over = True

            plot_snake(snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


# ================= START GAME =================
welcome()
