import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Blinker
from ..components.airship import Airship
from ..components.level import Level


class Gameplay(tools._State):
    def __init__(self):
        super(Gameplay, self).__init__()
        
    def startup(self, persistent):
        pg.event.get()
        self.persist = persistent
        self.player = self.persist["player"]
        self.level = Level(self.persist["level_num"])
        self.score = 0
        self.offset = 0
        self.bonus = 1
        pg.mixer.music.load(self.level.song)
        pg.mixer.music.set_volume(self.level.music_volume)
        self.labels = pg.sprite.Group()
        self.score_label = Label(
                "{}".format(self.score),
                {"midtop": (prepare.SCREEN_RECT.midtop)},
                self.labels, font_size=32, text_color=self.level.text_color)
        self.bonus_label = Label("x{} Bonus".format(self.bonus), 
                                            {"midtop": (prepare.SCREEN_RECT.centerx, 48)},
                                            text_color=self.level.text_color, font_size=16)
        self.level_label = Label("Level {}".format(self.level.num), 
                                         {"midbottom": (prepare.SCREEN_RECT.centerx, prepare.SCREEN_RECT.centery - 64)},
                                         self.labels, text_color=self.level.text_color, font_size=64)
        self.start_label = Blinker(
                "Click to start level",
                {"midtop": prepare.SCREEN_RECT.center},
                550, self.labels, text_color=self.level.text_color, font_size=32)
        high_score = 0
        if str(self.level.num) in self.player.high_scores:
            high_score = self.player.high_scores[str(self.level.num)]
        self.goal_label = Label("{:,}/{:,} points".format(high_score, self.level.max_score),
                                         {"midbottom": (prepare.SCREEN_RECT.center)},
                                         self.labels, text_color=self.level.text_color, font_size=32)
        self.msg = None
        self.current_jewel = self.level.jewel_goals.pop()
        
        self.airship = Airship()
        self.started = False
        
    def start(self):
        self.started = True
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif not self.started and event.type == pg.MOUSEBUTTONUP:
            self.start_label.kill()
            self.goal_label.kill()
            self.level_label.kill()
            pg.mixer.music.play()
            self.start()
            
    def update(self, dt):
        if dt > 100:
            return
        if not self.started:
            self.labels.update(dt)
            return
        self.level.update(dt, self.airship)
        dx = self.airship.update(dt)
        self.offset += dx
        if self.airship.dead:
            self.done = True
            self.level.cleanup()
            self.next = "LEVELFAIL"
            self.persist["level"] = self.level
            self.persist["text"] = self.msg
        elif not self.airship.exploded:
            if self.airship.screen_rect.left >= prepare.SCREEN_RECT.right:
                self.done = True
                self.next = "LEVELWIN"
                self.persist["level"] = self.level
                pg.mixer.music.fadeout(prepare.FADE_TIME)
                self.persist["score"] = self.score
            if self.offset >= self.level.rect.w - prepare.SCREEN_RECT.w:
                self.offset = self.level.rect.w - prepare.SCREEN_RECT.w
                self.airship.screen_rect.left = self.airship.rect.left - self.offset
            if (pg.sprite.collide_mask(self.airship, self.level)
                        or self.airship.rect.top > prepare.SCREEN_RECT.bottom):
                self.airship.explode()
                self.msg = "You crashed"
                pg.mixer.music.fadeout(prepare.FADE_TIME)
            if self.airship.rect.bottom < 0:
                self.airship.explode()
                self.msg = "You flew too high"
                pg.mixer.music.fadeout(prepare.FADE_TIME)
            if self.current_jewel.rect.right < self.airship.rect.left:
                try:
                    self.current_jewel = self.level.jewel_goals.pop()
                    self.bonus = 1
                except IndexError:
                    pass
            for jewel in self.level.jewels:
                if pg.sprite.collide_mask(self.airship, jewel):
                    self.score += jewel.points * self.bonus
                    self.bonus += 1
                    try:
                        self.current_jewel = self.level.jewel_goals.pop()
                    except IndexError:
                        pass
                    jewel.sound.play()
                    jewel.kill()
        self.score_label.set_text("{:,}".format(self.score))
        self.bonus_label.set_text("x{} Bonus".format(self.bonus))
        
    def draw(self, surface):
        surface.fill(self.level.sky_color)
        surface.blit(self.level.image.subsurface((int(self.offset), 0, prepare.SCREEN_SIZE[0], prepare.SCREEN_SIZE[1])), (0, 0))
        for jewel in self.level.jewels:
            surface.blit(jewel.image, jewel.rect.move((-self.offset, 0)))
        for waterfall in self.level.waterfalls:
            waterfall.draw(surface, int(-self.offset))
        self.airship.draw(surface)
        self.labels.draw(surface)
        if self.bonus > 1:
            self.bonus_label.draw(surface)