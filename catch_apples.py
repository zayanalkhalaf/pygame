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

# Define fruit colors
FRUIT_COLORS = [RED, GREEN, (255, 165, 0), (255, 255, 0)]  # Red (apple), Green (lime), Orange, Yellow (banana)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Fruits")
clock = pygame.time.Clock()

# Basket settings
BASKET_WIDTH = 100
BASKET_HEIGHT = 40
basket_x = (SCREEN_WIDTH - BASKET_WIDTH) // 2
basket_y = SCREEN_HEIGHT - 100
basket_speed = 15

# Apple settings
APPLE_RADIUS = 20
apple_speed = 10
apples = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to create apples (now fruits)
def create_fruit():
    x = random.randint(APPLE_RADIUS, SCREEN_WIDTH - APPLE_RADIUS)
    y = -APPLE_RADIUS
    color = random.choice(FRUIT_COLORS)  # Randomly select a fruit color
    fruit = {"rect": pygame.Rect(x, y, APPLE_RADIUS * 2, APPLE_RADIUS * 2), "color": color}
    apples.append(fruit)

# Function to draw text
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Draw basket
def draw_basket(x, y, width, height):
    # Draw the basket base (rectangle)
    pygame.draw.rect(screen, BROWN, (x, y, width, height))
    
    # Draw the basket handle (arc)
    pygame.draw.arc(
        screen, BROWN, 
        (x - 10, y - height, width + 20, height * 2), 
        3.14, 0, 5  # Arc from left to right
    )

# Game loop
def game_loop():
    global basket_x, score, apple_speed
    apples.clear()
    create_fruit()
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

        # Update fruit positions
        for fruit in apples:
            fruit["rect"].y += apple_speed
            if fruit["rect"].y > SCREEN_HEIGHT:
                apples.remove(fruit)
                create_fruit()

        # Check for catching fruits
        basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)
        for fruit in apples:
            if basket_rect.colliderect(fruit["rect"]):
                apples.remove(fruit)
                score += 1
                apple_speed += 0.2  # Increase speed slightly with every caught fruit
                create_fruit()

        # Draw basket
        draw_basket(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)

        # Draw fruits
        for fruit in apples:
            pygame.draw.circle(screen, fruit["color"], fruit["rect"].center, APPLE_RADIUS)

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
