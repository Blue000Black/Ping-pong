from pygame import *
from time import time as t
from math import sin, cos
from random import randint


class Table():
    def __init__(self):
        sprites['table'] = self
        self.rect = (350, 200, 700, 500)
        self.rect1 = Rect(350, 200, 350, 500)
        self.rect2 = Rect(700, 200, 350, 500)

    def draw(self):
        draw.rect(mw, (0, 50, 0), self.rect, 0)
        draw.line(mw, (255, 255, 255), (360, 450), (1040, 450), 3)
        draw.line(mw, (0, 0, 0), (700, 195), (700, 705), 2)

    def update(self):
        if self.rect1.colliderect(sprites['ball']) and 750 < sprites['ball'].h < 850:
            sprites['ball'].sh *= -0.93


class Player():
    def __init__(self, n, x, y, angle, length):
        sprites['player'+n] = self
        self.serve = False
        self.jumps = 1
        self.length = length
        self.angle = angle
        self.sx = 100
        self.sy = 70
        self.x = x
        self.y = y
        self.score = 0

    def draw(self):
        draw.line(mw, (0, 0, 255), (int(self.x), int(self.y)),
            (int(self.x + self.length * cos(self.angle)), int(self.y + self.length * sin(self.angle))), 5)

    def update(self):
        self.angle %= 360

    def collideball(self):
        #if () ** 2 + () ** 2 <= 25
        pass


class Ball():
    def __init__(self):
        sprites['ball'] = self
        self.x = 700
        self.y = 450
        self.h = 2000
        self.sh = 0
        self.sx = 50
        self.sy = 50
        self.rect = Rect(self.x - 5, self.y - 5, 10, 10)
        self.sender = True
        self.touched = False

    def draw(self):
        draw.circle(mw, (255, 255, 255), (int(self.x), int(self.y)), self.h / 160, 0)
        draw.circle(mw, (50, 255, 50), (int(self.x), int(self.y)), 5, 2)

    def update(self):
        self.x += self.sx / fps
        self.y += self.sy / fps
        self.sh -= 9800 / fps
        self.h += self.sh / fps
        if self.h <= 0:
            finish = True


def update():
    for i in sprites.keys():
        sprites[i].update()


def draw_display():
    global sprites
    mw.blit(l_scores, (670, 5))
    for i in sprites.keys():
        sprites[i].draw()
    if finish and cnt < 5:
        for i in range(5):
            if t() >= times[i]:
                draw.circle(mw, (255, 0, 0), (sprites['ball'].x, sprites['ball'].y), circles[i], 2)
                circles[i] += 2
    display.update()


if __name__ == '__main__':
    fps = 90
    scoreL = 0
    scoreR = 0
    mixer.init()
    mw = display.set_mode((1400, 900))
    display.set_caption('Ping-pong')
    clock = time.Clock()
    running = True
    sprites = dict()
    table = Table()
    ball = Ball()
    scores_c = (255, 255, 255)
    font.init()
    font = font.SysFont('Arial', 55)
    l_scores = font.render(str(scoreL) + ':' + str(scoreR), True, scores_c)
    l_resume = font.render('Press "R" to resume', True, (255, 255, 255))
    l_restart = font.render('Press "P" to restart', True, (255, 255, 255))
    l_winL = font.render('Blue player has won!', True, (0, 0, 255))
    l_winR = font.render('Red player has won!', True, (255, 0, 0))
    l_draw = font.render('You have a draw!', True, (255, 255, 255))
    finish = False
    restart = False
    cnt = 0
    circles = [0, 0, 0, 0, 0]
    times = [t(), t() + 0.5, t() + 1, t() + 1.5, t() + 2]
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        mw.fill((245, 155, 66))
        draw_display()
        if not finish:
            update()
        clock.tick(fps)
exit()
