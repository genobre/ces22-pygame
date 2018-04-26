import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game(object):
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((W, H))
        pg.display.set_caption("Tama's first adventure")
        self.clock = pg.time.Clock()
        self.running = True
        self.bg = pg.image.load("Fase_1.png").convert_alpha()
        self.soil = pg.image.load("soil.png").convert_alpha()
        self.bgWidth, self.bgHeight = self.bg.get_rect().size
        self.playerPosX = 16
        self.playerPosY = HH
        self.stageWidth = self.bgWidth
        self.stagePosX = 0
        self.stageHeight = self.bgHeight
        self.stagePosY = 0
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.tamasprite = Spritesheet(path.join(img_dir, "tama.png"))
        self.plasticsprite = Spritesheet(path.join(img_dir, "plastic_bag.png"))
        self.krillsprite = Spritesheet(path.join(img_dir, "shrimp.png"))
        self.bubblesprite = Spritesheet(path.join(img_dir, "bubble.png"))
        # load sounds

    def new(self):
        # start a new game
        # self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        # self.powerups = pg.sprite.Group()
        self.plasticbag = pg.sprite.Group()
        self.krills = pg.sprite.Group()
        self.player = Player(self)
        self.plastic_timer = 0
        self.krill_timer = 0
        self.flag_space = False
        self.bubbles = list([])
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.player.keys()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.player.update()
        self.all_sprites.update()

        ##spawn a plasticbag?
        now = pg.time.get_ticks()
        if now - self.plastic_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.plastic_timer = now
            PlasticBag(self)
        # hit mobs?
        plastic_hits = pg.sprite.spritecollide(self.player, self.plasticbag, False, pg.sprite.collide_mask)
        if plastic_hits:
            self.playing = False

        ##spawn a krill?
        if now - self.krill_timer > 2000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.krill_timer = now
            Krill(self)

        ## check
        self.playerPosX += self.player.vel.x
        self.playerPosY += self.player.vel.y
        if self.playerPosX > self.stageWidth - tamaWidth / 2:
            self.playerPosX = self.stageWidth - tamaWidth / 2
        if self.playerPosX < tamaWidth / 2:
            self.playerPosX = tamaWidth / 2
        if self.playerPosX < startScrollingPosX:
            self.player.pos.x = self.playerPosX
        elif self.playerPosX > self.stageWidth - startScrollingPosX:
            self.player.pos.x = self.playerPosX - self.stageWidth + W
        else:
            self.player.pos.x = startScrollingPosX
            self.stagePosX += -self.player.vel.x  # Atenção!!!

        if self.playerPosY < tamaHeight / 2:
            self.playerPosY = tamaHeight
        elif self.playerPosY > 450:
            self.playerPosY = 450
        else:
            self.player.pos.y = startScrollingPosY
            self.stagePosY += -self.player.vel.y
        # if player hits powerup

        # moving bubbles
        cont = 0
        for b in self.bubbles:
            cont += 1
            if b.rect.left > W:
                del (self.bubbles[cont - 1])

        # Die!

        # spawn enemies

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.K_SPACE:
                if self.flag_space == False:
                    self.flag_space = True
                    bubi = Bubble(Kelly.rect.right, Kelly.rect.centery, Kelly.size)
                    all_sprites.add(bubi)
                    self.bubbles.append(bubi)
            if not event.type == pg.K_SPACE:
                if self.flag_space == True:
                    self.flag_space = False


    def draw(self):
        # Game Loop - draw
        rel_y = self.stagePosY % self.bgHeight
        rel_x = self.stagePosX % self.bgWidth
        self.screen.blit(self.bg, (rel_y - self.bgHeight, 0))
        self.screen.blit(self.soil, (rel_y - self.bgHeight, 0))
        if rel_y > H:
            self.screen.blit(self.bg, (rel_y, 0))
        self.screen.blit(self.bg, (rel_x - self.bgWidth, 0))
        self.screen.blit(self.soil, (rel_x - self.bgWidth, 0))
        if rel_x < W:
            self.screen.blit(self.bg, (rel_x, 0))
            self.screen.blit(self.soil, (rel_x, 0))

        # draw turtle and objects:
        self.screen.blit(self.player.image, (self.player.pos.x, self.playerPosY - (tamaHeight / 2)))
        self.all_sprites.draw(self.screen)

        # *after* drawing everything, update the display
        pg.display.update()
        self.screen.fill(BLACK)


g = Game()
while g.running:
    g.new()

pg.quit()
