import os
from random import randrange as rand
from sys import exit
import pygame
from pygame import *

init()

mixer.music.load('audio2/tetris.mp3')  # загрузка музыки
mixer.music.set_volume(0.1)  # уменьшение её громкости
mixer.music.play(-1)  # включение музыки на повторение


def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def check_col(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board


def matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1


def newbord():
    board = [
        [0 for x in range(cols)]
        for y in range(rows)
    ]
    board += [[1 for x in range(cols)]]
    return board


class Tetris(object):
    def __init__(self):
        key.set_repeat(250, 25)
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.bground_grid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]

        self.default_font = font.Font(
            font.get_default_font(), 12)

        self.screen = display.set_mode((self.width, self.height))
        event.set_blocked(MOUSEMOTION)

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    def init_game(self):
        self.board = newbord()
        self.new_stone()
        self.level, self.score, self.lines = 1, 0, 0
        time.set_timer(USEREVENT + 1, 1000)

    def disp_msg(self, msg, tpleft):
        x, y = tpleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(line, False, (255, 255, 255), (0, 0, 0)), (x, y))
            y += 14

    def drwmatrx(self, matrix, ofst):
        of_x, of_y = ofst
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    draw.rect(self.screen, color[val],
                                     Rect((of_x + x) * cell_size,
                                                 (of_y + y) * cell_size,
                                                 cell_size,
                                                 cell_size), 0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level * 6:
            self.level += 1
            newdelay = 1000 - 50 * (self.level - 1)
            newdelay = 100 if newdelay < 100 else newdelay
            time.set_timer(USEREVENT + 1, newdelay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_col(self.board,
                             self.stone,
                             (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self):
        if not self.gameover and not self.paused:
            self.score += 1  # добавление очков от падения
            self.stone_y += 1
            if check_col(self.board,
                         self.stone,
                         (self.stone_x, self.stone_y)):
                self.board = matrixes(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove(
                                self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def new_stone(self):
        self.stone = self.next_stone[:]

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]

        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if check_col(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate(self.stone)
            if not check_col(self.board,
                             new_stone,
                             (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x = msgim_center_x // 2
            msgim_center_y = msgim_center_y // 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))

    def run(self):
        key_actions = {
            'a': lambda: self.move(-1),
            'd': lambda: self.move(+1),
            's': lambda: self.drop(),
            'w': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game,
        }

        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = time.Clock()
        run = True
        while run:
            self.screen.fill((0, 0, 0))
            if self.gameover:
                self.center_msg("""Game Over!\nYour score: %d
                Press space to continue""" % self.score)
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    draw.line(self.screen,
                                     (255, 255, 255),
                                     (self.rlim + 1, 0),
                                     (self.rlim + 1, self.height - 1))
                    self.disp_msg("Next:", (
                        self.rlim + cell_size,
                        2))
                    self.disp_msg("Score: %d\n\nLevel: %d\
                    \nLines: %d" % (self.score, self.level, self.lines),
                                  (self.rlim + cell_size, cell_size * 5))
                    self.drwmatrx(self.bground_grid, (0, 0))
                    self.drwmatrx(self.board, (0, 0))
                    self.drwmatrx(self.stone,
                                     (self.stone_x, self.stone_y))
                    self.drwmatrx(self.next_stone,
                                     (cols + 1, 2))
            display.update()

            for event in pygame.event.get():
                if event.type == USEREVENT + 1:
                    self.drop()
                elif event.type == QUIT:
                    run = False
                keys = pygame.key.get_pressed()
                ex = keys[K_ESCAPE]
                if ex:
                    run = False
                elif event.type == KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                                             + key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(maxfps)


# размер клетки поля
cell_size = 18
# размер поля
cols = 10
rows = 22

maxfps = 30
# цвета
color = [(0, 0, 0),
         (255, 85, 85),
         (100, 200, 115),
         (255, 140, 50),
         (120, 108, 245),
         (50, 120, 52),
         (146, 202, 73),
         (150, 161, 218),
         (35, 35, 35)]

tetris_shapes = [[
    # угловая палка как буква T
    [1, 1, 1],
    [0, 1, 0]],
    # угловая палка как отзеркаленыя буква Z
    [[0, 2, 2],
     [2, 2, 0]],
    # угловая палка как буква Z
    [[3, 3, 0],
     [0, 3, 3]],
    # угловая палка как отзеркаленыя буква L
    [[4, 0, 0],
     [4, 4, 4]],
    # угловая палка как буква L
    [[0, 0, 5],
     [5, 5, 5]],
    # прямая палка как буква I
    [[6, 6, 6, 6]],
    # квадрат
    [[7, 7],
     [7, 7]]
]

if __name__ == '__main__':
    App = Tetris()
    App.run()
display.quit()
quit()
os.system('C:/Users/Admin/PycharmProjects/pythonProject/main.py')
exit()
