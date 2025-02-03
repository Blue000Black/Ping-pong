from pygame import *
from math import sin, cos, radians, sqrt, acos
from time import time as t
import os

class Lose():
    def __init__(self, x, y):
        sprites['lose'] = self
        self.x = x
        self.y = y
        self.r = 0
        self.d = 50
        self.sound = mixer.Sound('lose.mp3')

    def update(self):
        pass

    def draw(self):
        global status
        sprites['lose'].x = ball.x
        sprites['lose'].y = ball.y
        for i in range(6):
            draw.circle(mw, (255, 0, 0),
                        (self.x, self.y), self.r - i * self.d, 3)
        if status == 'lose':
            self.sound.play()
            self.r += 300 / fps
        if self.r > 425:
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
        self.rect = Rect(350, 200, 700, 500)
        self.rect1 = Rect(350, 200, 350, 500)
        self.rect2 = Rect(700, 200, 350, 500)
        self.touched1 = False
        self.touched2 = False
        self.sound = mixer.Sound('table_sound.mp3')

    def draw(self):
        draw.rect(mw, (0, 50, 0), self.rect, 0)
        draw.line(mw, (255, 255, 255), (360, 450),
                  (1040, 450), 3)
        draw.line(mw, (0, 0, 0), (700, 195),
                  (700, 705), 2)

    def update(self):
        global status
        global l_scores
        global score1
        global score2
        if (self.rect1.collidepoint(sprites['ball'].x, ball.y)
                and 750 < sprites['ball'].h < 850):
            sprites['ball'].sh *= -0.93
            sprites[sprites['ball'].sender].score += int(sqrt((sprites[sprites['ball'].sender].x - 525) ** 2 +
                (sprites[sprites['ball'].sender].y - 450) ** 2))
            self.sound.play()
            if not self.touched1:
                self.touched1 = True
            else:
                if ball.sender == 'player1':
                    score2 += 1
                else:
                    score1 += 1
                l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
                status = 'lose'
        if self.rect2.collidepoint(sprites['ball'].x, ball.y) and 750 < sprites['ball'].h < 850:
            sprites['ball'].sh *= -0.93
            sprites[sprites['ball'].sender].score += int(sqrt((sprites[sprites['ball'].sender].x - 875) ** 2 +
                (sprites[sprites['ball'].sender].y - 450) ** 2))
            self.sound.play()
            if not self.touched2:
                self.touched2 = True
            else:
                if ball.sender == 'player1':
                    score2 += 1
                else:
                    score1 += 1
                l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
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
        self.length = length
        self.angle = angle
        self.sx = 350
        self.sy = 400
        self.x = x
        self.y = y
        self.score = 0
        self.l = l
        self.r = r
        self.u = u
        self.d = d
        self.rl = rl
        self.rr = rr
        self.sound = mixer.Sound('zvuk-udara-po-myachiku.mp3')

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
        self.collideball()

    def collideball(self):
        global status
        global ball
        global table
        global score1
        global score2
        global l_scores
        if self.n == '1':
            if (status == 'serve' and table.touched2 and table.touched1) | (status == 'default' and table.touched1):
                d = sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
                if d < self.length + 5 :
                    if d < 25:
                        score2 += 1
                        status = 'lose'
                    else:
                        ax = self.length * cos(radians(self.angle))
                        ay = self.length * sin(radians(self.angle))
                        bx = ball.x - self.x
                        by = ball.y - self.y
                        a = sqrt(ax ** 2 + ay ** 2)
                        b = sqrt(bx ** 2 + by ** 2)
                        angle = acos((ax * bx + ay * by) / a / b)
                        h = b * sin(angle)
                        if h < 5:
                            self.sound.play()
                            ball.sender = 'player' + self.n
                            ball.angle = ball.angle + self.angle
                            ball.sh = 5000
                            sprites['table'].touched1 = True
                            sprites['table'].touched2 = False
                            status = 'default'
                    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
        elif self.n == '2':
            if (status == 'serve' and table.touched2 and table.touched1) | (status == 'default' and table.touched2):
                d = sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
                if d < self.length + 5 :
                    if d < 25:
                        score1 += 1
                        status = 'lose'
                    else:
                        ax = self.length * cos(radians(self.angle))
                        ay = self.length * sin(radians(self.angle))
                        bx = ball.x - self.x
                        by = ball.y - self.y
                        a = sqrt(ax ** 2 + ay ** 2)
                        b = sqrt(bx ** 2 + by ** 2)
                        angle = acos((ax * bx + ay * by) / a / b)
                        h = b * sin(angle)
                        if h < 5:
                            self.sound.play()
                            ball.sender = 'player' + self.n
                            ball.angle = ball.angle + self.angle
                            ball.sh = 5000
                            sprites['table'].touched1 = False
                            sprites['table'].touched2 = True
                            status = 'default'
                    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)


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
                    score2 += 1
                if self.sender == 'player2':
                    score1 += 1
            elif status == 'serve' and table.touched2 and table.touched1:
                if self.sender == 'player1':
                    score1 += 1
                if self.sender == 'player2':
                    score2 += 1
            else:
                if self.sender == 'player1':
                    score2 += 1
                if self.sender == 'player2':
                    score1 += 1
            l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
            status = 'lose'
            sprites['lose'].x = self.x
            sprites['lose'].y = self.y


