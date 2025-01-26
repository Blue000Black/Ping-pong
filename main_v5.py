from pygame import *
from math import sin, cos, radians
from time import time as t


class Lose():
    def __init__(self, x, y):
        sprites['lose'] = self
        self.x = x
        self.y = y
        self.r = 0
        self.d = 50

    def update(self):
        pass

    def draw(self):
        global status
        sprites['lose'].x = ball.x
        sprites['lose'].y = ball.y
        for i in range(6):
            draw.circle(mw, (255, 0, 0), (self.x, self.y), self.r - i * self.d, 3)
        if status == 'lose':
            self.r += 300 / fps
        if self.r > 1700:
            for i in sprites.keys():
                sprites[i].reset()
            status = 'onserve'

    def reset(self):
        self.x = 0
        self.y = 0
        self.r = 0


class Table():
    def __init__(self):
        sprites['table'] = self
        self.rect = (350, 200, 700, 500)
        self.rect1 = Rect(350, 200, 350, 500)
        self.rect2 = Rect(700, 200, 350, 500)
        self.touched1 = False
        self.touched2 = False

    def draw(self):
        draw.rect(mw, (0, 50, 0), self.rect, 0)
        draw.line(mw, (255, 255, 255), (360, 450), (1040, 450), 3)
        draw.line(mw, (0, 0, 0), (700, 195), (700, 705), 2)

    def update(self):
        global status
        global l_scores
        global score1
        global score2
        if self.rect1.collidepoint(sprites['ball'].x, ball.y) and 750 < sprites['ball'].h < 850:
            sprites['ball'].sh *= -0.93
            if not self.touched1:
                self.touched1 = True
            else:
                if ball.sender == 'player1':
                    score2 += 1
                else:
                    score1 += 1
                l_scores = font.render(str(score1) + ':' + str(score2), True, scores_c)
                status = 'lose'
        if self.rect2.collidepoint(sprites['ball'].x, ball.y) and 750 < sprites['ball'].h < 850:
            sprites['ball'].sh *= -0.93
            if not self.touched2:
                self.touched2 = True
            else:
                if ball.sender == 'player1':
                    score2 += 1
                else:
                    score1 += 1
                l_scores = font.render(str(score1) + ':' + str(score2), True, scores_c)
                status = 'lose'
        if 690 <= ball.x <= 710 and 195 < ball.y < 705 and 750 < ball.h < 950:
            sprites['lose'].x = ball.x
            sprites['lose'].y = ball.y
            status = 'lose'

    def reset(self):
        self.touched1 = False
        self.touched2 = False


class Player():
    def __init__(self, n, x, y, angle, length, l, r, u, d, rl, rr):
        sprites['player'+n] = self
        self.n = n
        self.serve = False
        self.jumps = 1
        self.length = length
        self.angle = angle
        self.sx = 350
        self.sy = 400
        self.x = x
        self.y = y
        self.strike_complexity = 0
        self.cnt = 0
        self.l = l
        self.r = r
        self.u = u
        self.d = d
        self.rl = rl
        self.rr = rr

    def reset(self):
        if self.n == '1':
            self.x = 100
            self.y = 450
            self.angle = 0
        else:
            self.x = 1300
            self.y = 450
            self.angle = 180

    def draw(self):
        draw.circle(mw, (0, 0, 255), (self.x, self.y), 20, 0)
        draw.line(mw, (0, 0, 255), (int(self.x), int(self.y)),
            (int(self.x + self.length * cos(radians(self.angle))), int(self.y + self.length * sin(radians(self.angle)))), 5)

    def update(self):
        self.angle %= 360
        keys_pressed = key.get_pressed()
        if keys_pressed[self.u] and self.y >= 20:
            self.y -= self.sy / fps
        if keys_pressed[self.d] and 880 >= self.y:
            self.y += self.sy / fps
        if keys_pressed[self.l] and self.x >= 20 and self.n =='1':
            self.x -= self.sx / fps
        if keys_pressed[self.r] and self.x <= 680 and self.n == '1':
            self.x += self.sx / fps
        if keys_pressed[self.l] and self.x >= 720 and self.n == '2':
            self.x -= self.sx / fps
        if keys_pressed[self.r] and self.x <= 1380 and self.n == '2':
            self.x += self.sx / fps
        if keys_pressed[self.rl]:
            self.angle -= 100 / fps
        if keys_pressed[self.rr]:
            self.angle += 100 / fps

    def collideball(self):
        pass


