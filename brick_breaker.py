
# project started on 04/04/2021
from colors import Color
import pygame
import os
import math
from random import randint
import sys
pygame.font.init()

WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('boobs')

FPS = 60

randval = 10

ball_size = (20, 20)
brick_width = 80
# brick_size = (brick_width, round(brick_width*1.0691823899))
brick_size = (brick_width, 32)

top_border = pygame.Rect(0, 0, WIDTH, 1)
right_border = pygame.Rect(WIDTH, 0, 1, HEIGHT)
left_border = pygame.Rect(0, 0, 1, HEIGHT)

ball_out = pygame.USEREVENT + 1
win_event = pygame.USEREVENT + 2

bg = Color('light pink').rgb
black = Color('black').rgb


lostifonti = pygame.font.SysFont('impact', 100)
winfont = pygame.font.SysFont('impact', 20)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ball_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('balz', 'ball.png'))), ball_size)


class Brick:
    def __init__(self, x, y, wins):
        self.x = x
        self.y = y
        self.top_border = pygame.Rect(x, y, brick_size[0], 1)
        self.bottom_border = pygame.Rect(x, y + brick_size[1] - 1, brick_size[0], 1)
        self.right_border = pygame.Rect(x + brick_size[0] - 1, y, 1, brick_size[1])
        self.left_border = pygame.Rect(x, y, 1, brick_size[1])
        self.borders = [self.right_border, self.top_border, self.left_border, self.bottom_border]
        if wins > 3:
            wins = 3
        self.hp = randint(1, 2 + wins)
        # self.hp = randint(1, 2)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 50, randint(HEIGHT - 270, HEIGHT - 180), ball_size[0], ball_size[1])
        self.angle = deg_to_rd(93)
        self.height = self.rect.height
        self.width = self.rect.width
        randomize_angle(self.angle)
        self.speed = 2.4

    def reset_pos(self):
        self.angle = deg_to_rd(93)
        randomize_angle(self.angle)
        self.rect.y = randint(HEIGHT - 140, HEIGHT - 100)
        self.rect.x = randint(WIDTH // 2 - 80, WIDTH // 2 - 20)


def randomize_angle(angle, r=randval):
    angle += deg_to_rd(randint(-r, r))
    return angle


def check_static(x, y, px, py, angle):
    angle += deg_to_rd(randint(-randval - 22, randval + 22)) * (px - 1.5 <= x <= px + 1.5)
    angle += deg_to_rd(randint(-randval - 22, randval + 22)) * (py - 1.5 <= y <= py + 1.5)
    return angle


def deg_to_rd(x): return x * math.pi / 180


def draw_stuff(bar, balls, bricks, wins, score):
    win.fill(bg)
    pygame.draw.rect(win, black, bar)
    score_text = winfont.render(f'score: {score}    wins: {wins}', True, Color('white').rgb)
    win.blit(score_text, (20, 20))

    for ball in balls:
        win.blit(ball_img, (ball.rect.x, ball.rect.y))

    for b in bricks:
        brick_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join('balz', f'brick{b.hp}.png'))),
                                           brick_size)
        win.blit(brick_img, (b.x, b.y))

    pygame.display.update()


def bar_movement(keys, bar, speed):
    if keys[pygame.K_q] and bar.x - speed > 0:  # LEFT
        bar.x -= speed
    if keys[pygame.K_d] and bar.x + speed < WIDTH - bar.width:  # RIGHT
        bar.x += speed


