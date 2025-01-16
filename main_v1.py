from pygame import *
from random import randint


class Table():
    def __init__(self):
        global sprites
        sprites['table'] = self
        self.rect = (350, 200, 700, 500)

    def draw(self):
        draw.rect(mw, (0, 50, 0), self.rect, 0)
        draw.line(mw, (255, 255, 255), (360, 450), (1040, 450), 3)
        draw.line(mw, (0, 0, 0), (700, 195), (700, 705), 2)


class Ball():
    def __init__(self):
        global sprites
        sprites['ball'] = self
        self.x = 700
        self.y = 450
        self.h = 1000
        self.plus = 0
        self.xs = 50
        self.ys = 50
        self.sender = True
        self.touched = False

    def draw(self):
        draw.circle(mw, (255, 255, 255), (self.x, self.y), int(self.h / 50))
        draw.circle(mw, (50, 255, 50), (self.x, self.y), 10, 2)



def draw_display():
    global sprites
    mw.blit(l_scores, (670, 5))
    for i in sprites.keys():
        sprites[i].draw()
    display.update()


if __name__ == '__main__':
    fps = 60
    scoreL = 0
    scoreR = 0
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
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        mw.fill((245, 155, 66))
        draw_display()
        clock.tick(fps)
exit()
