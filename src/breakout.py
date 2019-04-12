#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License
#
##############################################################

# Modified for educational purposes for the
# CNU Department of Physics, Computer Science and Engineering
#
# Spring 2019 Semester
# Mathew Bartgis, David Conner
#

import sys
import random
import math
import os
import pygame
from pygame.locals import *
import struct


pygame.font.init() #https://stackoverflow.com/questions/20546661/pygame-display-variable-on-display-window
myfont = pygame.font.SysFont('Comic Sans MS', 30)
small_font = pygame.font.SysFont('Comic Sans MS', 20)
end_font = pygame.font.SysFont('Comic Sans MS', 100)

############################################################
#                       BUGS                               #
#The ball keeps the same angle when transitioning between levels.
#If the ball is going down when the level ends, it will be going down when the next level begins
#Add a codition that prevents the ball from being too horizontally moving
#The ball sometimes gets stuck in the paddle
#The motion can be completely horizontal
#When the ball is caught between the brick and the top of the screen sometimes this results in death
############################################################

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../img', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image
    except pygame.error:
        print('Cannot load image:', fullname)


def calcnewpos(rect, vector):
    (angle, z) = vector
    (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
    return rect.move(dx, dy)

##################################################################################################################

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('green_ball.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0
        self.strength = 100
        self.speed = 10.25
        self.state = "still"
        self.color_count = 0
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.rect.center = (self.area.centerx, 440)

    def update(self):

        self.color_count += 1
        color_rate = 10
        colors = ['red_ball.png', 'orange_ball.png', 'yellow_ball.png', 'green_ball.png', 'blue_ball.png',
                  'indigo_ball.png', 'violet_ball.png']

        if self.color_count >= color_rate * len(colors):
            self.color_count = 0

        self.image = load_png(colors[self.color_count // color_rate])

        newpos = calcnewpos(self.rect, self.vector)

        self.rect = newpos
        (angle, self.speed) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            # if (tr and tl) or (br and bl):
            #     angle = -angle
            # elif (tr and br) or (tl and bl):
            #     angle = math.pi - angle
            # if (bl and br):
            #     self.reinit()
            #     player1.reinit()
            #     player1.lives -= 1
            if (bl and br):
                self.reinit()
                player1.reinit()
                player1.lives -= 1
            elif (tr and br) or (tl and bl):
                angle = math.pi - angle
            else:
                angle = -angle

        for sprite in bricksprite:
            if self.rect.colliderect(sprite.rect) and not self.hit and sprite.health > 0:
                print('collision')
                tr = sprite.rect.collidepoint(newpos.topright)
                tl = sprite.rect.collidepoint(newpos.topleft)
                br = sprite.rect.collidepoint(newpos.bottomright)
                bl = sprite.rect.collidepoint(newpos.bottomleft)
                print(tr, tl, br, bl)
                if (tr and tl) or (br and bl):
                    print('hit bottom')
                    angle = -angle
                    sprite.health -= self.strength
                    player1.game_score += 1
                    self.hit = not self.hit
                elif (tl and bl) or (tr and br):
                    print('hit side')
                    angle = math.pi - angle
                    sprite.health -= self.strength
                    player1.game_score += 1
                    self.hit = not self.hit
                elif tl or bl or br or tr:
                    print('hit corner')
                    angle = angle + math.pi + .05
                    sprite.health -= self.strength
                    player1.game_score += 1
                    self.hit = not self.hit

        else:
            # Deflate the rectangles so you can't catch a ball behind the bat
            player1.rect.inflate(-3, -3)

            # Do ball and bat collide?
            # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
            # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
            # bat, the ball reverses, and is still inside the bat, so bounces around inside.
            # This way, the ball can always escape and bounce away cleanly
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                # angle = -angle
                # self.hit = not self.hit
                tr = player1.rect.collidepoint(newpos.topright)
                tl = player1.rect.collidepoint(newpos.topleft)
                br = player1.rect.collidepoint(newpos.bottomright)
                bl = player1.rect.collidepoint(newpos.bottomleft)
                if (tr and tl) or (br and bl):
                    angle = -angle
                    self.hit = not self.hit
                elif (tl and bl) or (tr and br):
                    angle = angle + math.pi
                    self.hit = not self.hit
                elif tr or tl or br or bl:
                    angle = -angle
                    self.hit = not self.hit

            elif self.hit:
                self.hit = not self.hit

        self.vector = (angle, self.speed)


class Paddle(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    X = 0
    Y = 1

    game_score = 0
    level = 1
    lives = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        self.rect.midbottom = self.area.midbottom
        # self.rect.midtop = self.area.midtop

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveleft(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] - self.speed
        self.state = "moveleft"

    def moveright(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] + self.speed
        self.state = "moveright"

    def still(self):
        self.movepos = [0, 0]
        self.state = "still"


class Brick(pygame.sprite.Sprite):

    def __init__(self, coordinate, health=100, power=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('block.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = health
        self.coordinate = coordinate
        self.state = "still"
        self.reinit()
        self.power = power

    def reinit(self):
        self.state = "still"
        self.rect.topleft = self.coordinate#self.area.topright

    def update(self):
        brick_bg = pygame.Surface((100, 30))
        brick_bg = brick_bg.convert()
        if self.health > 0:
            if self.health > 75:
                brick_bg.fill((55,208,51))
            elif self.health > 50:
                brick_bg.fill((165,208,66))
            elif self.health > 25:
                brick_bg.fill((208,160,71))
            elif self.health > 0:
                brick_bg.fill((208,66,36))
            screen.blit(brick_bg, self.rect)
            bricksprite.draw(screen)
        else:
            self.kill()
            brick_bg.fill((0, 0, 0))
            screen.blit(brick_bg, self.rect)

###################################################################################################################

def set_bricks():
    global bricksprite

    for i in range(0,626,110):
        for j in range(50,151,45):
            brick = Brick((i,j))
            if i == 0 and j == 50:
                bricksprite = pygame.sprite.RenderPlain(brick)
            else:
                bricksprite.add(brick)

play = False
start_bool = True

def game_end():
    try:
        os.remove("breakout_save.dat")
    except:
        pass
    screen.blit(background, (0, 0))
    end_screen = load_png("gameover.png")
    end_txt = myfont.render("Press Space Bar to Play Again", False, (255, 255, 255))
    end_score = myfont.render("SCORE: " + str(player1.game_score), False, (255, 255, 100))
    end_level = myfont.render("LEVEL: " + str(player1.level), False, (255, 255, 100))
    screen.blit(end_screen, (25, 125))
    screen.blit(end_score, (265, 300))
    screen.blit(end_level, (276, 345))
    screen.blit(end_txt, (120, 400))
    # screen.blit(background, ball.rect, ball.rect)  # cover up ball
    # screen.blit(background, player1.rect, player1.rect)  # cover up paddle
    # pygame.display.flip()


def startup():
    global play
    play = False
    screen.blit(background, (0, 0))
    welcome_screen = load_png("breakoutstart.png")
    start_text = myfont.render("Press Space Bar to Start Game", False, (255, 255, 255))
    screen.blit(welcome_screen, (45, 125))
    screen.blit(start_text, (100, 300))
    # screen.blit(background, ball.rect, ball.rect)  # cover up ball
    # screen.blit(background, player1.rect, player1.rect)  # cover up paddle
    # pygame.display.flip()

pause_bool = False

def pause():
    ball.state = 'still'
    screen.blit(background, (0, 0))
    pause_screen = end_font.render("PAUSED", False, (255, 255, 255))
    pause_txt = myfont.render("Press Escape to Resume Game", False, (255, 255, 255))
    screen.blit(pause_screen, (125, 125))
    screen.blit(pause_txt, (120, 300))

def start_game():
    try:
        with open("breakout_save.dat", "rb") as file:
            ba = bytearray(file.read(struct.calcsize(">5idd???ii")))
            player1.game_score, player1.level, player1.lives, ball.rect[0], ball.rect[1], z, theta, run, play, pause, player1.X, player1.Y = struct.unpack(">5idd???ii", ba)
            ball.vector = (theta, z)
            print("Unpack first 42 bytes")
            file.seek(struct.calcsize(">5idd???ii"))
            brick_data = file.read()
            #len_brick_data = len(brick_data)
            chunk_size = struct.calcsize(">3i?")
            for i in range(len(brick_data)//chunk_size):
                brickx, bricky, health, pwr = struct.unpack(">3i?", brick_data[i * chunk_size:(i + 1) * chunk_size])
                brick = Brick((brickx,bricky), health, pwr)
                print("Unpack bricks")
                if i == 0:
                    global bricksprite
                    bricksprite = pygame.sprite.RenderPlain(brick)
                else:
                    bricksprite.add(brick)
    except Exception as e:
        print(e)
        print('start')
        player1.lives = 3
        player1.game_score = 0
        player1.reinit()
        ball.reinit()
        set_bricks()

#################################################################################################################

def main():
    # Initialize screen
    pygame.init()


    global screen
    screen = pygame.display.set_mode((650, 480))
    pygame.display.set_caption('Breakout')

    # Fill background
    global background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialize players
    global player1
    player1 = Paddle()

    # Initialize ball
    global ball

    #changing the speed here does nothing
    #the speed of the ball
    rand = 0.1 * random.randint(5, 8)
    ball = Ball((0.47, 10.25))
    # Initialize sprites
    global ballsprite

    playersprites = pygame.sprite.RenderPlain(player1)
    ballsprite = pygame.sprite.RenderPlain(ball)

    set_bricks()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize clock
    clock = pygame.time.Clock()


################################################################################################################
#we should add a condition that makes the vector of the ball reset after the level has gone up or the game restarts
    run = True
    global play
    global start_bool
    global pause_bool

    # Event loop
    while run:

        if not play:
            if start_bool:
                startup()
            else:
                game_end()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play = True
                        start_bool = False
                        start_game()

        if play and not pause_bool:
            # Make sure game doesn't run at more than 60 frames per second
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    with open(os.path.join("breakout_save.dat"), "wb") as file:
                        ba = bytearray()
                        ba.extend(struct.pack(">5idd???ii", player1.game_score, player1.level, player1.lives, ball.rect[0],
                                    ball.rect[1], ball.vector[1], ball.vector[0], run, play, pause, player1.X, player1.Y))

                        for brick in bricksprite:
                            ba.extend(struct.pack('>3i?', brick.coordinate[0], brick.coordinate[1], brick.health, brick.power))

                        file.write(ba)

                    run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player1.moveleft()
                    if event.key == pygame.K_RIGHT:
                        player1.moveright()

                    elif event.key == pygame.K_SPACE:
                        ball.state = 'moving'

                    if event.key == pygame.K_q:
                        print("quit")
                        run = False
                    if event.key == pygame.K_r:
                        start_game()

                    if event.key == pygame.K_ESCAPE:
                        pause_bool = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player1.still()

            screen.blit(background, ball.rect, ball.rect)   # cover up ball
            screen.blit(background, player1.rect, player1.rect)  # cover up paddle

            x = 'Score: ' + str(player1.game_score)
            score = small_font.render(x, False, (255, 255, 255))
            level = small_font.render('Level: ' + str(player1.level), False, (255, 255, 255))
            heart = load_png("Heart.png")
            screen.blit(background, (0, 0))
            screen.blit(score, (5, 5))
            screen.blit(level, (550, 5))

            if ball.state == 'still':
                txt = myfont.render('Press Space Bar to Launch Ball', False, (255, 255, 255))
                screen.blit(txt, (100, 300))

            # brick1.update()     # disappears if health <=0, stays otherwise

            if ball.state == 'moving':
                ballsprite.update()
                playersprites.update()

            bricksprite.update()

            ballsprite.draw(screen)  # draw updated ball
            playersprites.draw(screen)  # draw updated paddle

            if not bricksprite:
                set_bricks()
                ball.speed += 25.0
                ball.reinit()
                player1.reinit()
                player1.lives += 1
                player1.level += 1

            if 0 < player1.lives < 4:
                x = 340
                for i in range(player1.lives):
                    screen.blit(heart, (x, 5))
                    x -= 35
            elif player1.lives >= 4:
                lives = myfont.render('{}x'.format(player1.lives), False, (255, 255, 255))
                if player1.lives >= 10:
                    screen.blit(lives, (275, 5))
                else:
                    screen.blit(lives, (285, 5))
                screen.blit(heart, (325, 10))
            else:
                play = False


            # if player1.lives == 3:
            #     screen.blit(heart, (530, 445))
            #     screen.blit(heart, (565, 445))
            #     screen.blit(heart, (600, 445))
            # elif player1.lives == 2:
            #     screen.blit(heart, (565, 445))
            #     screen.blit(heart, (600, 445))
            # elif player1.lives == 1:
            #     screen.blit(heart, (600, 445))
            # else:
            #     game_end()

            pygame.display.flip()

        elif play and pause_bool:
            pause()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open(os.path.join("breakout_save.dat"), "wb") as file:
                        ba = bytearray()
                        ba.extend(struct.pack(">5idd???ii", player1.game_score, player1.level, player1.lives, ball.rect[0],
                                    ball.rect[1], ball.vector[1], ball.vector[0], run, play, pause, player1.X, player1.Y))

                        for brick in bricksprite:
                            ba.extend(struct.pack('>3i?', brick.coordinate[0], brick.coordinate[1], brick.health, brick.power))

                        file.write(ba)
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_bool = False
                        ball.state = 'moving'

if __name__ == '__main__':
    main()
