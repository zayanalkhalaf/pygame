import pygame
import time
import random


pygame.init()

yellow = (255, 255, 0)
display_width = 800
display_height = 600
gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("sword throw")
clock = pygame.time.Clock()
sword_width = 100  
sword_height = 150  # Add sword height

def draw_obstacle(obs_startx, obs_starty, obs_width, obs_height):
    rock_color = (128, 128, 128)  # Grey color
    points = [
        (obs_startx, obs_starty),
        (obs_startx + obs_width * 0.4, obs_starty - obs_height * 0.2),
        (obs_startx + obs_width * 0.8, obs_starty),
        (obs_startx + obs_width, obs_starty + obs_height * 0.4),
        (obs_startx + obs_width * 0.6, obs_starty + obs_height),
        (obs_startx + obs_width * 0.2, obs_starty + obs_height * 0.8)
    ]
    pygame.draw.polygon(gamedisplays, rock_color, points)

def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()

def message_display(text, score):
    largetext = pygame.font.Font("freesansbold.ttf", 80)
    smalltext = pygame.font.Font("freesansbold.ttf", 36)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((display_width / 2), (display_height / 2))
    gamedisplays.blit(textsurf, textrect)
    
    scoresurf, scorerect = text_objects(f"Score: {score}", smalltext)
    scorerect.center = ((display_width / 2), (display_height / 2) + 50)
    gamedisplays.blit(scoresurf, scorerect)
    
    pygame.display.update()
    time.sleep(3)
    game_loop()

def crash(message, score):
    message_display(message, score)

backgroundpic = pygame.image.load('background.jfif')
backgroundpic = pygame.transform.scale(backgroundpic, (display_width, display_height))

swordimg = pygame.image.load('sword.png')
swordimg = pygame.transform.scale(swordimg, (sword_width, sword_height))  # Use sword height

def background():
    gamedisplays.blit(backgroundpic, (0, 0))

def sword(x, y):
    gamedisplays.blit(swordimg, (x, y))

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    bumped = False
    x_change = 0
    obstacle_speed = 9
    obs_startx = random.randrange(200, (display_width - 200))
    obs_starty = -750
    obs_width = random.randint(50, 140)  # Random width between 50 and 140
    obs_height = random.randint(50, 140)  # Random height between 50 and 140
    score = 0

    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10  # Increase the speed here
                if event.key == pygame.K_RIGHT:
                    x_change = 10  # Increase the speed here
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        # Prevent the sword from going out of bounds
        if x > display_width - sword_width:
            x = display_width - sword_width
            crash("OUT", score)
        if x < 0:
            x = 0
            crash("OUT", score)

        gamedisplays.fill(yellow)
        background()  # Call the background function to display the background
        draw_obstacle(obs_startx, obs_starty, obs_width, obs_height)
        obs_starty += obstacle_speed
        sword(x, y)

        if obs_starty > display_height:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(170, (display_width - 170))
            obs_width = random.randint(50, 140)  # Random width between 50 and 140
            obs_height = random.randint(50, 140)  # Random height between 50 and 140
            score += 1  # Increment the score when an obstacle passes the bottom

            # Increase obstacle speed by 1% after every score
            obstacle_speed *= 1.01

        # Check for collision with the obstacle
        if y < obs_starty + obs_height and y + sword_height > obs_starty:
            if x > obs_startx and x < obs_startx + obs_width or x + sword_width > obs_startx and x + sword_width < obs_startx + obs_width:
                crash("CRUSHHHEDD :<<", score)

        # Display the score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (0, 0, 0))
        gamedisplays.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
