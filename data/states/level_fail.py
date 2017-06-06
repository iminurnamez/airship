import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Blinker


class LevelFailScreen(tools._State):
    def __init__(self): 
        super(LevelFailScreen, self).__init__()
        self.song = prepare.MUSIC["sadorchestra"]
        self.music_volume = .5

    def startup(self, persistent):
        self.timer = 0
        self.persist = persistent
        level = self.persist["level"]
        self.bg = pg.display.get_surface().copy()
        text = self.persist["text"]
        self.labels = pg.sprite.Group()
        Label(text, {"midbottom": prepare.SCREEN_RECT.center},
                 self.labels, text_color=level.text_color, font_size=64)
        Blinker("Click to restart level",
                {"midtop": prepare.SCREEN_RECT.center},
                 500, self.labels, text_color=level.text_color, font_size=32)
        
    def update(self, dt):
        self.timer += dt
        self.labels.update(dt)
        if not pg.mixer.music.get_busy():
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.load(self.song)
            pg.mixer.music.play()            
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONUP and self.timer >= prepare.FADE_TIME:
            self.done = True
            self.next = "GAMEPLAY"
            pg.mixer.music.fadeout(1000)

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.labels.draw(surface)
        
    