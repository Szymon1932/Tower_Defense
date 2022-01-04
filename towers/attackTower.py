import pygame
import os
from .tower import Tower


klatki_wieza_atakujaca=[]
lucznik_klatki=[]

for x in range(1, 3):  # index of towers
    # load towers
    klatki_wieza_atakujaca.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/attack", str(x) + ".png")),
        (90, 90)))

for x in range(0, 9):
    lucznik_klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/archer", str(x) + ".png")),
        (200, 100)))


class AttackTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.szerokosc=self.wysokosc=90
        self.klatki=klatki_wieza_atakujaca
        self.lucznik_klatki = lucznik_klatki
        self.lucznik_klatka = 0
        self.zasieg = 200
        self.w_zasiegu = True
        self.obrazenia = 1

    def rysuj(self, win):
        super().rysuj(win)
        if self.w_zasiegu:
            self.lucznik_klatka += 1
            if self.lucznik_klatka >= len(self.lucznik_klatki):
                self.lucznik_klatka = 0
        else:
            self.lucznik_klatka = 0
        lucznik = self.lucznik_klatki[self.lucznik_klatka]
        win.blit(lucznik, ((self.x - lucznik.get_width() / 2 - 5), (self.y - lucznik.get_height()-15)))
