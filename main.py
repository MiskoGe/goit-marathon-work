import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from os import listdir

pygame.init()
FPS = pygame.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BLUE = 0, 0, 255
IMGS_PATH = 'goose'

font = pygame.font.SysFont('verdana', 20)

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = player_imgs[0]
ball_rect = ball.get_rect()
ball_speed = 5

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, height - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_width()), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(2, 4)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENM = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENM, 1500)
CREATE_BNS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BNS, 3000)
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

score = 0
img_index = 0

enemies = []
bonuses = []

is_working = True
while is_working:
    FPS.tick(100)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENM:
            enemies.append(create_enemy())
        if event.type == CREATE_BNS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs): img_index = 0
            ball = player_imgs[img_index]

    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX2 < 0:
        bgX = 0
        bgX2 = width

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(score), True, BLUE), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move((-enemy[2], 0))
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move((0, bonus[2]))
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].top > height:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1


    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_DOWN] and ball_rect.bottom < height:
        ball_rect = ball_rect.move((0, ball_speed))
    if pressed_keys[K_UP] and ball_rect.top > 0:
        ball_rect = ball_rect.move((0, -ball_speed))
    if pressed_keys[K_LEFT] and ball_rect.left > 0:
        ball_rect = ball_rect.move((-ball_speed, 0))
    if pressed_keys[K_RIGHT] and ball_rect.right < width:
        ball_rect = ball_rect.move((ball_speed, 0))

    pygame.display.flip()
