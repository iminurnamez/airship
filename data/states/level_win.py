import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Blinker


class LevelWinScreen(tools._State):
    def __init__(self): 
        super(LevelWinScreen, self).__init__()
        self.song = prepare.MUSIC["happytune"]

    def unlock_level(self, level_num):
        p = os.path.join("resources", "unlocked.json")
        with open(p, "r") as f:
            unlocked = json.load(f)
        unlocked.append(level_num)
        with open(p, "w") as f:
            json.dump(unlocked, f)

    def startup(self, persistent):
        sr = prepare.SCREEN_RECT
        self.persist = persistent
        self.bg = pg.display.get_surface().copy()
        self.labels = pg.sprite.Group()
        score = self.persist["score"]
        level = self.persist["level"]
        self.player = self.persist["player"]
        self.player.add_score(level.num, score)
        self.player.save()
        Label("Level {} Complete!".format(level.num),
                {"midbottom": sr.center}, self.labels,
                text_color=level.text_color, font_size=24)
        Label("{}/{}".format(score, level.max_score),
                {"midtop": sr.center}, self.labels,
                text_color=level.text_color, font_size=24)
        Blinker("Click to continue", 
                   {"midbottom": (sr.centerx, sr.bottom - 100)},
                   550, self.labels, text_color=level.text_color,
                   font_size=16)
    
    def update(self, dt):
        self.labels.update(dt)
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(self.song)
            pg.mixer.music.play()            
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = "LEVELSELECT"
            pg.mixer.music.fadeout(1000)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            
    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.labels.draw(surface)
        
    