class Menu():
    def __init__(self):
        sprites['settings'] = self
        self.rect = Rect(500, 75, 500, 630)
        self.btns = dict()
        self.btns['Руководство по игре'] = 0
        self.btns['Продолжить'] = 0
        self.btns['Новая игра'] = 0
        self.btns['Загрузить игру'] = 0
        self.btns['Сохранить игру'] = 0
        self.btns['Завершить партию'] = 0
        self.btns['Выйти из игры'] = 0
        self.t = 0

    def draw(self):
        global status
        global keys_pressed
        global pred
        if status == 'paused':
            draw.rect(mw, (200, 200, 255), self.rect, 0)
            i = 0
            mw.blit(default.render('Меню', True, (255, 0, 255)), (510, 75))
            for btn in self.btns.keys():
                self.btns[btn] = Rect(510, 140+i*80, 480, 70)
                draw.rect(mw, (0, 0, 0), self.btns[btn], 0)
                mw.blit(default.render(btn, True, (255, 0, 255)), (515, 140+i*80))
                i += 1
            if keys_pressed[K_ESCAPE] and t() - self.t >= 0.3:
                status = pred
                self.t = t()
            self.action(self.btnpressed())

    def btnpressed(self):
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                for btn in self.btns.keys():
                    if self.btns[btn].collidepoint(e.pos):
                        return btn

    def action(self, btn):
        global status
        global pred
        global maxscore
        global serves
        global score2
        global score1
        global level
        global last
        global player1
        global player2
        global starter
        global running
        global l_winner
        global l_scores
        if btn == 'Руководство по игре':
            status = 'description'
        if btn == 'Продолжить':
            status = pred
        if btn == 'Новая игра':
            status = 'newgame'
        if btn == 'Загрузить игру':
            try:
                with open('saved_game.txt', 'r', encoding='utf8') as file:
                    level, starter, maxscore, serves, score1, score2, player1.score, player2.score = file.read().split(';')
                    file.close()
                sprites['ball'].sender = starter
                maxscore = int(maxscore)
                serves = int(serves)
                score1 = int(score1)
                score2 = int(score2)
                player1.score = int(player1.score)
                player2.score = int(player2.score)
                l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
                i = 0
                while i < score2 + score1:
                    if i - last >= serves:
                        ball.sender = server
                        changep()
                        server = ball.sender
                        last = i
                    i += 1
                status = 'onserve'
            except:
                pass
        if btn == 'Сохранить игру' and pred != 'toserve' and pred != 'finish':
            with open('saved_game.txt', 'w', encoding='utf8') as file:
                file.write(f'{level};{starter};{maxscore};{serves};{score1};{score2};{player1.score};{player2.score}')
                file.close()
        if btn == 'Завершить партию':
            if score1 > score2:
                l_winner = default.render(f'Левый игрок победил!\nОчки за точность ударов: {player1.score}', True,
                                       (255, 0, 255))
            elif score1 < score2:
                l_winner = default.render(f'Правый игрок победил!\nОчки за точность ударов: {player2.score}', True,
                                       (255, 0, 255))
            else:
                if player1.score > player2.score:
                    l_winner = default.render(f'Левый игрок победил по очкам за точность ударов:\n{player1.score} > {player2.score}', True,
                                           (255, 0, 255))
                elif player1.score < player2.score:
                    l_winner = default.render(
                        f'Правый игрок победил по очкам за точность ударов:\n{player2.score} > {player1.score}', True,
                        (255, 0, 255))
                else:
                    l_winner = default.render('Ничья!', True,(255, 0, 255))
            try:
                os.remove(os.path.join('last_game.txt'))
            except Exception:
                pass
            status = 'finish'
        if btn == 'Выйти из игры':
            running = False

    def update(self):
        pass

    def reset(self):
        pass

