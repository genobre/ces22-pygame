# Sprite classes for platform game
import sys
import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2


class Spritesheet:
    # utility class for loading spritesheets
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert_alpha()
        self.cols = 0
        self.rows = 0
        self.totalCellCount = 0
        self.rect = 0
        self.cellWidth = 0
        self.cellHeight = 0
        self.cellCenter = 0

    def sprt(self, cols, rows, cellindex):
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([(0, 0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h), (-hw, -h), (-w, -h), ])
        image = pg.Surface((w, h))
        image.blit(self.sheet, (0, 0), self.cells[cellindex])
        image = pg.transform.scale(image, (w*2, h*2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, velocity = 1):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.swim_r = False
        self.swim_l = False
        self.swim_up = False
        self.swim_down = False

        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.swim_r_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (16, HH)

        self.pos = vec(16, HH)
        self.vel = velocity
        self.points = 0

    def load_images(self):
        self.swim_r_frames = [self.game.tamasprite.sprt(5, 1, 0 % 5),
                                self.game.tamasprite.sprt(5, 1, 1 % 5),
                                self.game.tamasprite.sprt(5, 1, 2 % 5),
                                self.game.tamasprite.sprt(5, 1, 3 % 5),
                                self.game.tamasprite.sprt(5, 1, 4 % 5)]
        for frame in self.swim_r_frames:
            frame.set_colorkey(BLACK)
        self.swim_l_frames = []
        for frame in self.swim_r_frames:
            frame.set_colorkey(BLACK)
            self.swim_l_frames.append(pg.transform.flip(frame, True, False))

    def keys(self):
        k = pg.key.get_pressed()

        if k[pg.K_LEFT]: self.xVelocity = -self.vel
        elif k[pg.K_RIGHT]: self.xVelocity = self.vel
        else: self.xVelocity = 0

        if k[pg.K_DOWN]: self.yVelocity = self.vel
        elif k[pg.K_UP]: self.yVelocity = -self.vel
        else: self.yVelocity = 0

    def update(self):
        self.animate()
        if ((self.xVelocity > 0 and self.rect.right < (W - 15)) or (self.xVelocity < 0 and self.rect.left > 15)):
            self.rect.right += self.xVelocity
        if ((self.yVelocity > 0 and self.rect.bottom < (H - 15)) or (self.yVelocity < 0 and self.rect.top > 15)):
            self.rect.bottom += self.yVelocity

    def animate(self):
        now = pg.time.get_ticks()
        # show swimming animation
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.swim_r_frames)
            bottom = self.rect.bottom
            if self.xVelocity >= 0:
                self.image = self.swim_r_frames[self.current_frame]
            else:
                self.image = self.swim_l_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

class Bubble(pg.sprite.Sprite):
    def __init__(self,x_init, y_init,size, radius = 4, velocity = 5):
        pg.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2*radius,2*radius))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.velocity = velocity
        self.distance = size
        self.rect.left = x_init
        self.rect.centery = y_init

    def update(self):
        self.rect.right += 5

class PlasticBag(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.plasticbag
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.floating_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, 3492])
        self.rect.y = randrange(H)
        self.vy = 0
        self.vx = 1
        self.dy = 0.25

    def load_images(self):
        self.floating_frames = [self.game.plasticsprite.sprt(6, 1, 0 % 6),
                                self.game.plasticsprite.sprt(6, 1, 1 % 6),
                                self.game.plasticsprite.sprt(6, 1, 2 % 6),
                                self.game.plasticsprite.sprt(6, 1, 3 % 6),
                                self.game.plasticsprite.sprt(6, 1, 4 % 6),
                                self.game.plasticsprite.sprt(6, 1, 5 % 6)]
        for frame in self.floating_frames:
            frame.set_colorkey(BLACK)

    def update(self):
        self.animate()
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 1 or self.vy < -1:
            self.dy *= -1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > 3492 or self.rect.right < -100:
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        # show swimming animation
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.floating_frames)
            self.image = self.floating_frames[self.current_frame]
        self.mask = pg.mask.from_surface(self.image)