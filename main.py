import os
from sys import exit

import pygame

game = ''
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
font_ = pygame.font.SysFont('', 50)
run = True


class Menu:
    def __init__(self):
        self.option_sur = []
        self.collbacks_ = []
        self.current_operation_index = 0

    def append_operation(self, option, callback):
        self.option_sur.append(font_.render(option, True, (255, 255, 255)))
        self.collbacks_.append(callback)

    def switch(self, direction):
        self.current_operation_index = max(0, min(self.current_operation_index + direction, len(self.option_sur) - 1))

    def select(self):
        self.collbacks_[self.current_operation_index]()

    def draw(self, surf, x, y, option_y_pad):
        for i, option in enumerate(self.option_sur):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_pad)
            if i == self.current_operation_index:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)


menu = Menu()
menu.append_operation('Flappy bird', lambda: flappy_bird())
menu.append_operation('Tetris', lambda: tetris())
menu.append_operation('Змейка', lambda: zmeica())
menu.append_operation('Quit', pygame.quit)


def flappy_bird():
    global game, run
    game = 'Flappy bird'
    run = False


def tetris():
    global game, run
    game = 'Tetris'
    run = False


def zmeica():
    global game, run
    game = 'Змейка'
    run = False


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                menu.switch(-1)
            elif event.key == pygame.K_s:
                menu.switch(1)
            elif event.key == pygame.K_SPACE:
                menu.select()

        screen.fill((0, 0, 0))

        menu.draw(screen, 100, 100, 75)

        pygame.display.flip()
pygame.display.quit()
pygame.quit()
if game == 'Flappy bird':
    os.system('C:/Users/Admin/PycharmProjects/pythonProject/main2.py')
elif game == 'Tetris':
    os.system('C:/Users/Admin/PycharmProjects/pythonProject/main1.py')
elif game == 'Змейка':
    os.system('C:/Users/Admin/PycharmProjects/pythonProject/main3.py')
exit()
