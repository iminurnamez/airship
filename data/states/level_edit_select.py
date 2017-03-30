import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup


class LevelEditSelect(tools._State):
    def __init__(self):
        super(LevelEditSelect, self).__init__()
        
    def startup(self, persistent):
        self.persist = persistent
        self.make_buttons()

    def get_unlocked_levels(self):
        p = os.path.join("resources", "unlocked.json")
        with open(p, "r") as f:
            return json.load(f)
            
    def make_buttons(self):
        self.buttons = ButtonGroup()
        unlocked_style = {"button_size": (400, 30),
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
            img = pg.transform.scale(prepare.LEVELS["level{}".format(x)], (400, 30))
            r = img.get_rect()
            cover = pg.Surface(r.size).convert_alpha()
            cover.fill((0, 0, 0, 100))
            dull = img.copy()
            dull.blit(cover, (0, 0))
            label = Label("{}".format(x), {"center": r.center},
                                text_color="antiquewhite", font_size=24)
            label.draw(img)
            label.draw(dull)
            Button((left, top), self.buttons, text="{}".format(x),
                       hover_image=img, idle_image=dull,
                       call=self.start_level, args=x, **unlocked_style)
            left += 608
            if left > prepare.SCREEN_RECT.right - 608:
                top += 80
                left = 64
            
    def start_level(self, level_num):
        self.persist["level_num"] = level_num
        self.done = True
        self.next = "LEVELEDITOR"
            
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.buttons.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.buttons.draw(surface)