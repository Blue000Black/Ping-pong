from pygame import *
from random import randint


class table():
    def __init__(self):
        global sprites
        sprites['table'] = self

    def draw(self):
        draw.rect(mw, (0, 50, 0), (250, 200, 700, 500), 1)


def draw_display():
    for i in sprites.keys():
        sprite[i].draw()


if __name__ == '__main__':
    fps = 30
    scoreL = 0
    scoreR = 0
    mw = display.set_mode((1200, 900))
    display.set_caption('Ping-pong')
    clock = time.Clock()
    running = True
    sprites = dict()
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        mw.fill((245, 155, 66))
        draw_display()
        clock.tick(fps)
exit()
