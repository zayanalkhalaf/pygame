import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Apples")
clock = pygame.time.Clock()

# Basket settings
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
basket_x = (SCREEN_WIDTH - BASKET_WIDTH) // 2
basket_y = SCREEN_HEIGHT - 50
basket_speed = 10

# Apple settings
APPLE_RADIUS = 20
apple_speed = 5
apples = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to create apples
def create_apple():
    x = random.randint(APPLE_RADIUS, SCREEN_WIDTH - APPLE_RADIUS)
    y = -APPLE_RADIUS
    apples.append(pygame.Rect(x, y, APPLE_RADIUS * 2, APPLE_RADIUS * 2))

# Function to draw text
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game loop
def game_loop():
    global basket_x, score, apple_speed
    apples.clear()
    create_apple()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Basket controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH:
            basket_x += basket_speed

        # Update apple positions
        for apple in apples:
            apple.y += apple_speed
            if apple.y > SCREEN_HEIGHT:
                apples.remove(apple)
                create_apple()

        # Check for catching apples
        basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)
        for apple in apples:
            if basket_rect.colliderect(apple):
                apples.remove(apple)
                score += 1
                create_apple()
                if score % 10 == 0:  # Increase speed every 10 points
                    apple_speed += 1

        # Draw basket
        pygame.draw.rect(screen, BROWN, basket_rect)

        # Draw apples
        for apple in apples:
            pygame.draw.circle(screen, RED, apple.center, APPLE_RADIUS)

        # Display score
        draw_text(f"Score: {score}", BLACK, 10, 10)

        pygame.display.flip()
        clock.tick(30)

    # Game over screen
    screen.fill(WHITE)
    draw_text("Game Over!", RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Final Score: {score}", BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("Press any key to exit", BLACK, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Start the game
game_loop()
pygame.quit()
