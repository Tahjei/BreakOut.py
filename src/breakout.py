#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License
#
##############################################################
#
# Modified for educational purposes for the
# CNU Department of Physics, Computer Science and Engineering
#
# Spring 2019 Semester
# Mathew Bartgis, David Conner
#

VERSION = "0.4"

import sys
import random
import math
import os
import pygame
from pygame.locals import *


pygame.font.init() #https://stackoverflow.com/questions/20546661/pygame-display-variable-on-display-window
myfont = pygame.font.SysFont('Comic Sans MS', 30)


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


class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('ball.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0
        self.strength = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.rect.center = (self.area.centerx,440)

    def update(self):

        newpos = calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                angle = -angle
            if (tl and bl) or (tr and br):
                angle = math.pi - angle
            if (bl and br):
                self.reinit()#raise pygame.error("You lose!") #Right now just throws an error. Was looking into how to make a new
                                                #window pop up with a button: Play again? Y/N. Still working on that.
                                                    #But the ball stops the game when it hits the bottom, so I think that fulfulls the requirement.

        else:
            # Deflate the rectangles so you can't catch a ball behind the bat
            player1.rect.inflate(-3, -3)

            # Do ball and bat collide?
            # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
            # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
            # bat, the ball reverses, and is still inside the bat, so bounces around inside.
            # This way, the ball can always escape and bounce away cleanly
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = -angle
                self.hit = not self.hit
            elif self.rect.colliderect(brick1.rect) == 1 and not self.hit and brick1.health > 0:
                tr = not self.rect.collidepoint(brick1.rect.topright)
                tl = not self.rect.collidepoint(brick1.rect.topleft)
                br = not self.rect.collidepoint(brick1.rect.bottomright)
                bl = not self.rect.collidepoint(brick1.rect.bottomleft)
                print(tr,tl,br,bl)
                player1.game_score += 1
                if (tr and tl) or (br and bl):
                    print('hit bottom')
                    angle = -angle
                    brick1.health -= self.strength
                    self.hit = not self.hit
                if (tl and bl) or (tr and br):
                    print('hit side')
                    angle = math.pi - angle
                    brick1.health -= self.strength
                    self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit

        self.vector = (angle, z)


class Paddle(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    X = 0
    Y = 1

    game_score = 0
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

    def __init__(self, coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('basic_block.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = 100
        self.coordinate = coordinate
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.rect.topright = self.coordinate#self.area.topright

    def update(self):
        brick_bg = pygame.Surface((128, 64))
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
            brick_bg.fill((0, 0, 0))
            screen.blit(brick_bg, self.rect)


def main():
    # Initialize screen
    pygame.init()


    global screen
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Tom\'s Pong: v' + str(VERSION))

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
    speed = 13
    rand = 0.1 * random.randint(5, 8)
    ball = Ball((0.47, speed))

    global brick1
    brick1 = Brick((240,240))

    # Initialize sprites
    global bricksprite

    playersprites = pygame.sprite.RenderPlain(player1)
    ballsprite = pygame.sprite.RenderPlain(ball)
    bricksprite = pygame.sprite.RenderPlain(brick1)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exit Game?')
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.moveleft()
                if event.key == pygame.K_RIGHT:
                    player1.moveright()
                if event.key == pygame.K_SPACE and ball.state == 'moving':
                    ball.state = 'still'
                elif event.key == pygame.K_SPACE and ball.state == 'still':
                    ball.state = 'moving'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1.still()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        screen.blit(background, ball.rect, ball.rect)   # cover up ball
        screen.blit(background, player1.rect, player1.rect) # cover up paddle

        x = str(player1.game_score)
        score = myfont.render(x, False, (255, 255, 255))
        lives = myfont.render(u'\u2764\u2764\u2764', False, (255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(score, (0, 0))
        # if player1.lives == 3:                    #Working on displaying lives in corner
        #     screen.blit(u'\u2764\u2764\u2764')
        # elif player1.lives == 2:
        #     pass

        brick1.update()     # disappears if health <=0, stays otherwise

        if ball.state == 'moving':
            ballsprite.update()
            playersprites.update()
        bricksprite.update()

        ballsprite.draw(screen) # draw updated ball
        playersprites.draw(screen)  # draw updated paddle

        pygame.display.flip()


if __name__ == '__main__':
    main()
