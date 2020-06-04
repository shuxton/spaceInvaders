import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score_value = font.render("Score :"+str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


enemyImg = pygame.image.load('enemy.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
   # enemyImg.append()
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX-bulletX)**2)+((enemyY-bulletY)**2))
    if distance < 27:
        return True
    else:
        return False


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


over = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over_text = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bulletX = playerX
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":

        bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    for i in range(num_of_enemies):
        if enemyY[i] >= 470:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = (-1)*enemyX_change[i]
        elif enemyX[i] > 736:
            enemyX[i] = 736
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = (-1)*enemyX_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision and bullet_state is "fire":
            boom = mixer.Sound('explosion.wav')
            boom.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        elif collision and bullet_state is "ready":
            game_over()
        enemy(enemyX[i], enemyY[i])
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