class Ball():
    def __init__(self):
        sprites['ball'] = self
        self.x = 200
        self.y = 450
        self.h = 2000
        self.sh = 0
        self.speed = 400
        self.angle = 0
        self.sender = 'player1'
        self.rect = Rect(self.x - 5, self.y - 5, 10, 10)

    def reset(self):
        global server
        self.x = 700
        self.y = 450
        self.h = 2000
        self.sh = 0
        self.speed = 400
        self.angle = 0
        self.sender = server

    def draw(self):
        draw.circle(mw, (255, 255, 255), (int(self.x), int(self.y)), self.h / 160, 0)
        draw.circle(mw, (50, 255, 50), (int(self.x), int(self.y)), 5, 2)

    def update(self):
        global status
        global score1
        global score2
        global l_scores
        self.x += self.speed / fps * cos(radians(self.angle))
        self.y += self.speed / fps * sin(radians(self.angle))
        self.sh -= 9800 / fps
        self.h += self.sh / fps
        self.angle %= 360
        if self.h <= 0:
            if status == 'default':
                if self.sender == 'player1':
                    if table.touched2:
                        score1 += 1
                    else:
                        score2 += 1
                else:
                    if table.touched1:
                        score2 += 1
                    else:
                        score1 += 1
            else:
                if self.sender == 'player1':
                    if table.touched1 and table.touched2:
                        score1 += 1
                    else:
                        score2 += 1
                else:
                    if table.touched1 and table.touched2:
                        score2 += 1
                    else:
                        score1 += 1
            l_scores = font.render(str(score1) + ':' + str(score2), True, scores_c)
            status = 'lose'
            sprites['lose'].x = self.x
            sprites['lose'].y = self.y


def update():
    for i in sprites.keys():
        sprites[i].update()


def draw_display():
    global sprites
    for i in sprites.keys():
        sprites[i].draw()
    mw.blit(l_scores, (670, 5))
    if status == 'finish':
        mw.blit(l_winner, (500, 290))
        mw.blit(l_restart, (450, 390))
    display.update()

def changep():
    global server
    if sprites['ball'].sender == 'player1':
        server = 'player2'
        sprites['ball'].sender = 'player2'
        sprites['ball'].x = sprites['player2'].x + (player2.length + 30) * cos(radians(player2.angle))
        sprites['ball'].y = sprites['player2'].y + (player2.length + 30) * sin(radians(player2.angle))
        sprites['ball'].angle = sprites['player2'].angle
    else:
        server = 'player1'
        sprites['ball'].sender = 'player1'
        sprites['ball'].x = sprites['player1'].x + (player1.length + 30) * cos(radians(player1.angle))
        sprites['ball'].y = sprites['player1'].y + (player1.length + 30) * sin(radians(player1.angle))
        sprites['ball'].angle = sprites['player1'].angle

if __name__ == '__main__':
    fps = 90
    status = 'toserve'
    score1 = 0
    score2 = 0
    serves = 2
    last = 0
    maxscore = 11
    server = 'player1'
    mixer.init()
    mw = display.set_mode((1400, 900))
    display.set_caption('Ping-pong')
    clock = time.Clock()
    running = True
    sprites = dict()
    table = Table()
    ball = Ball()
    lose = Lose(0, 0)
    player1 = Player('1', 100, 450, 0, 70, K_a, K_d, K_w, K_s, K_LSHIFT, K_LCTRL)
    player2 = Player('2', 1300, 450, 180, 70, K_l, K_QUOTE, K_p, K_SEMICOLON, K_RSHIFT, K_RCTRL)
    scores_c = (255, 255, 255)
    font.init()
    font = font.SysFont('Arial', 55)
    l_scores = font.render(str(score1) + ':' + str(score2), True, scores_c)
    l_restart = font.render('Press "space" to restart', True, (255, 255, 255))
    l_winner = font.render('Left player won!', True, (255, 0, 255))
    tl = 0
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        keys_pressed = key.get_pressed()
        if status == 'toserve':
            if keys_pressed[K_SPACE] and t() - tl > 0.3:
                changep()
                tl = t()
            if keys_pressed[K_RETURN]:
                status = 'onserve'
        if status == 'onserve' or status == 'serve' or status == 'default':
            update()
        if status == 'onserve':
            if score1 + score2 - last >= 2:
                ball.sender = server
                changep()
                server = ball.sender
                last = score1 + score2
            if sprites['ball'].sender == 'player1':
                sprites['ball'].x = sprites['player1'].x + (player1.length + 30) * cos(radians(player1.angle))
                sprites['ball'].y = sprites['player1'].y + (player1.length + 30) * sin(radians(player1.angle))
                sprites['ball'].angle = sprites['player1'].angle
            else:
                sprites['ball'].x = sprites['player2'].x + (player2.length + 30) * cos(radians(player2.angle))
                sprites['ball'].y = sprites['player2'].y + (player2.length + 30) * sin(radians(player2.angle))
                sprites['ball'].angle = sprites['player2'].angle
            ball.sh = 0
            ball.h = 2000
            if keys_pressed[K_SPACE]:
                status = 'serve'
        if score1 >= maxscore and status != 'finish':
            l_winner = font.render('Left player won!', True, (255, 0, 255))
            status = 'finish'
        if score2 >= maxscore and status != 'finish':
            l_winner = font.render('Right player won!', True, (255, 0, 255))
            status = 'finish'
        if status == 'finish' and keys_pressed[K_SPACE]:
            for i in sprites.keys():
                sprites[i].reset()
            score1 = 0
            score2 = 0
            cnt = 0
            last = 0
            status = 'toserve'
        mw.fill((245, 155, 66))
        draw_display()
        clock.tick(fps)
exit()
