# import pygame
import pygame
# import random, math, and mixer from pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

def player(x, y):
    # Display the player on the screen
    screen.blit(player_img, (x, y))

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

def enemy(x, y, i):
    # Display an enemy on the screen
    screen.blit(enemy_img[i], (x, y))

def show_score(x, y):
    # Display the score on the screen
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = 'ready'

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    # Check if a collision has occurred between an enemy and a bullet
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

def fire_bullet(x, y):
    global bullet_state
    # Fire a bullet on the screen
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))

def set_background():
    # Set the background of the screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

def move_bullet():
    global bullet_x, bullet_y, bullet_state
    # Move the bullet on the screen
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

def game_input():
    global running, player_x_change, bullet_x, player_x, bullet_y
    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

def enemy_movement():
    global enemy_x, enemy_x_change, enemy_y, enemy_y_change
    # Move the enemies on the screen
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]
        enemy(enemy_x[i], enemy_y[i], i)

def collision():
    global num_of_enemies, enemy_x, enemy_y, bullet_x, bullet_y, bullet_state, score_value
    # Handle collisions between enemies and bullets
    for i in range(num_of_enemies):
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

# Timer
start_time = pygame.time.get_ticks()
game_duration = 1 * 60 * 1000  # 5 minutes in milliseconds
font_timer = pygame.font.Font('freesansbold.ttf', 32)

# Game Loop
running = True
while running:
    set_background()
    game_input()
    enemy_movement()
    collision()
    move_bullet()
    player(player_x, player_y)
    show_score(text_x, text_y)

    # Display Timer
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, game_duration - elapsed_time)
    timer_text = font_timer.render('Time: {:.2f}'.format(remaining_time / 1000), True, (255, 255, 255))
    screen.blit(timer_text, (600, 10))

    pygame.display.update()

    # Check if the timer is out
    if elapsed_time >= game_duration:
        running = False

# Game Over Message
game_over_text = font.render('Game Over', True, (255, 255, 255))
score_text = font.render('Final Score: ' + str(score_value), True, (255, 255, 255))
screen.blit(game_over_text, (250, 250))
screen.blit(score_text, (300, 300))
pygame.display.update()

# Wait for a moment before closing the game
pygame.time.delay(4000)

pygame.quit()
