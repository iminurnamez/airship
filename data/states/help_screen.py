import pygame as pg

from .. import tools, prepare
from ..components.level import Jewel
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel


class HelpScreen(tools._State):
    def __init__(self):
        super(HelpScreen, self).__init__()
        self.msg = " ".join([
            "Earn points by collecting jewels as you navigate your airship through each level.",
            "Each consecutive jewel collected increases your jewel bonus by 1.",
            "Missing a jewel resets your bonus.",
            "Spend your points to unlock additional levels.",
            "You can replay each level as many times as you like,",
            "but you'll only recieve the number of points that are higher than your high score."])
        self.make_jewel_info()
        self.make_buttons()

    def startup(self, persistent):
        self.persist = persistent

    def make_jewel_info(self):
        colors = ["Yellow", "Green", "Red", "Pink", "Blue", "Grey"]
        left = 593
        top = 280
        self.jewels = pg.sprite.Group()
        self.labels = pg.sprite.Group()
        self.msg_label = MultiLineLabel(prepare.FONTS["weblysleekuisb"],
                                                      24, self.msg, "gray80",
                                                      {"midtop": (prepare.SCREEN_RECT.centerx, 8)},
                                                      bg=None, char_limit=64,
                                                      align="center", vert_space=0)
        Label("Jewel Values", {"center": (prepare.SCREEN_RECT.centerx, 232)},
                self.labels, text_color="antiquewhite", font_size=32)
        for color in colors:
            jewel = Jewel((left, top), color, self.jewels)
            Label("{}".format(jewel.points), {"center": (left + 64, top - 4)},
                     self.labels, font_size=24, text_color="antiquewhite")
            top += 48

    def finish(self, *args):
        self.done = True
        self.next = "LEVELSELECT"
        
    def make_buttons(self):
        sr = prepare.SCREEN_RECT
        self.buttons = ButtonGroup()
        Button((sr.centerx - 128, sr.bottom - 80), self.buttons, text="OK",
                   text_color=pg.Color("antiquewhite"), button_size=(256, 64),
                   fill_color=pg.Color("gray40"), hover_text="OK",
                   hover_text_color=pg.Color("antiquewhite"),
                   hover_fill_color=pg.Color("gray60"), call=self.finish,
                   font_size=48)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.buttons.get_event(event)

    def update(self, dt):
        self.jewels.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.fill(pg.Color("gray10"))
        self.jewels.draw(surface)
        self.labels.draw(surface)
        self.msg_label.draw(surface)
        self.buttons.draw(surface)
