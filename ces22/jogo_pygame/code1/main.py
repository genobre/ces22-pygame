# "This Game Is Over" - Joseph Pueyo http://www.josephpueyo.com/
# wind by Please credit Lanea Zimmerman

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from pygame.locals import *


class MainMenuAnimation:
    def __init__(self, filename="Tela_inicial.png", cols=4, rows=3):
        self.sheet = pg.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([(0, 0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h), (-hw, -h), (-w, -h), ])

    def draw_screen(self, surface, cellIndex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])


class Button:
    # Creates the buttons to start the game, go to section 'How to Play' and to close this section
    def __init__(self, filename, cols, rows):
        self.sheet = pg.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([(0, 0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h), (-hw, -h), (-w, -h), ])

    def draw_button(self, surface, cellIndex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])


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
        self.font_name = pg.font.match_font('Alpha Beta BRK')
        self.bgWidth, self.bgHeight = self.bg.get_rect().size
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        # load highscore
        with open(path.join(self.dir, "highscore.txt"), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.tamasprite = Spritesheet(path.join(img_dir, "tama.png"))
        self.tamashieldsprite = Spritesheet(path.join(img_dir, "tamashield.png"))
        self.plasticsprite = Spritesheet(path.join(img_dir, "plastic_bag.png"))
        self.krillsprite = Spritesheet(path.join(img_dir, "shrimp.png"))
        self.bubblesprite = Spritesheet(path.join(img_dir, "bubble.png"))
        self.jellysprite = Spritesheet(path.join(img_dir, "jelly_fish.png"))
        self.cansprite = Spritesheet(path.join(img_dir, "can.png"))
        self.crabsprite = Spritesheet(path.join(img_dir, "crab.png"))
        self.fishsprite = Spritesheet(path.join(img_dir, "lower_fish.png"))
        self.headsprite = Spritesheet(path.join(img_dir, "bigbosshead.png"))
        self.headhitsprite = Spritesheet(path.join(img_dir, "bigbossheadhit.png"))
        self.tentaclesprite = Spritesheet(path.join(img_dir, "tentacles.png"))
        self.inksprite = Spritesheet(path.join(img_dir, "ink.png"))
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.bubble_sound = pg.mixer.Sound(path.join(self.snd_dir, 'pop.ogg'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'powerup.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hit.wav'))
        self.killed_sound = pg.mixer.Sound(path.join(self.snd_dir, 'killed.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.bubbles = pg.sprite.Group()
        self.plasticbag = pg.sprite.Group()
        self.jellyfish = pg.sprite.Group()
        self.krills = pg.sprite.Group()
        self.cans = pg.sprite.Group()
        self.crabs = pg.sprite.Group()
        self.inks = pg.sprite.Group()
        self.fishes = pg.sprite.Group()
        self.tentacles = pg.sprite.Group()
        self.heads = pg.sprite.Group()
        self.player = Player(self)
        self.plastic_timer = 0
        self.krill_timer = 0
        self.jelly_timer = 0
        self.can_timer = 0
        self.crab_timer = 0
        self.fish_timer = 0
        self.ink_timer = 0
        self.powerjelly_timer = 0
        self.flag_space = False
        self.playerPosX = 16
        self.playerPosY = HH
        self.stageWidth = self.bgWidth
        self.stagePosX = 0
        self.stageHeight = self.bgHeight
        self.stagePosY = 0
        self.metboss = False
        self.win = False
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        pg.mixer.music.set_volume(0.4)
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.player.keys()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # Spawn enemies and food:
        now = pg.time.get_ticks()
        if now - self.plastic_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.plastic_timer = now
            PlasticBag(self)

        if now - self.jelly_timer > 4000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.jelly_timer = now
            JellyFish(self)

        if now - self.can_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.can_timer = now
            Can(self)

        if now - self.crab_timer > 2500 + random.choice([-1000, -500, 0, 500, 1000]):
            self.crab_timer = now
            Crab(self)

        if now - self.fish_timer > 3500 + random.choice([-1000, -500, 0, 500, 1000]):
            self.fish_timer = now
            Fish(self)

        if now - self.krill_timer > 2000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.krill_timer = now
            Krill(self)

        if (now - self.ink_timer > 2000 + random.choice([-1000, -500, 0, 500, 1000])) and self.metboss == True:
            self.ink_timer = now
            BossInk(self)

        ## Check for collisions with bubbles:
        krill_cls = pg.sprite.groupcollide(self.bubbles, self.krills, False, False)
        if krill_cls:
            krill_shot = pg.sprite.groupcollide(self.bubbles, self.krills, True, True, pg.sprite.collide_mask)
            if krill_shot:
                self.score += 5
                self.hit_sound.play()

        crab_cls = pg.sprite.groupcollide(self.bubbles, self.crabs, False, False)
        if crab_cls:
            crab_shot = pg.sprite.groupcollide(self.bubbles, self.crabs, True, True, pg.sprite.collide_mask)
            if crab_shot:
                self.score += 10
                self.hit_sound.play()

        jelly_cls = pg.sprite.groupcollide(self.bubbles, self.jellyfish, False, False)
        if jelly_cls:
            jelly_shot = pg.sprite.groupcollide(self.bubbles, self.jellyfish, True, True, pg.sprite.collide_mask)
            if jelly_shot:
                self.score += 20
                self.hit_sound.play()

        plastic_cls = pg.sprite.groupcollide(self.bubbles, self.plasticbag, False, False)
        if plastic_cls:
            plastic_shot = pg.sprite.groupcollide(self.plasticbag, self.bubbles, False, True, pg.sprite.collide_mask)
            for bag in plastic_shot:
                if self.player.atejelly:
                    bag.kill()
                    self.score += 50
                else:
                    bag.got_shot = True
                self.hit_sound.play()

        can_cls = pg.sprite.groupcollide(self.bubbles, self.cans, False, False)
        if can_cls:
            can_shot = pg.sprite.groupcollide(self.cans, self.bubbles, False, True, pg.sprite.collide_mask)
            for canhit in can_shot:
                if self.player.atejelly:
                    canhit.kill()
                    self.score += 30
                else:
                    canhit.got_shot = True
                self.hit_sound.play()

        fish_cls = pg.sprite.groupcollide(self.bubbles, self.fishes, False, False)
        if fish_cls:
            fish_shot = pg.sprite.groupcollide(self.fishes, self.bubbles, False, True, pg.sprite.collide_mask)
            for fishhit in fish_shot:
                if self.player.atejelly:
                    fishhit.kill()
                    self.score += 50
                else:
                    if fishhit.life == 1:
                        self.score += 100
                    fishhit.got_shot = True
                self.hit_sound.play()

        tentacle_cls = pg.sprite.groupcollide(self.bubbles, self.tentacles, False, False)
        if tentacle_cls:
            t = pg.sprite.groupcollide(self.tentacles, self.bubbles, False, True, pg.sprite.collide_mask)
            if t:
                self.hit_sound.play()

        ink_cls = pg.sprite.groupcollide(self.bubbles, self.inks, False, False)
        if ink_cls:
            i=pg.sprite.groupcollide(self.inks, self.bubbles, True, True, pg.sprite.collide_mask)
            if i:
                self.hit_sound.play()

        head_cls = pg.sprite.groupcollide(self.bubbles, self.heads, False, False)
        if head_cls:
            head_shot = pg.sprite.groupcollide(self.heads, self.bubbles, False, True, pg.sprite.collide_mask)
            for h in head_shot:
                if self.player.atejelly:
                    self.score += 5
                    h.got_shot = True
                    h.life -= 1
                else:
                    h.got_shot = True
                    h.life -= 0.5
                if h.life <= 1:
                    self.win = True
                self.hit_sound.play()

        ## Check for collisions of enemies with turtle:
        plastic_hits = pg.sprite.spritecollide(self.player, self.plasticbag,True, pg.sprite.collide_mask)
        if plastic_hits:
            if self.player.shield:
                self.player.shield = False
            else:
                self.playing = False
            self.killed_sound.play()

        can_close = pg.sprite.spritecollide(self.player, self.cans, False)
        if can_close:
            can_hit = pg.sprite.spritecollide(self.player, self.cans, True, pg.sprite.collide_mask)
            if can_hit:
                if self.player.shield:
                    self.player.shield = False
                else:
                    self.playing = False
                self.killed_sound.play()

        fish_close = pg.sprite.spritecollide(self.player, self.fishes, False)
        if fish_close:
            fish_hit = pg.sprite.spritecollide(self.player, self.fishes, True, pg.sprite.collide_mask)
            if fish_hit:
                if self.player.shield:
                    self.player.shield = False
                else:
                    self.playing = False
                self.killed_sound.play()

        ink_close = pg.sprite.spritecollide(self.player, self.inks, False)
        if ink_close:
            ink_hit = pg.sprite.spritecollide(self.player, self.inks, True, pg.sprite.collide_mask)
            if ink_hit:
                if self.player.shield:
                    self.player.shield = False
                else:
                    self.playing = False
                self.killed_sound.play()

        tentacle_close = pg.sprite.spritecollide(self.player, self.tentacles, False)
        if tentacle_close:
            tentacle_hit = pg.sprite.spritecollide(self.player, self.tentacles, False, pg.sprite.collide_mask)
            if tentacle_hit:
                if self.player.shield:
                    self.player.shield = False
                else:
                    self.playing = False
                self.killed_sound.play()

        head_close = pg.sprite.spritecollide(self.player, self.heads, False)
        if head_close:
            head_hit = pg.sprite.spritecollide(self.player, self.heads, False, pg.sprite.collide_mask)
            if head_hit:
                if self.player.shield:
                    self.player.shield = False
                else:
                    self.playing = False
                self.killed_sound.play()

        ## Check for collisions of food with turtle:
        krill_close = pg.sprite.spritecollide(self.player, self.krills, False)
        if krill_close:
            krill_hits = pg.sprite.spritecollide(self.player, self.krills, True, pg.sprite.collide_mask)
            if krill_hits:
                self.score += 10
                self.boost_sound.play()

        crab_close = pg.sprite.spritecollide(self.player, self.crabs, False)
        if crab_close:
            crab_hits = pg.sprite.spritecollide(self.player, self.crabs, True, pg.sprite.collide_mask)
            if crab_hits:
                self.player.shield = True
                self.boost_sound.play()

        jelly_close = pg.sprite.spritecollide(self.player, self.jellyfish, False)
        if jelly_close:
            jelly_hits = pg.sprite.spritecollide(self.player, self.jellyfish, True, pg.sprite.collide_mask)
            if jelly_hits:
                self.player.atejelly = True
                self.powerjelly_timer = now
                self.boost_sound.play()

        #checks if you exceeded powerup time:
        if now - self.powerjelly_timer > 5000:
            self.player.atejelly = False

        if (self.playerPosX > self.stageWidth - startScrollingPosX) and self.metboss == False:
            self.metboss = True
            BossHead(self)
            BossTentacles(self)

        ## check
        self.playerPosX += self.player.xVelocity
        self.playerPosY += self.player.yVelocity

        if self.playerPosX > self.stageWidth - (tamaWidth/2):
            self.playerPosX = self.stageWidth - (tamaWidth/2)
        if self.playerPosX < (tamaWidth/2):
            self.playerPosX = (tamaWidth/2)
        if self.playerPosX < startScrollingPosX:
            self.player.rect.centerx = self.playerPosX
        elif self.playerPosX > self.stageWidth - startScrollingPosX:
            self.player.rect.centerx = self.playerPosX - self.stageWidth + W
        else:
            self.player.rect.centerx = startScrollingPosX
            self.stagePosX += -self.player.xVelocity

        if self.playerPosY < (tamaHeight/2):
            self.playerPosY = tamaHeight
        elif self.playerPosY > 450:
            self.playerPosY = 450
        else:
            self.player.rect.centery = startScrollingPosY
            self.stagePosY += -self.player.yVelocity

        self.player.rect.right = self.player.rect.centerx
        self.player.rect.bottom = self.playerPosY

        #check if space bar is pressed
        if self.flag_space:
            if self.player.swim_l:
                self.bubble_sound.play()
                Bubble(self, self.player.rect.centerx - tamaWidth + 10, self.playerPosY - tamaHeight/2 - 4, self.player.swim_l, self.player.atejelly)
            else:
                self.bubble_sound.play()
                Bubble(self, self.player.rect.centerx + tamaWidth/2 + 2, self.playerPosY - tamaHeight / 2 - 4, self.player.swim_l, self.player.atejelly)
            if not self.player.atejelly:
                self.flag_space = False

        if self.win:
            self.playing = False

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
                if self.flag_space:
                   self.flag_space = False

    def draw(self):
        # Game Loop - draw
        rel_y = self.stagePosY % self.bgHeight
        rel_x = self.stagePosX % self.bgWidth
        self.screen.blit(self.bg, (rel_y - self.bgHeight, 0))
        if rel_y > H:
            self.screen.blit(self.bg, (rel_y, 0))
        self.screen.blit(self.bg, (rel_x - self.bgWidth, 0))
        if rel_x < W:
            self.screen.blit(self.bg, (rel_x, 0))

        # draw turtle and objects:
        self.all_sprites.draw(self.screen)

        #show score:
        self.draw_text(str(self.score), 22, WHITE, W / 2, 15)

        # *after* drawing everything, update the display
        pg.display.update()
        self.screen.fill(BLACK)

    def cliques(self):
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()

    def introduction(self):
        intro = True
        index = 0
        global s
        pg.mixer.music.load(path.join(self.snd_dir, 'wind.ogg'))
        pg.mixer.music.play(loops=-1)
        s = MainMenuAnimation("Tela_inicial.png", 4, 3)
        while intro:
            self.cliques()
            s.draw_screen(self.screen, index % s.totalCellCount, HW, HH, 4)
            if index <= 9:
                index += 1
                self.clock.tick(4)

            start_but = Button("start_button.png", 2, 1)
            howto_but = Button("howto_button.png", 2, 1)
            exit_but = Button("exit_button.png", 2, 1)
            click = pg.mouse.get_pressed()
            mouse = pg.mouse.get_pos()
            x = HW - 200
            y = HH + 100
            if index == 10:
                if 280 > mouse[0] > 120 and 360 > mouse[1] > 300:
                    start_but.draw_button(self.screen, 1 % s.totalCellCount, x, y, 4)
                    if click[0] == 1:
                        intro = False
                else:
                    start_but.draw_button(self.screen, 0 % s.totalCellCount, x, y, 4)
                if 480 > mouse[0] > 320 and 360 > mouse[1] > 300:
                    howto_but.draw_button(self.screen, 1 % s.totalCellCount, 200 + x, y, 4)
                    if click[0] == 1:
                        index = 11
                else:
                    howto_but.draw_button(self.screen, 0 % s.totalCellCount, 200 + x, y, 4)
            if index == 11:
                if 777 > mouse[0] > 752 and 43 > mouse[1] > 18:
                    exit_but.draw_button(self.screen, 1 % s.totalCellCount, 764, 31, 4)
                    if click[0] == 1:
                        index = 10
                else:
                    exit_but.draw_button(self.screen, 0 % s.totalCellCount, 764, 31, 4)
            pg.display.update()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        if self.win:
            self.show_victory_screen()
        else:
            pg.mixer.music.load(path.join(self.snd_dir, 'ThisGameIsOver.ogg'))
            pg.mixer.music.play(loops=-1)
            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", 48, WHITE, W / 2, H / 4)
            self.draw_text("Score: " + str(self.score), 22, WHITE, W/ 2, H / 2)
            self.draw_text("Click to play again", 22, WHITE, W / 2, H * 3 / 4)
            if self.score > self.highscore:
                self.highscore = self.score
                self.draw_text("NEW HIGH SCORE!", 22, WHITE, W/ 2, H / 2 + 40)
                with open(path.join(self.dir, "highscore.txt"), 'w') as f:
                    f.write(str(self.score))
            else:
                self.draw_text("High Score: " + str(self.highscore), 22, WHITE, W/ 2, H / 2 + 40)
            pg.display.flip()
            self.wait_for_key()
            self.playing = False
            pg.mixer.music.fadeout(500)

    def show_victory_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text("YOU WON!", 48, WHITE, W / 2, H / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, W/ 2, H / 2)
        self.draw_text("Click to play again", 22, WHITE, W / 2, H * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, W/ 2, H / 2 + 40)
            with open(path.join(self.dir, "highscore.txt"), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, W/ 2, H / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        self.playing = False
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                click = pg.mouse.get_pressed()
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if click[0] == 1:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.introduction()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
