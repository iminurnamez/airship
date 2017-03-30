from __future__ import division
from math import hypot

import pygame as pg

from .. import prepare


class SoundSource(object):
    def __init__(self, sound, pos, max_volume, audible_range):
        """        
        sound: a pygame.Sound object
        pos: x, y position for calculating distance to listener
        max_volume: float between 0 and 1 (inclusive), this is the volume when 
                             the distance to the listener is 0
        audible_range: int or float, distance at which sound begins playing (at volume 0)
        """
        self.sound = sound
        self.pos = pos
        self.max_volume = max_volume
        self.audible_range = audible_range
        self.active = False
        
    def update(self, listener):
        active = False
        distance_to_listener = abs(self.pos[0] - listener.pos[0])
        if distance_to_listener <= self.audible_range:
            active = True
            volume = self.max_volume * (1 - (distance_to_listener / self.audible_range))
            self.sound.set_volume(volume)
        else:
            active = False
            self.sound.stop()
        if active:
            if not self.active:
                self.sound.play(-1)
        self.active = active                
        
    