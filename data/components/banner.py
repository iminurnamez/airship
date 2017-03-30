from math import pi, sin

import pygame as pg

from ..components.labels import Label


class BannerStrip(pg.sprite.Sprite):
    def __init__(self, topleft, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)
        self.pos = self.rect.topleft
        
    def update(self, x_move, y_pos):
        self.pos = self.pos[0] + x_move, y_pos
        self.rect.topleft = self.pos
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        
class Banner(pg.sprite.Sprite):
    def __init__(self, topleft, text, font_size, text_color, fill_color):
        self.topleft = topleft
        label = Label(text, {"topleft": (0, 0)}, text_color=text_color,
                            font_size=font_size, fill_color=fill_color)
        w, h = label.rect.size
        self.strips = [BannerStrip((self.topleft[0] + x, 0), label.image.subsurface((x, 0, 1, h)))
                            for x in range(w)][::-1]
        self.amplitude = 8
        self.frequency = .003
        self.timer = 0
        self.speed = .2
        
    def update(self, dt):
        self.timer -= dt
        x_move = self.speed * dt
        self.topleft = self.topleft[0] + x_move , self.topleft[1]
        for i, strip in enumerate(self.strips):
            siney = self.amplitude * sin(2*pi*self.frequency * (self.timer + i))
            y = self.topleft[1] - siney
            strip.update(x_move, y)
            
    def draw(self, surface):
        for s in self.strips:
            s.draw(surface)