import os
import random
from sys import exit

import pygame

size = 30
half_size = size // 2

res = 750

FPS = 30
fps_snace = 4
counter = 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode((res, res))

start_pos = res // 2 - half_size
lenght = 4

x, y = 0, size
direct = {'w': (0, -size), 's': (0, size), 'a': (-size, 0), 'd': (size, 0)}

score = 0

snake = [(start_pos, start_pos)]
apple = (random.randrange(0, res - size, size), random.randrange(0, res - size, size))
run = True


def apple_gen():
    global apple, score, lenght
    apple = (random.randrange(0, res - size, size), random.randrange(0, res - size, size))
    for snake_num in range(len(snake)):
        if apple[0] == snake[snake_num][0] and apple[1] == snake[snake_num][1]:
            apple_gen()
        else:
            apple = (random.randrange(0, res - size, size), random.randrange(0, res - size, size))
            break
    score += 1
    lenght += 1


while run:
    pygame.display.set_caption("Змеёка. Счёт: " + str(score))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0, 0, 0))

    [pygame.draw.rect(screen, (0, 160, 0), (x, y, size, size)) for x, y in snake]
    pygame.draw.circle(screen, (160, 0, 0), (apple[0] + half_size, apple[1] + half_size), half_size)

    key = pygame.key.get_pressed()
    if counter % fps_snace == 0:
        newx = snake[-1][0] + x
        newy = snake[-1][1] + y
        snake.append((newx, newy))

        snake = snake[-lenght - 1:]

    if apple[0] == snake[-1][0] and apple[1] == snake[-1][1]:
        apple_gen()
    if key[pygame.K_w]:
        if (x, y) != direct['s']:
            x, y = direct['w']
    if key[pygame.K_s]:
        if (x, y) != direct['w']:
            x, y = direct['s']
    if key[pygame.K_a]:
        if (x, y) != direct['d']:
            x, y = direct['a']
    if key[pygame.K_d]:
        if (x, y) != direct['a']:
            x, y = direct['d']

    if snake[-1][0] <= -size or snake[-1][0] >= res or snake[-1][1] <= -size or snake[-1][1] >= res:
        run = False

    counter += 1
    clock.tick(FPS)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
os.system('C:/Users/Admin/PycharmProjects/pythonProject/main.py')
exit()
