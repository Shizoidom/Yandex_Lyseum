import os
from random import randint
from sys import exit

import pygame

pygame.init()

state = 'start'

front1 = pygame.font.Font(None, 35)  # добавление шрифта (маленького)
front2 = pygame.font.Font(None, 80)  # добавление шрифта (большого)
WIDTH, HEIDHT = 800, 600
FPS = 60
frame = 0  # переменная для плавной анимации
timer = 10  # переменная для включения гемплея или отключения игры
pipe_speed = 3  # скорость труб
pipe_gate_size = 200  # ширина проххххххода труб
live = 3  # кол-во жизней
scores = 0  # количество очков

py, sy, ay = HEIDHT // 2, 0, 0  # py sy ay всё это координаты птички на оси y разделены для удобства
player = pygame.Rect(WIDTH // 3, py, 34, 24)  # хитбокс птички (просто квадрат который мы не будем рисовать)
pipe_gate_pos = HEIDHT // 2  # позиция труб

window = pygame.display.set_mode((WIDTH, HEIDHT))
clock = pygame.time.Clock()
# загрузка изображений
img_fon = pygame.image.load('img/fon.png')
img_bird = pygame.image.load('img/bird.png')
img_pipe_top = pygame.image.load('img/pipe_niz.png')
img_pipe_bottom = pygame.image.load('img/pipe_verh.png')

pygame.mixer.music.load('audio/music.mp3')  # загрузка музыки
pygame.mixer.music.set_volume(0.1)  # уменьшение её громкости
pygame.mixer.music.play(-1)  # включение музыки на повторение

die_sound = pygame.mixer.Sound('audio/die.ogg')  # загрузка звука смерти

pygame.display.set_caption('Flappy bird')
pygame.display.set_icon(pygame.image.load('img/icon.png'))  # иконка приложения
pipes_scores = []  # трубы за которые уже дали очки
pipes = []  # все трубы(хитбокс)
# фон
fon = []

fon.append(pygame.Rect(0, 0, 280, 600))  # первый фон

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    ex = keys[pygame.K_ESCAPE]
    if ex:
        play = False
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1
    frame = (frame + 0.2) % 3  # смена анимации
    pipe_speed = 3 + scores // 100  # скорость движения труб

    for i in range(len(fon) - 1, -1, -1):
        fone = fon[i]
        fone.x -= pipe_speed // 2  # фон движется в два раза медленее труб

        if fone.right < 0:  # если фон вышел за границу то удаляем его
            fon.remove(fone)

        if fon[len(fon) - 1].right <= WIDTH:  # если фон не закрывает всю облость экрана то добовляем ещё один
            fon.append(pygame.Rect(fon[len(fon) - 1].right, 0, 280, 600))

    for i in range(len(pipes) - 1, -1, -1):  # список по удалению труб поторые ушли налево
        pipe = pipes[i]  # отдельно взятая труба
        pipe.x -= pipe_speed  # движение труб
        if pipe.right < 0:  # если труба ушла левее граници экрана
            pipes.remove(pipe)
            if pipe in pipes_scores:  # очищаем список с трубами за которые дали очки
                pipes_scores.remove(pipe)

    if state == 'start':

        if click and timer == 0 and len(pipes) == 0:  # игра начнётся только после того как игрок нажмёт пробел
            # или правую кнопку мыши так же если прошла минимум 1 секунда и если на экране исчезли все трубы
            state = 'play'

        py += (HEIDHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play':
        if click:  # птичка всё время падает если начать играть
            ay = -2

        else:
            ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.95
        player.y = py
        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 55, pipe_gate_pos - pipe_gate_size // 2))  # верхняя труба
            pipes.append(pygame.Rect(WIDTH, pipe_gate_pos + pipe_gate_size // 2, 55, HEIDHT -  # нижняя труба
                                     pipe_gate_pos + pipe_gate_size // 2))
            pipe_gate_pos += randint(-100, 100)  # трубы будут менять место проход

            if pipe_gate_pos < pipe_gate_size:  # что бы проход не ушёл слишком вверх
                pipe_gate_pos = pipe_gate_size

            elif pipe_gate_pos > HEIDHT - pipe_gate_size:  # что бы проход не ушёл слишком вниз
                pipe_gate_pos = HEIDHT - pipe_gate_size

        if player.top < 0 or player.bottom > HEIDHT:  # если игрок коснётся потолка или пола то он потеряет жизнь
            state = 'fall'

        for pipe in pipes:

            if player.colliderect(pipe):  # проверка пересечения птици с трубой
                state = 'fall'

            if pipe.right < player.left and pipe not in pipes_scores:  # когда координаты птички
                # больше координаты трубы и за трубу ещё не давали очки добовляем очки
                pipes_scores.append(pipe)
                scores += 5  # изза двух труб добовляется по 10 очков

    elif state == 'fall':
        die_sound.play()  # включение звука смерти
        sy, ay = 0, 0
        pipe_gate_pos = HEIDHT // 2  # нужно что бы в начале игры трубы были на уровне игрока
        live -= 1

        if live > 0:  # если жизней больше 0 то игра продолжается
            state = 'start'
            timer = 60

        else:
            state = 'game over'
            timer = 180  # время через которое выключится игра

    else:  # когда игра заканчивается птичка падает пролетает дно и уходит из зоны видимости
        py += sy
        sy = (sy + ay + 1) * 0.95
        player.y = py

        if timer == 0:
            play = False

    window.fill(pygame.Color('black'))

    for fn in fon:  # отрисовка фона
        window.blit(img_fon, fn)

    for pipe in pipes:

        if pipe.y == 0:  # проверка на то нижняя труба или верхняя
            rect = img_pipe_top.get_rect(bottomleft=pipe.bottomleft)  # картинка трубы налаживается на хитбокс трубы
            window.blit(img_pipe_top, rect)  # отрисовка трубы

        else:
            rect = img_pipe_bottom.get_rect(topleft=pipe.topleft)
            window.blit(img_pipe_bottom, rect)

    image = img_bird.subsurface(34 * int(frame), 0, 34, 24)  # анимация
    image = pygame.transform.rotate(image, -sy * 2)  # наклонение птички вверх или вниз

    text = front1.render('Очки: ' + str(scores), 0, pygame.Color('black'))
    window.blit(text, (10, 10))

    text = front1.render('Жизни: ' + str(live), 0, pygame.Color('black'))
    window.blit(text, (10, HEIDHT - 30))

    window.blit(image, player)  # рисуем птичку в координатах хитбокса

    pygame.display.update()

    clock.tick(FPS)

pygame.display.quit()
pygame.quit()
os.system('C:/Users/Admin/PycharmProjects/pythonProject/main.py')
exit()
