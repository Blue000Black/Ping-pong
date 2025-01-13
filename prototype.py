from pygame import *
from random import randint

fps = 30
scoreL = 0
scoreR = 0
mw = display.set_mode((700,500))
display.set_caption('Ping-pong')
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, color, player_speed_y, player_x, player_y):
        super().__init__()
        self.rect = Rect(player_x, player_y, 20, 20)
        self.fill_color = color
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed_y = player_speed_y

class Player(GameSprite):
    def __init__(self, color, player_speed_y, player_x, player_y, sK_up, sK_down):
        super().__init__(color, player_speed_y, player_x, player_y)
        self.rect = Rect(player_x, player_y, 30, 100)
        self.fill_color = color
        self.sK_up = sK_up
        self.sK_down = sK_down
    def reset(self):
        draw.rect(mw, self.fill_color, self.rect)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[self.sK_up] and self.rect.y >= 5:
            self.rect.y -= self.player_speed_y
        if keys_pressed[self.sK_down] and self.rect.y <= 390:
            self.rect.y += self.player_speed_y

class Ball(GameSprite):
    def __init__(self, color, player_speed_y, player_x, player_y, player_speed_x):
        super().__init__(color, player_speed_y, player_x, player_y)
        a = randint(1, 2)
        b = randint(1, 2)
        if a == 1:
            self.player_speed_x = player_speed_x
        else:
            self.player_speed_x = (-1)*player_speed_x
        if b == 1:
            self.player_speed_y = player_speed_y
        else:
            self.player_speed_y = (-1)*player_speed_y
    def reset(self):
        draw.circle(mw, self.fill_color, (self.rect.x, self.rect.y), 5)
    def update(self):
        global fps
        global scoreL
        global scoreR
        global finish
        global scores_c
        if self.rect.y <= 5:
            self.player_speed_y *= -1
        if self.rect.y >= 495:
            self.player_speed_y *= -1
        if sprite.collide_rect(self, player1) or sprite.collide_rect(self, player2):
            self.player_speed_x *= -1
            fps += 1
        if self.rect.x <= 0 and finish == False:
            finish = True
            scoreR += 1
            scores_c = (255, 0, 0)
        if self.rect.x >= 700 and finish == False:
            finish = True
            scoreL += 1
            scores_c = (0, 0, 255)
        self.rect.x += self.player_speed_x
        self.rect.y += self.player_speed_y

player1 = Player((0, 0, 255), 7, 5, 200, K_w, K_s)
player2 = Player((255, 0, 0), 7, 665, 200, K_UP, K_DOWN)
ball = Ball((255, 255, 255), 6, 350, 250, 6)
scores_c = (255, 255, 255)
font.init()
font = font.SysFont('Arial', 55)
l_scores = font.render(str(scoreL)+':'+str(scoreR), True, scores_c)
l_resume = font.render('Press "R" to resume', True, (255, 255, 255))
l_restart = font.render('Press "P" to restart', True, (255, 255, 255))
l_winL = font.render('Blue player has won!', True, (0, 0, 255))
l_winR = font.render('Red player has won!', True, (255, 0, 0))
l_draw = font.render('You have a draw!', True, (255, 255, 255))
game = True
finish = False
restart = False
while game:
    mw.fill((0, 50, 0))
    draw.rect(mw, (0, 0, 0), Rect(349, 0, 2, 500))
    l_scores = font.render(str(scoreL) + ':' + str(scoreR), True, scores_c)
    mw.blit(l_scores, (315, 5))
    player1.reset()
    player2.reset()
    ball.reset()
    player1.update()
    player2.update()
    ball.update()
    events = event.get()
    for e in events:
        if e.type == QUIT:
            game = False
    if finish == True:
        ball.player_speed_x = 0
        ball.player_speed_y = 0
        player1.player_speed_y = 0
        player2.player_speed_y = 0
        keys_pressed = key.get_pressed()
        if restart == False:
            if keys_pressed[K_p]:
                fps = 30
                x = 5*fps
                restart = True
        if keys_pressed[K_r]:
            scores_c = (255, 255, 255)
            del(player1)
            del(player2)
            del(ball)
            fps = 30
            player1 = Player((0, 0, 255), 7, 5, 200, K_w, K_s)
            player2 = Player((255, 0, 0), 7, 665, 200, K_UP, K_DOWN)
            ball = Ball((255, 255, 255), 6, 350, 250, 6)
            finish = False
        elif restart == True:
            x -= 1
            l_time = font.render(str(x//30+1), True, (0, 255, 0))
            mw.fill((0, 0, 0))
            mw.blit(l_scores, (315, 5))
            mw.blit(l_time, (320, 310))
            mw.blit(font.render('Get ready to restart!', True, (0, 255, 0)), (150, 250))
            if scoreL > scoreR:
                mw.blit(l_winL, (150, 200))
            elif scoreL < scoreR:
                mw.blit(l_winR, (150, 200))
            else:
                mw.blit(l_draw, (150, 200))
            if x < 0:
                scores_c = (255, 255, 255)
                scoreL = 0
                scoreR = 0
                del(player1)
                del(player2)
                del(ball)
                player1 = Player((0, 0, 255), 7, 5, 200, K_w, K_s)
                player2 = Player((255, 0, 0), 7, 665, 200, K_UP, K_DOWN)
                ball = Ball((255, 255, 255), 6, 350, 250, 6)
                finish = False
                restart = False
        else:
            mw.blit(l_resume, (150, 245))
            mw.blit(l_restart, (150, 290))

    display.update()
    clock.tick(fps)
