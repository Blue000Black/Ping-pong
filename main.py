from pygame import *
from random import randint

fps = 30
scoreL = 0
scoreR = 0
mw = display.set_mode((700,500))
display.set_caption('Ping-pong')
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, color, player_speed, player_x, player_y):
        super().__init__()
        self.rect = Rect(player_x, player_y, 30, 100)
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed = player_speed
        self.fill_color = color
    def reset(self):
        draw.rect(mw, self.fill_color, self.rect)

class Player(GameSprite):
    def __init__(self, color, player_speed, player_x, player_y, sK_up, sK_down):
        super().__init__(color, player_speed, player_x, player_y)
        self.sK_up = sK_up
        self.sK_down = sK_down
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[self.sK_up] and self.rect.y >= 50:
            self.rect.y -= self.player_speed
        if keys_pressed[self.sK_down] and self.rect.y <= 450:
            self.rect.y += self.player_speed

class Ball(GameSprite):
    def update(self):
        if self.rect.y >= 0:
            self.rect.y -= self.player_speed
        else:
            del(self)

sprites = list()
player1 = Player((0, 0, 255), 4, 5, 220, K_w, K_s)
player2 = Player((255, 0, 0), 4, 665, 230, K_UP, K_DOWN)
sprites.append(player1)
sprites.append(player2)
font.init()
font = font.SysFont('Arial', 55)
game = True
while game:
    mw.fill((0, 50, 0))
    draw.rect(mw, (0,0,0), Rect(349, 0, 2, 500))
    for s in sprites:
        s.reset()
        s.update()
    events = event.get()
    for e in events:
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(fps)
