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
        self.jellysprite = Spritesheet(path.join(img_dir, "jelly_fish.png"))
        self.cansprite = Spritesheet(path.join(img_dir, "can.png"))
        self.crabsprite = Spritesheet(path.join(img_dir, "crab.png"))
        self.fishsprite = Spritesheet(path.join(img_dir, "lower_fish.png"))
        # load sounds

    def new(self):
        # start a new game
        # self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.bubbles = pg.sprite.Group()
        self.plasticbag = pg.sprite.Group()
        self.jellyfish = pg.sprite.Group()
        self.krills = pg.sprite.Group()
        self.cans = pg.sprite.Group()
        self.crabs = pg.sprite.Group()
        self.fishes = pg.sprite.Group()
        self.player = Player(self)
        self.plastic_timer = 0
        self.krill_timer = 0
        self.jelly_timer = 0
        self.can_timer = 0
        self.crab_timer = 0
        self.fish_timer = 0
        self.flag_space = False
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        print(self.playing)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.player.keys()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # Spawn enemies and food:
        now = pg.time.get_ticks()
        if now - self.plastic_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.plastic_timer = now
            PlasticBag(self)

        if now - self.jelly_timer > 4000:
            self.jelly_timer = now
            JellyFish(self)

        if now - self.can_timer > 5000:
            self.can_timer = now
            Can(self)

        if now - self.crab_timer > 2500:
            self.crab_timer = now
            Crab(self)

        if now - self.fish_timer > 3500:
            self.fish_timer = now
            Fish(self)

        if now - self.krill_timer > 2000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.krill_timer = now
            Krill(self)

        ## Check for collisions with bubbles:
        krill_close = pg.sprite.groupcollide(self.bubbles, self.krills, False, False)
        if krill_close:
            krill_shot = pg.sprite.groupcollide(self.bubbles, self.krills, True, True, pg.sprite.collide_mask)
            if krill_shot:
                print("MATOU SUA COMIDA")

        crab_close = pg.sprite.groupcollide(self.bubbles, self.crabs, False, False)
        if crab_close:
            crab_shot = pg.sprite.groupcollide(self.bubbles, self.crabs, True, True, pg.sprite.collide_mask)
            if crab_shot:
                print("MATOU SUA COMIDA")

        jelly_close = pg.sprite.groupcollide(self.bubbles, self.jellyfish, False, False)
        if jelly_close:
            jelly_shot = pg.sprite.groupcollide(self.bubbles, self.jellyfish, True, True, pg.sprite.collide_mask)
            if jelly_shot:
                print("MATOU SUA COMIDA")

        plastic_close = pg.sprite.groupcollide(self.bubbles, self.plasticbag, False, False)
        if plastic_close:
            plastic_shot = pg.sprite.groupcollide(self.plasticbag, self.bubbles, False, True, pg.sprite.collide_mask)
            for bag in plastic_shot:
                bag.got_shot = True

        can_close = pg.sprite.groupcollide(self.bubbles, self.cans, False, False)
        if can_close:
            can_shot = pg.sprite.groupcollide(self.cans, self.bubbles, False, True, pg.sprite.collide_mask)
            for canhit in can_shot:
                canhit.got_shot = True

        fish_close = pg.sprite.groupcollide(self.bubbles, self.fishes, False, False)
        if fish_close:
            fish_shot = pg.sprite.groupcollide(self.fishes, self.bubbles, False, True, pg.sprite.collide_mask)
            for fishhit in fish_shot:
                fishhit.got_shot = True

        ## Check for collisions of enemies with turtle:
        plastic_close = pg.sprite.spritecollide(self.player, self.plasticbag, False, False)
        if plastic_close:
            plastic_hits = pg.sprite.spritecollide(self.player, self.plasticbag, False, pg.sprite.collide_mask)
            if plastic_hits:
                self.playing = False
                self.running = False
        can_close = pg.sprite.spritecollide(self.player, self.cans, False)
        if can_close:
            can_hit = pg.sprite.spritecollide(self.player, self.cans, False, pg.sprite.collide_mask)
            if can_hit:
                self.playing = False
                self.running = False
        fish_close = pg.sprite.spritecollide(self.player, self.fishes, False)
        if fish_close:
            fish_hit = pg.sprite.spritecollide(self.player, self.fishes, False, pg.sprite.collide_mask)
            if fish_hit:
                self.playing = False
                self.running = False

        ## Check for collisions of food with turtle:
        krill_close = pg.sprite.spritecollide(self.player, self.krills, False)
        if krill_close:
            krill_hits = pg.sprite.spritecollide(self.player, self.krills, True, pg.sprite.collide_mask)
            if krill_hits:
                print("somar ponto")

        crab_close = pg.sprite.spritecollide(self.player, self.crabs, False)
        if crab_close:
            crab_hits = pg.sprite.spritecollide(self.player, self.crabs, True, pg.sprite.collide_mask)
            if crab_hits:
                print("you got a shield!")

        jelly_close = pg.sprite.spritecollide(self.player, self.jellyfish, False)
        if jelly_close:
            jelly_hits = pg.sprite.spritecollide(self.player, self.jellyfish, True, pg.sprite.collide_mask)
            if jelly_hits:
                print("Now you shoot 3 bubbles at time!")

        ## check
        self.playerPosX += self.player.xVelocity
        self.playerPosY += self.player.yVelocity
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
            self.stagePosX += -self.player.xVelocity

        if self.playerPosY < tamaHeight / 2:
            self.playerPosY = tamaHeight
        elif self.playerPosY > 450:
            self.playerPosY = 450
        else:
            self.player.pos.y = startScrollingPosY
            self.stagePosY += -self.player.yVelocity

        self.player.rect.right = self.player.pos.x
        self.player.rect.bottom = self.playerPosY
        # if player hits powerup

        if self.flag_space:
            if self.player.swim_l:
                Bubble(self, self.player.pos.x - tamaWidth - 15, self.playerPosY - tamaHeight/2 - 4, self.player.swim_l)
            else:
                Bubble(self, self.player.pos.x, self.playerPosY - tamaHeight / 2 - 4, self.player.swim_l)
            self.flag_space = False

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.flag_space == False:
                        self.flag_space = True
            if not event.type == pg.KEYDOWN:
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
        self.all_sprites.draw(self.screen)

        # *after* drawing everything, update the display
        pg.display.update()
        self.screen.fill(BLACK)


g = Game()
while g.running:
    g.new()

pg.quit()
