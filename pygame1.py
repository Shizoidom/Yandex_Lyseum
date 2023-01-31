import os
import random

import pygame

pygame.init()


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(dod_image, (45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        global jamp
        # сброс переменных
        scroll = 0
        dx = 0
        dy = 0
        # управление
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False
        # гравитация
        self.vel_y += gravity
        dy += self.vel_y
        # игрок должен быть в экране
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        # столкновение с платформами по оси y
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # проверка находится ли игрок над платформой
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        # игрок прыгает
                        self.vel_y = -20
                        # звук прыжка
                        jamp.play()
        # проверка прыгнул ли игрок
        if self.rect.top <= minimum_threshold:
            # если он прыгает то переменнная движения игрока меняется
            if self.vel_y < 0:
                scroll = -dy
        # обновление хитбокса
        self.rect.x += dx
        self.rect.y += dy + scroll
        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        # платформа двигается на экране
        self.rect.y += scroll
        # когда позиция платформы меньше ниже 600 удаляем её
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

clock = pygame.time.Clock()
FPS = 45

minimum_threshold = 200
gravity = 0.98
maximum_platforms = 12
y_axis_movement = 0
fon_ = 0
game_over = False
score = 0
game_over_move = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

dod_image = pygame.image.load('data/img/dod.png').convert_alpha()
fon_image = pygame.image.load('data/img/fon.jpg').convert_alpha()
platform_image = pygame.image.load('data/img/plot.png').convert_alpha()

jamp = pygame.mixer.Sound('data/audio/jamp.wav')

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

platform_group = pygame.sprite.Group()
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)
run = True
while run:
    clock.tick(FPS)
    if not game_over:
        y_axis_movement = player.move()
        # фон
        fon_ += y_axis_movement
        if fon_ >= 600:
            fon_ = 0
        # отрисовка фона
        screen.blit(fon_image, (0, 0 + fon_))
        screen.blit(fon_image, (0, -600 + fon_))
        # генерация платформ
        if len(platform_group) < maximum_platforms:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)
        # движение платформ вниз относительно игрока
        platform_group.update(y_axis_movement)
        # обновление очков
        if y_axis_movement > 0:
            score += y_axis_movement
            score = int(score // 1)
        # отметка максимального результата
        pygame.draw.line(screen, BLACK, (0, score - high_score + minimum_threshold),
                         (SCREEN_WIDTH, score - high_score + minimum_threshold), 3)
        # надпись с 'HIGH SCORE'
        img = font_small.render('HIGH SCORE', True, BLACK)
        screen.blit(img, (SCREEN_WIDTH - 130, score - high_score + minimum_threshold))
        # отрисовка игрока и платформ
        platform_group.draw(screen)
        player.draw()
        # очки
        img = font_small.render('SCORE: ' + str(score), True, BLACK)
        screen.blit(img, (0, 0))
        # проверка на поражение
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        score = int(score // 1)
        if game_over_move < SCREEN_HEIGHT:
            game_over_move += 5
            for y in range(6):
                pygame.draw.rect(screen, BLACK, (0, 0, 400, game_over_move))
        else:
            img = font_big.render('GAME OVER!', True, WHITE)
            screen.blit(img, (130, 200))
            img = font_big.render('SCORE: ' + str(score), True, WHITE)
            screen.blit(img, (130, 250))
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # сбрасываем переменные
                game_over = False
                score = 0
                scroll = 0
                game_over_move = 0
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                platform_group.empty()
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False
    pygame.display.update()
pygame.quit()
