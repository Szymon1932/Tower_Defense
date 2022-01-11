import pygame
import os
import math
from .wieza import Wieza



wymiary_obrazka = 90
totem_zasieg = [pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/totems", "0.png")),
        (wymiary_obrazka,wymiary_obrazka))]

class TotemZasieg(Wieza):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.klatki = totem_zasieg[:]
        self.szerokosc=self.wysokosc=wymiary_obrazka
        self.zasieg = 75
        self.wzmocnienie = 0.25
        self.nazwa="totem_zasieg"

    def rysuj(self, okno):
        super().pokaz_zasieg_wiezy(okno)
        super().rysuj(okno)
    def dodaj_efekt(self, wieze_ataku):
        wzmocnione = []
        for w in wieze_ataku:
            x = w.x
            y = w.y
            zasieg = math.sqrt((self.x - x) ** 2+(self.y - y) ** 2)
            if zasieg <=self.zasieg+w.wysokosc/2:
                wzmocnione.append(w)
        for w in wzmocnione:
            w.zasieg = w.pierwotny_zasieg+ round(w.zasieg * self.wzmocnienie)

totem_obrazenia = [pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/totems", "1.png")),
        (wymiary_obrazka,wymiary_obrazka))]


class TotemObrazenia(TotemZasieg):
    def __init__(self,x,y):
        super().__init__(x, y)
        self.range = 75
        self.wzmocnienie = 2
        self.szerokosc=self.wysokosc=wymiary_obrazka
        self.klatki = totem_obrazenia
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
