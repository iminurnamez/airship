import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.level import LEVEL_INFO, Level


class LevelSelect(tools._State):
    def __init__(self):
        super(LevelSelect, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.make_buttons()
            
    def make_buttons(self):
        unlocked = self.player.unlocked
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        locked_style = {"button_size": (545, 52),
                                "font_size": 24,
                                "text_color": pg.Color("gray50"),
                                "fill_color": pg.Color("gray10")}
        unlocked_style = {"button_size": (545, 52),
                                   "font_size": 24,
                                   "text_color": pg.Color("gray70"),
                                   "fill_color": pg.Color("gray30"),
                                   "hover_fill_color": pg.Color("gray50"),
                                   "hover_text_color": pg.Color("gray90")}
        p = os.path.join("resources", "levels")
        imgs = os.listdir(p)
        left = 64
        top = 50
        
        for x in range(1, len(prepare.LEVELS) + 1):
            level = Level(x)
            img = pg.Surface((545, 52))
            r = img.get_rect()
            img.fill((143, 143, 143))
            pg.draw.rect(img, (187, 187, 187), r.inflate(-2, -2))
            pg.draw.rect(img, (159, 159, 159), r.inflate(-10, -10))
            cover = pg.Surface(r.size).convert_alpha()
            cover.fill((0, 0, 0, 100))
            if x not in self.player.unlocked:
                pg.draw.rect(img, (100, 100, 100), r.inflate(-12, -12))
                dull = img.copy()
                dull.blit(cover, (0, 0))
                cost = LEVEL_INFO[x]["unlock cost"]
                lock = prepare.GFX["padlock"]
                l_rect = lock.get_rect(midbottom=r.center)
                img.blit(lock, l_rect)
                dull.blit(lock, l_rect)
                label = Label("{:,} to unlock".format(cost),
                                    {"midtop": r.center},
                                    text_color="antiquewhite", font_size=16)
                label.draw(img)
                label.draw(dull)
            else:
                pg.draw.rect(img, LEVEL_INFO[x]["sky"], r.inflate(-12, -12))
                img.blit(pg.transform.scale(prepare.LEVELS["level{}".format(x)], (533, 40)), (6, 6))
                dull = img.copy()
                dull.blit(cover, (0, 0))
                label = Label("{}".format(x), {"midbottom": (r.centerx, r.centery + 8)},
                                text_color="antiquewhite", font_size=24)
                try:
                    player_score = self.player.high_scores["{}".format(x)]
                except KeyError:
                    player_score = 0
                score_label = Label("{}/{}".format(player_score, level.max_score),
                                             {"midtop": (r.centerx, r.centery - 2)}, text_color="antiquewhite", font_size=16)
                label.draw(img)
                label.draw(dull)
                score_label.draw(img)
                score_label.draw(dull)
            Button((left, top), self.buttons,
                       hover_image=img, idle_image=dull,
                       call=self.start_level, args=x, **unlocked_style)
            left += 608
            if left > prepare.SCREEN_RECT.right - 608:
                top += 80
                left = 64
        self.player_points_label = Label(
                "{:,}".format(self.player.points),
                {"midtop": prepare.SCREEN_RECT.midtop}, self.labels,
                text_color="antiquewhite", font_size=24)                
        
    def start_level(self, level_num):
        if level_num in self.player.unlocked:
            self.persist["level_num"] = level_num
            self.done = True
            self.next = "GAMEPLAY"
            pg.mixer.music.fadeout(1000)
        else:
            cost = LEVEL_INFO[level_num]["unlock cost"]
            if self.player.points >= cost:
                prepare.SFX["unlock"].play()
                self.player.points -= cost
                self.player.unlocked.append(level_num)
                self.player.save()
                self.persist["level_num"] = level_num
                self.done = True
                self.next = "GAMEPLAY"
                pg.mixer.music.fadeout(1000)
            else:
                prepare.SFX["negative"].play()
                
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.buttons.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.player_points_label.set_text("{:,}".format(self.player.points))
        
    def draw(self, surface):
        surface.fill(pg.Color("gray10"))
        self.buttons.draw(surface)
        self.labels.draw(surface)