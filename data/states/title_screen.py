import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Blinker, MultiLineLabel
from ..components.player import Player
from ..components.banner import Banner
from ..components.airship import Airship


class DummyShip(Airship):
    def __init__(self, pos, speed):
        super(DummyShip, self).__init__()
        self.pos = pos
        self.speed = speed

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.prop_time:
            self.timer -= self.prop_time
            self.prop_image =  next(self.prop_images)
        self.pos = self.pos[0] + (self.speed * dt), self.pos[1]
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.prop_image, (self.rect.left + 2, self.rect.top + 26))


class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.player = self.load_player()
        self.banner = Banner((-870, 256), "Indefatidirigible", 96, (17, 141, 166), "antiquewhite")
        self.airship = DummyShip((-20, 316), self.banner.speed)
        self.start_label = Blinker("Click to Start",
                                          {"midbottom": prepare.SCREEN_RECT.center},
                                          500, font_size=32)
        self.start_label.active = False

    def load_player(self):
        p = os.path.join("resources", "player.json")
        if not os.path.isfile(p):
            with open(p, "w") as f:
                info = {
                        "unlocked": [1],
                        "points": 0,
                        "high scores": {}}

                json.dump(info, f)
        with open(p, "r") as f:
            try:
                info = json.load(f)
            except:
                with open(p, "w") as f:
                    info = {
                            "unlocked": [1],
                            "points": 0,
                            "high scores": {}}

                    json.dump(info, f)
        self.persist["player"] = Player(info)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif event.key == pg.K_e:
                self.done = True
                self.next = "LEVELEDITSELECT"
            elif event.key == pg.K_h:
                self.done = True
                self.next = "HELPSCREEN"
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = "LEVELSELECT"

    def update(self, dt):
        self.banner.update(dt)
        self.airship.update(dt)
        self.start_label.update(dt)
        if self.airship.pos[0] > prepare.SCREEN_RECT.centerx + 300:
            self.start_label.active = True
        self.get_line_points(self.banner)

    def get_line_points(self, banner):
        front_strip = banner.strips[0]
        self.top_line = [(self.airship.rect.left + 56, self.airship.rect.top + 28), front_strip.rect.topright]
        self.bottom_line = [(self.airship.rect.left + 56, self.airship.rect.top + 52), front_strip.rect.bottomright]

    def draw(self, surface):
        surface.fill(pg.Color(144, 215, 236))
        if self.start_label.active:
            self.start_label.draw(surface)
        pg.draw.line(surface, pg.Color("gray90"), *self.top_line)
        pg.draw.line(surface, pg.Color("gray90"), *self.bottom_line)
        self.banner.draw(surface)
        self.airship.draw(surface)