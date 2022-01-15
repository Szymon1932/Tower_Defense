import pygame
import os
from .wieza import Wieza
import math

from menu import Menu



menu_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (150, 80))
przycisk_ulepszenie = pygame.transform.scale(pygame.image.load(os.path.join("resources", "upgrade.png")), (50, 50))

#generowanie animacji przed wygenerowaniem obiektu
klatki_wieza_atakujaca=[]
lucznik_klatki=[]
for x in range(1, 4):
    klatki_wieza_atakujaca.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/attack", str(x) + ".png")),
        (90, 90)))

for x in range(0,10):
    lucznik_klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/archer", str(x) + ".png")),
        (200, 100)))


class WiezaAtaku(Wieza):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.synchronizacja_klatek = 4
        self.szerokosc=self.wysokosc=90
        self.klatki=klatki_wieza_atakujaca
        self.lucznik_klatki = lucznik_klatki[:]
        self.lucznik_klatka = 0
        self.menu = Menu(self, self.x, self.y, menu_tlo, [2000, 5000, "MAX"])
        self.menu.dodaj_nastepny_przycisk(przycisk_ulepszenie, "Ulepsz")
        self.pierwotny_zasieg = self.zasieg = 200
        self.w_zasiegu = False
        self.pierwotne_obrazenia=self.obrazenia = 1
        self.czy_obrocony=True
        self.nazwa="wieza_ataku"


    def rysuj(self, okno):
        super().pokaz_zasieg_wiezy(okno)
        super().rysuj(okno)

        lucznik = self.lucznik_klatki[self.lucznik_klatka//self.synchronizacja_klatek]
        okno.blit(lucznik, ((self.x - lucznik.get_width() / 2 - 5), (self.y - lucznik.get_height() - 15)))

    def atakuj(self, wrogowie):
        if self.w_zasiegu:
            self.lucznik_klatka += 1
            if self.lucznik_klatka >= len(self.lucznik_klatki)*self.synchronizacja_klatek:
                self.lucznik_klatka = 0
        else:
            self.lucznik_klatka = 0
        stan_konta=0
        self.w_zasiegu = False
        wrogowie_tab = []
        for w in wrogowie:
            x = w.x
            y = w.y

            odleglosc = math.sqrt((self.x - w.klatka.get_width() / 2 - x) ** 2 + (self.y - w.klatka.get_height() / 2 - y) ** 2)
            if odleglosc < self.zasieg:
                self.w_zasiegu = True
                wrogowie_tab.append(w) #dodawanie najblizszego przeciwnika do tablicy do ataku

        wrogowie_tab.sort(key=lambda przeciwnik: przeciwnik.x) #sortowanie po wspolrzednej X przeciwnika. Ostatni element ma najwiekszy X
        wrogowie_tab=wrogowie_tab[::-1]

        if len(wrogowie_tab) > 0:
            pierwszy_przeciwnik = wrogowie_tab[0]
            if self.lucznik_klatka == 8 * self.synchronizacja_klatek: # lucznik strzela do celu w klatce 8 - imitacja uderzenia
                if pierwszy_przeciwnik.atakuj(self.obrazenia) ==True:
                    stan_konta+= pierwszy_przeciwnik.stan_konta
                    wrogowie.remove(pierwszy_przeciwnik)

            if self.czy_obrocony and pierwszy_przeciwnik.x < self.x:
                self.czy_obrocony = False
                for x, img in enumerate(self.lucznik_klatki):
                    self.lucznik_klatki[x] = pygame.transform.flip(img, True, False)

            elif not (self.czy_obrocony) and pierwszy_przeciwnik.x>self.x:
                self.czy_obrocony = True
                for x, img in enumerate(self.lucznik_klatki):
                    self.lucznik_klatki[x] = pygame.transform.flip(img, True, False)

        return stan_konta #zwraca stan konta po zabiciu przeciwnika


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
        self.synchronizacja_klatek = 4
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
