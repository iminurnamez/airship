from itertools import cycle
from random import choice

import pygame as pg

from .. import tools, prepare
    
    

class Airship(pg.sprite.Sprite):
    def __init__(self):
        super(Airship, self).__init__()
        self.pos = (100, 100)
        self.vx = .2
        self.vy = 0
        self.accel = .0015
        self.image = prepare.GFX["airship"]
        self.rect = self.image.get_rect(center=self.pos)
        self.screen_rect = self.rect.copy()
        self.mask = pg.mask.from_surface(self.image)
        props = tools.strip_from_sheet(prepare.GFX["propstrip"], (0, 0), (3, 32), 10, 1)
        props.extend(props[-2:1:-1])
        self.prop_images = cycle(props)
        self.prop_image = next(self.prop_images)
        self.timer = 0
        self.prop_time = 20
        self.explode_time = 60
        self.explosions = tools.strip_from_sheet(prepare.GFX["explosion"], (0, 0), (64, 64), 12, 1)
        self.dead = False
        self.exploded = False
        self.crash_sounds = [prepare.SFX["crash{}".format(x)] for x in range(1, 5)]
        for s in self.crash_sounds:
            s.set_volume(.2)
        
    def update(self, dt):
        self.timer += dt
        if not self.exploded:
            if self.timer >= self.prop_time:
                self.timer -= self.prop_time
                self.prop_image =  next(self.prop_images)
            last = self.pos[0]
            self.vy += self.accel * dt
            if pg.mouse.get_pressed()[0]:
                self.vy -= self.accel * 2 * dt
            self.pos = self.pos[0] + (self.vx * dt), self.pos[1] + (self.vy * dt)
            self.rect.center = self.pos
            self.screen_rect.centery = self.rect.centery
            return self.pos[0] - last
        else:
            if self.timer >= self.explode_time:
                self.timer -= self.explode_time
                self.explosion_num += 1
                try:
                    self.image = self.explosions[self.explosion_num]
                except IndexError:
                    self.dead = True
            return 0
                
    def explode(self):
        choice(self.crash_sounds).play()
        self.explosion_num = 0
        self.image = self.explosions[self.explosion_num]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.screen_rect = self.image.get_rect(center=self.screen_rect.center)
        self.exploded = True
        self.timer = 0
        
        
    def draw(self, surface):
        surface.blit(self.image, self.screen_rect)
        if not self.exploded:
            surface.blit(self.prop_image, (self.screen_rect.left + 2, self.screen_rect.top + 26)) 