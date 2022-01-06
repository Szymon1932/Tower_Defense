import pygame
import os
from .tower import Tower
import math

from menu import Menu

klatki_wieza_atakujaca=[]
lucznik_klatki=[]
synchronizacja_klatek=4
wymiary_obrazka = 90

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("resources","menu.png")),(150,80))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("resources","upgrade.png")),(50,50))


for x in range(1, 4):  # index of towers
    # load towers
    klatki_wieza_atakujaca.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/attack", str(x) + ".png")),
        (wymiary_obrazka, wymiary_obrazka)))

for x in range(0,10):
    lucznik_klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/towers/archer", str(x) + ".png")),
        (200, 100)))


class AttackTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.szerokosc=self.wysokosc=wymiary_obrazka
        self.klatki=klatki_wieza_atakujaca
        self.lucznik_klatki = lucznik_klatki
        self.lucznik_klatka = 0
        self.menu = Menu(self,self.x, self.y, menu_bg,[2000,5000,"MAX"])
        self.menu.dodaj_nastepny_przycisk(upgrade_btn, "Ulepsz")
        self.zasieg = 200
        self.w_zasiegu = False
        self.obrazenia = 1
        self.czy_obrocony=True

    def wartosc_ulepszenia(self):
        return self.menu.pobierz_wartosc_obiektu()

    def rysuj(self, win):
        super().rysuj(win)
        if self.w_zasiegu:
            self.lucznik_klatka += 1
            if self.lucznik_klatka >= len(self.lucznik_klatki)*synchronizacja_klatek:
                self.lucznik_klatka = 0
        else:
            self.lucznik_klatka = 0
        lucznik = self.lucznik_klatki[self.lucznik_klatka//synchronizacja_klatek]
        win.blit(lucznik, ((self.x - lucznik.get_width() / 2 - 5), (self.y - lucznik.get_height()-15)))

    def atakuj(self, wrogowie):
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
            if self.lucznik_klatka == 8 * synchronizacja_klatek: # lucznik strzela do celu w klatce 8 - imitacja uderzenia
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
