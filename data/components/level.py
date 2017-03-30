import os
from itertools import cycle
import json


import pygame as pg

from .. import tools, prepare
from ..components.sound_source import SoundSource


JEWEL_POINTS = {
        "Yellow": 1,
        "Green": 2,
        "Red": 5,
        "Pink": 10,
        "Blue": 25,
        "Grey": 100}

LEVEL_INFO = {
        1: {"sky": (162, 215, 255),
             "unlock cost": 0,
              "song": "mirage",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (177, 127, 33)},
        2: {"sky": (162, 215, 255),
              "unlock cost": 2000,
              "song": "mirage",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (177, 127, 33)},
        3: {"sky": (25, 23, 22),
              "unlock cost": 5000,
              "song": "coolbeat1",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (247, 247, 247)},
        4: {"sky": (206, 230, 207),
              "unlock cost": 9000,
              "song": "forest",
              "music volume": 1.,
              "waterfalls": [pg.Rect(3249, 687, 627, 24)],
              "text color": (196, 69, 91)},
        5: {"sky": (206, 230, 207),
             "unlock cost": 14000,
              "song": "forest",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (196, 69, 91)},
        6: {"sky": (206, 230, 207),
              "unlock cost": 20000,
              "song": "happytune",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (247, 247, 247)},
        7: {"sky": (144, 215, 236),
              "unlock cost": 27000,
              "song": "adventure",
              "music volume": .5,
              "waterfalls": [],
              "text color": (17, 141, 166)},
        8: {"sky": (157, 208, 230),
              "unlock cost": 35000,
              "song": "calm",
              "music volume": 1.,
              "waterfalls": [],
              "text color": (76, 47, 24)},
        9: {"sky": (189, 203, 234),
              "unlock cost": 44000,
              "song": "chill",
              "music volume": 1.,
              "text color": (61, 104, 127),
              "waterfalls": [pg.Rect(3186, 687, 322, 24)]}
}


class Jewel(pg.sprite.Sprite):
    sounds = {
        "Yellow": "upshort",
        "Green": "upshort",
        "Red": "upshort",
        "Pink": "upmid",
        "Blue": "upmid",
        "Grey": "uplong"}

    def __init__(self, pos, color, *groups):
        super(Jewel, self).__init__(*groups)
        self.color = color
        self.images = cycle(tools.strip_from_sheet(
                prepare.GFX["jewel-{}".format(color.lower())],
                (0, 0), (32, 32), 8, 1))
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=pos)
        self.spin_time = 100
        self.timer = 0
        self.points = JEWEL_POINTS[color]
        self.sound = prepare.SFX[self.sounds[color]]

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.spin_time:
            self.timer -= self.spin_time
            self.image =next(self.images)

class WaterfallRow(object):
    def __init__(self, img_num, topleft, waterfall_rect, speed):
        img = prepare.GFX["bubble"]
        self.rect = pg.Rect(topleft, (waterfall_rect.width, img.get_width()))
        self.image = pg.Surface(self.rect.size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        if img_num == 0:
            start = 0
        else:
            start = -(img.get_width() // 2)
        for x in range(start, self.rect.w + img.get_width(), img.get_width()):
            self.image.blit(img, (x, 0))
        self.top = self.rect.top
        self.waterfall_rect = waterfall_rect
        self.speed = speed
        

    def update(self, dt):
        flip = False
        self.top += self.speed * dt
        if self.top > self.waterfall_rect.bottom:
            self.top = self.waterfall_rect.top
            flip = True
        self.rect.top = self.top
        return flip

class Waterfall(object):
    def __init__(self, rect):
        self.rect = rect
        self.rows = []
        self.speed = .02
        top = self.rect.top
        for x in range(1, 5):
            topleft = (self.rect.left, top)
            row = WaterfallRow(x%2, topleft, self.rect, self.speed)
            self.rows.append(row)
            top += 6
        self.sound_source = SoundSource(prepare.SFX["waterfall"],
                                                          self.rect.center, .4, 2500)
        
    def update(self, dt, airship):
        flip = False
        for row in self.rows:
            if row.update(dt):
                flip = True
        if flip:
            self.flip()
        self.sound_source.update(airship)
            

    def flip(self):
        left = [self.rows[-1]]
        right = self.rows[0:-1]
        self.rows = left + right

    def draw(self, surface, x_offset):
        for row in self.rows:
            surface.blit(row.image, row.rect.move((x_offset, 0)))


class Level(pg.sprite.Sprite):
    def __init__(self, level_num):
        super(Level, self).__init__()
        self.num = level_num
        info = LEVEL_INFO[self.num]
        self.unlock_cost = info["unlock cost"]
        self.sky_color = pg.Color(*info["sky"])
        self.text_color = pg.Color(*info["text color"])
        self.song = prepare.MUSIC[info["song"]]
        self.music_volume = info["music volume"]
        self.image = prepare.LEVELS["level{}".format(self.num)]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        fname = "jewels-level{}.json".format(self.num)
        p = os.path.join("resources", "jewels", fname)
        with open(p, "r") as f:
            jewels = json.load(f)        
        self.jewels = pg.sprite.Group()
        for pos, color in  jewels:
             Jewel(pos, color, self.jewels)
        self.jewel_goals = sorted(self.jewels, key=lambda x: x.rect.right)[::-1]
        self.waterfalls = [Waterfall(r) for r in info["waterfalls"]]
        self.max_score = self.get_max_score()
        
    def get_max_score(self):
        ordered = sorted(self.jewels, key=lambda x: x.rect.right)
        return sum((j.points * i for i, j in enumerate(ordered, start=1)))

    def cleanup(self):
        for w in self.waterfalls:
            w.sound_source.sound.stop()

    def update(self, dt, airship):
        self.jewels.update(dt)
        for w in self.waterfalls:
            w.update(dt, airship)