class NewGame():
    def __init__(self):
        sprites['newgame'] = self
        self.rect = Rect(300, 250, 800, 400)
        self.maxscoreup = Rect(850, 260, 55, 55)
        self.maxscoredown = Rect(850, 320, 55, 55)
        self.servesup = Rect(790, 400, 55, 55)
        self.servesdown = Rect(790, 460, 55, 55)
        self.levele = Rect(560, 560, 150, 50)
        self.levelm = Rect(710, 560, 150, 50)
        self.levelh = Rect(860, 560, 150, 50)

    def draw(self):
        global maxscore
        global serves
        if status == 'newgame':
            draw.rect(mw, (200, 200, 255), self.rect, 0)
            mw.blit(default.render(f'Количество раундов: {maxscore}', True, (255, 0, 255)), (310, 280))
            mw.blit(default.render(f'Количество подач: {serves}', True, (255, 0, 255)), (310, 420))
            draw.rect(mw, (0, 0, 0), self.maxscoreup, 0)
            draw.rect(mw, (0, 0, 0), self.maxscoredown, 0)
            draw.rect(mw, (0, 0, 0), self.servesup, 0)
            draw.rect(mw, (0, 0, 0), self.servesdown, 0)
            draw.rect(mw, (0, 255, 0), self.levele, 0)
            draw.rect(mw, (255, 255, 0), self.levelm, 0)
            draw.rect(mw, (255, 0, 0), self.levelh, 0)
            mw.blit(default.render(r'/\ ', True, (255, 0, 255)), (865, 260))
            mw.blit(default.render(r'\/', True, (255, 0, 255)), (865, 320))
            mw.blit(default.render(r'/\ ', True, (255, 0, 255)), (805, 400))
            mw.blit(default.render(r'\/', True, (255, 0, 255)), (805, 460))
            mw.blit(default.render('Сложность:', True, (255, 0, 255)), (310, 550))
            self.checkpress()

    def checkpress(self):
        global status
        global maxscore
        global serves
        global score2
        global score1
        global player1
        global player2
        global last
        global level
        global l_scores
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                if self.maxscoreup.collidepoint(e.pos):
                    maxscore += 1
                if self.maxscoredown.collidepoint(e.pos):
                    maxscore -= 1
                if self.servesup.collidepoint(e.pos):
                    serves += 1
                if self.servesdown.collidepoint(e.pos):
                    serves -= 1
                if self.levele.collidepoint(e.pos):
                    for i in sprites.keys():
                        sprites[i].reset()
                    score1 = 0
                    score2 = 0
                    last = 0
                    level = 'easy'
                    sprites['player1'].length = 100
                    sprites['player2'].length = 100
                    sprites['ball'].speed = 300
                    player1.score = 0
                    player2.score = 0
                    status = 'toserve'
                    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
                if self.levelm.collidepoint(e.pos):
                    for i in sprites.keys():
                        sprites[i].reset()
                    score1 = 0
                    score2 = 0
                    last = 0
                    level = 'easy'
                    sprites['player1'].length = 70
                    sprites['player2'].length = 70
                    player1.score = 0
                    player2.score = 0
                    sprites['ball'].speed = 400
                    status = 'toserve'
                    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
                if self.levelh.collidepoint(e.pos):
                    for i in sprites.keys():
                        sprites[i].reset()
                    score1 = 0
                    score2 = 0
                    last = 0
                    level = 'easy'
                    sprites['player1'].length = 70
                    sprites['player2'].length = 70
                    player1.score = 0
                    player2.score = 0
                    sprites['ball'].speed = 500
                    status = 'toserve'
                    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)

    def update(self):
        pass

    def reset(self):
        pass

class Description():
    def __init__(self):
        global descr_text
        sprites['description'] = self
        self.text = descr_text
        self.rect = Rect(100, 60, 1200, 800)

    def draw(self):
        global status
        if status == 'description':
            draw.rect(mw, (50, 50, 50), self.rect, 0)
            for i in range(len(self.text)):
                mw.blit(default.render(self.text[i], True, (255, 0, 255)), (110, 70 + i * 60))

    def update(self):
        pass

    def reset(self):
        pass


def update():
    for i in sprites.keys():
        sprites[i].update()


