import os
from itertools import cycle
import json

import pygame as pg

from .. import tools, prepare
from ..components.level import Level, Jewel


class LevelEditor(tools._State):
    def __init__(self):
        super(LevelEditor, self).__init__()
        self.scroll_keys = {
            pg.K_a: (-4, 0),        
            pg.K_d: (4, 0)}
        self.colors = cycle(["Yellow", "Green", "Red", "Blue", "Pink", "Grey"])
        self.current_color = next(self.colors)
        
    def startup(self, persistent):
        self.persist = persistent
        self.level_num = self.persist["level_num"]
        self.level = Level(self.level_num)
        self.view_rect = prepare.SCREEN_RECT.copy()
        self.jewels = [x for x in self.level.jewels]


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.done  = True
                self.next = "LEVELEDITSELECT"
            elif event.key == pg.K_s:
                self.save()
            elif event.key == pg.K_UP:
                self.current_color = next(self.colors)
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                pos = event.pos[0] + self.view_rect.left, event.pos[1] + self.view_rect.top
                jewel = Jewel(pos, self.current_color)
                self.jewels.append(jewel)
            elif event.button == 3:
                for j in self.jewels:
                    pos = (event.pos[0] + self.view_rect.left,
                               event.pos[1] + self.view_rect.top)
                    if j.rect.collidepoint(pos):
                        self.jewels.remove(j)
                        break

    def save(self):
        info = [(j.rect.center, j.color) for j in self.jewels]
        fname = "jewels-level{}.json".format(self.level.num)
        p = os.path.join("resources", "jewels", fname)
        with open(p, "w") as f:
            json.dump(info, f)
        
    def update(self, dt):
        keys = pg.key.get_pressed()
        for k in self.scroll_keys:
            if keys[k]:
                self.view_rect.move_ip(self.scroll_keys[k])
                if self.view_rect.left < 0:
                    self.view_rect.left = 0
                elif self.view_rect.right > self.level.rect.w:
                    self.view_rect.right = self.level.rect.w
                    
    def draw(self, surface):
        surface.fill(self.level.sky_color)
        surface.blit(self.level.image.subsurface(self.view_rect), (0, 0))
        for j in self.jewels:
            surface.blit(j.image, j.rect.move(-self.view_rect.left, -self.view_rect.top))