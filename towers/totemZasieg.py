import pygame
import os
import math
from .wieza import Wieza


class TotemZasieg(Wieza):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.wymiary_obrazka = 90
        self.totem_zasieg = [pygame.transform.scale(
            pygame.image.load(os.path.join("resources/towers/totems", "0.png")),
            (self.wymiary_obrazka, self.wymiary_obrazka))]
        self.klatki = self.totem_zasieg[:]
        self.szerokosc = self.wysokosc = self.wymiary_obrazka
        self.zasieg = 125
        self.wzmocnienie = 0.25
        self.nazwa = "totem_zasieg"

    def rysuj(self, okno):
        super().pokaz_zasieg_wiezy(okno)
        super().rysuj(okno)

    def dodaj_efekt(self, wieze_ataku):
        wzmocnione = []
        for w in wieze_ataku:
            x = w.x
            y = w.y
            zasieg = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if zasieg <= self.zasieg + w.wysokosc / 2:
                wzmocnione.append(w)
        for w in wzmocnione:
            w.zasieg = w.pierwotny_zasieg + round(w.zasieg * self.wzmocnienie)