def draw_display():
    global sprites
    for i in sprites.keys():
        sprites[i].draw()
    mw.blit(l_scores, (670, 5))
    if status == 'finish':
        mw.blit(l_winner, (100, 290))
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
    descr_text = [
        'Управление:',
        'Пробел, чтобы сменить подающего.',
        'Энтер, чтобы зафиксировать',
        'Дальше можно двигаться и пробел, чтобы подать.',
        'Игрок 1 управляется клавишами W, A, S, D',
        "Игрок 2 управляется клавишами L, P, ;, '",
        'Shift  и Ctrl вращение ракетки.',
        'Правила игры:',
        '1) Определите подающего',
        '2) Подайте',
        '3) Отбивайте мяч во вражескую половину стола,',
        'стараясь не задеть сетку'
    ]
    fps = 90
    status = 'toserve'
    pred = 'toserve'
    level = 'medium'
    score1 = 0
    score2 = 0
    serves = 2
    last = 0
    maxscore = 11
    server = 'player1'
    starter = 'player1'
    mixer.init()
    clock = time.Clock()
    running = True
    sprites = dict()
    table = Table()
    ball = Ball()
    lose = Lose(0, 0)
    player1 = Player('1', 100, 450, 0, 70, K_a, K_d, K_w, K_s, K_LSHIFT, K_LCTRL)
    player2 = Player('2', 1300, 450, 180, 70, K_l, K_QUOTE, K_p, K_SEMICOLON, K_RCTRL, K_RSHIFT)
    menu = Menu()
    description = Description()
    newgame = NewGame()
    scores_c = (255, 255, 255)
    font.init()
    default = font.SysFont('Arial', 55)
    l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
    l_winner = default.render('Left player won!', True, (255, 0, 255))
    tl = 0
    mw = display.set_mode((700, 700))
    display.set_caption('Ping-pong')
    background_image = transform.scale(image.load('tabletennis.jpg'), (700, 700))
    while running:
        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == MOUSEBUTTONDOWN:
                running = False
        mw.blit(background_image, (0, 0))
        mw.blit(font.SysFont('TimesNewRoman', 40).render('''Добро пожаловать в игру Ping-pong!''', True, (255, 100, 100)), (40, 20))
        mw.blit(font.SysFont('TimesNewRoman', 30).render('''Нажмите на окно, чтобы продолжить''',
                True, (100, 100, 100)), (200, 660))
        display.update()
        clock.tick(60)
    mw = display.set_mode((1400, 900))
    running = True
    try:
        with open('last_game.txt', 'r', encoding='utf8') as file:
            level, starter, maxscore, serves, score1, score2, player1.score, player2.score = file.read().split(';')
            file.close()
        sprites['ball'].sender = starter
        maxscore = int(maxscore)
        serves = int(serves)
        score1 = int(score1)
        score2 = int(score2)
        player1.score = int(player1.score)
        player2.score = int(player2.score)
        l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
        i = 0
        while i < score2 + score1:
            if i - last >= serves:
                ball.sender = server
                changep()
                server = ball.sender
                last = i
            i += 1
        status = 'onserve'
    except Exception:
        pass
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        keys_pressed = key.get_pressed()
        if status == 'toserve':
            if keys_pressed[K_SPACE] and t() - tl > 0.3:
                changep()
                starter = ball.sender
                tl = t()
            if keys_pressed[K_RETURN]:
                status = 'onserve'
        if status == 'onserve' or status == 'serve' or status == 'default':
            update()
        if status == 'onserve':
            if score1 + score2 - last >= serves:
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
                sprites[ball.sender].sound.play()
        if score1 >= maxscore and status != 'finish':
            l_winner = default.render(f'Левый игрок победил!\nОчки за точность ударов: {player1.score}', True, (255, 0, 255))
            status = 'finish'
            try:
                os.remove(os.path.join('last_game.txt'))
            except Exception:
                pass
        if score2 >= maxscore and status != 'finish':
            l_winner = default.render(f'Правый игрок победил!\nОчки за точность ударов: {player1.score}', True, (255, 0, 255))
            status = 'finish'
            try:
                os.remove(os.path.join('last_game.txt'))
            except Exception:
                pass
        if status == 'finish' and keys_pressed[K_SPACE]:
            for i in sprites.keys():
                sprites[i].reset()
            score1 = 0
            score2 = 0
            cnt = 0
            last = 0
            l_scores = default.render(str(score1) + ':' + str(score2), True, scores_c)
            status = 'toserve'
        if keys_pressed[K_ESCAPE] and status != 'paused' and t() - menu.t >= 0.3:
            if status in ['toserve', 'onserve', 'serve', 'finish', 'lose', 'default']:
                pred = status
            status = 'paused'
            menu.t = t()
        mw.fill((245, 155, 66))
        draw_display()
        clock.tick(fps)
    if pred != 'toserve' and pred != 'finish' or status in ['onserve', 'serve', 'lose', 'default']:
        with open('last_game.txt', 'w', encoding='utf8') as file:
            file.write(f'{level};{starter};{maxscore};{serves};{score1};{score2};{player1.score};{player2.score}')
            file.close()
    tl = t()
    mw = display.set_mode((700, 700))
    while t() - tl <= 1:
        for e in event.get():
            if e.type == QUIT:
                exit()
        mw.blit(background_image, (0, 0))
        mw.blit(font.SysFont('TimesNewRoman', 55).render('''До скорых встреч!''', True, (255, 100, 100)), (40, 20))
        display.update()
        clock.tick(60)
exit()