def ball_movement(balls, bar, bricks: list, score, wins):
    
    k = False   # Collision bool
    w = False   # Potential win bool
    bh = False  # Brick hit bool

    for ball in balls:
        rect = ball.rect
        
        px, py = rect.x, rect.y

        # print(rect.x, rect.y)
        
        if rect.colliderect(bar):
            ball.angle = - ball.angle
            k = True

        if rect.colliderect(right_border):
            ball.angle = math.pi - ball.angle
            k = True

        if rect.colliderect(left_border):
            ball.angle = math.pi - ball.angle
            k = True

        if rect.colliderect(top_border):
            ball.angle = -ball.angle
            k = True

        if rect.y > HEIGHT:
            pygame.event.post(pygame.event.Event(ball_out))
            balls.remove(ball)
            break

        for b in bricks:
            if rect.colliderect(b.top_border):
                ball.angle = -ball.angle
                b.hp -= 1
                if b.hp <= 0:
                    bricks.remove(b)
                    w = True
                k = True
                bh = True
                break

            if rect.colliderect(b.bottom_border):
                ball.angle = - ball.angle
                b.hp -= 1
                if b.hp <= 0:
                    bricks.remove(b)
                    w = True
                k = True
                bh = True
                break

            if rect.colliderect(b.right_border):
                ball.angle = math.pi - ball.angle
                b.hp -= 1
                if b.hp <= 0:
                    bricks.remove(b)
                    w = True
                k = True
                bh = True
                break

            if rect.colliderect(b.left_border):
                ball.angle = math.pi - ball.angle
                b.hp -= 1
                if b.hp <= 0:
                    bricks.remove(b)
                    w = True
                k = True
                bh = True
                break

        if w and len(bricks) == 0:
            pygame.event.post(pygame.event.Event(win_event))

        rect.x += math.cos(ball.angle) * ball.speed
        rect.y += math.sin(ball.angle) * ball.speed

        if k:
            ball.angle = check_static(rect.x, rect.y, px, py, ball.angle)
            ball.angle = randomize_angle(ball.angle)

            max_speed = 5 + wins * 0.45
            if max_speed > 15:
                max_speed = 15

            if ball.speed < max_speed:
                ball.speed += 0.05 + wins*0.06

        if bar.x < rect.x < bar.x + bar.width and bar.y < rect.y < bar.y + bar.height:
            rect.y -= rect.y - bar.y + ball.height
            ball.angle = randomize_angle(ball.angle, randval + 20)

    # angle += 0.25 * (math.pi / 2 - 0.08 <= angle <= math.pi / 2 + 0.08)    # avoid going vertically

    # angle -= 0.25 * (ball.x == 0)

    # m = ((py - ball.y) / (px - ball.x))     # slope
    score += bh * 1
    return score


def make_bricks(bricks, wins):
    x = 63
    m = HEIGHT - 400 + wins * (brick_size[1] + 6)
    if m > HEIGHT - 150:
        m = HEIGHT - 150
    while x < WIDTH - 90:
        y = 55
        while y < m:
            bricks.append(Brick(x, y, wins))
            # print(x, y)
            y += brick_size[1] + 5
        x += 85


def loose():
    draw_text = lostifonti.render('You lose', True, Color('white').rgb)
    win.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


def win_func():
    draw_text = lostifonti.render('You win', True, Color('white').rgb)
    win.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    wins = 0
    score = 0
    bar_speed = 6.5
    bar_speed += 0.45 * wins
    bar = pygame.Rect(WIDTH // 2 - 90, HEIGHT - 80, 130, 17)
    balls = [Ball()]
    
    bricks = []
    make_bricks(bricks, wins)

    draw_stuff(bar, balls, bricks, wins, score)
    pygame.time.delay(1000)

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == ball_out:
                if len(balls) == 0:
                    loose()
                    main()

            if event.type == win_event or keys_pressed[pygame.K_RCTRL]:
                balls.append(Ball())
                wins += 1

                for b in balls:
                    b.speed -= 5 * (b.speed >= 9)
                    b.reset_pos()
                bricks = []
                make_bricks(bricks, wins)
                if bar_speed < 20:
                    bar_speed += 0.45*wins
                bar.x = WIDTH // 2 - 90
                draw_stuff(bar, balls, bricks, wins, score)
                pygame.time.delay(1500)
                continue

        keys_pressed = pygame.key.get_pressed()
        bar_movement(keys_pressed, bar, bar_speed)
        score = ball_movement(balls, bar, bricks, score, wins)

        draw_stuff(bar, balls, bricks, wins, score)


if __name__ == '__main__':
    main()
