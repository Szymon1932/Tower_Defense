import pygame
import os
from .wiezaAtaku import WiezaAtaku
from menu import Menu

menu_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (150, 80))
przycisk_ulepszenie = pygame.transform.scale(pygame.image.load(os.path.join("resources", "upgrade.png")), (50, 50))

klatki_wieza_atakujaca_2=[]
lucznik_klatki_2=[]

for x in range(0, 3):
    klatki_wieza_atakujaca_2.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/attack_2", str(x) + ".png")),
        (90, 90)))

for x in range(0,10):
    lucznik_klatki_2.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/archer", str(x) + ".png")),
        (200, 100)))


class WiezaAtaku_2(WiezaAtaku):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.synchronizacja_klatek = 6
        self.szerokosc=self.wysokosc=90
        self.klatki=klatki_wieza_atakujaca_2
        self.lucznik_klatki = lucznik_klatki_2
        self.lucznik_klatka = 0
        self.menu = Menu(self, self.x, self.y, menu_tlo, [2000, 5000, "MAX"])
        self.menu.dodaj_nastepny_przycisk(przycisk_ulepszenie, "Ulepsz")
        self.pierwotny_zasieg = self.zasieg = 150
        self.w_zasiegu = False
        self.obrazenia=self.pierwotne_obrazenia = 2
        self.czy_obrocony=True
        self.nazwa = "wieza_ataku_2"

