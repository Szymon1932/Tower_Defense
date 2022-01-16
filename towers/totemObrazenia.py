import pygame
import os
import math
from .totemZasieg import TotemZasieg
class TotemObrazenia(TotemZasieg):
    def __init__(self,x,y):
        super().__init__(x, y)
        self.wymiary_obrazka=90
        self.totem_obrazenia = [pygame.transform.scale(
            pygame.image.load(os.path.join("resources/towers/totems", "1.png")),
            (self.wymiary_obrazka, self.wymiary_obrazka))]
        self.range = 125
        self.wzmocnienie = 2
        self.szerokosc=self.wysokosc=self.wymiary_obrazka
        self.klatki = self.totem_obrazenia
        self.nazwa="totem_obrazenia"

    def dodaj_efekt(self, wieze_ataku):
        wzmocnione = []
        for w in wieze_ataku:
            x = w.x
            y = w.y
            zasieg = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if zasieg <= self.zasieg + w.wysokosc / 2:
                wzmocnione.append(w)
        for w in wzmocnione:
            w.obrazenia = w.pierwotne_obrazenia * self.wzmocnienie
