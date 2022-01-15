import pygame
import os
from menu import Menu
import math

tlo_menu = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (150, 80))
ulepszenie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "upgrade.png")), (50, 50))


class Wieza:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.szerokosc = 0
        self.wysokosc = 0
        self.poziom = 0
        self.klatki = []
        self.czy_wybrano = False
        self.menu = Menu(self, self.x, self.y, tlo_menu, ["MAX"])
        self.menu.dodaj_nastepny_przycisk(ulepszenie_tlo, "Ulepsz")
        self.zasieg_pierwotny = self.zasieg = 100
        self.pierwotne_obrazenia = self.obrazenia = 1
        self.kolor_wiezy = (12, 255, 14, 100)
        self.promien_kola_wiezy = 35

    def rysuj(self, win):
        img = self.klatki[self.poziom]
        win.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))
        if self.czy_wybrano:
            self.menu.rysuj(win)

    def czy_wcisniete(self, X, Y):
        obiekt = self.klatki[self.poziom]
        if X >= self.x - obiekt.get_width() // 2 and X <= self.x - obiekt.get_width() // 2 + self.szerokosc:  # kiedy klik w obszarze wiezy
            if Y >= self.y - obiekt.get_height() // 2 and Y <= self.y - obiekt.get_height() // 2 + self.wysokosc:
                return True
        return False

    def ulepsz(self):
        if self.poziom + 1 < len(self.klatki):
            self.poziom += 1
            self.obrazenia += 1
            self.pierwotne_obrazenia += 1
        else:
            self.poziom = self.poziom
            self.obrazenia = self.obrazenia
            self.pierwotne_obrazenia = self.pierwotne_obrazenia

    def pokaz_zasieg_wiezy(self, okno):

        if self.czy_wybrano == True:
            powierzchnia = pygame.Surface((self.zasieg * 4, self.zasieg * 4), pygame.SRCALPHA)
            pygame.draw.circle(powierzchnia, (64, 64, 64, 100), (self.zasieg, self.zasieg), self.zasieg, 0)
            okno.blit(powierzchnia, (self.x - self.zasieg, self.y - self.zasieg))

    def wartosc_ulepszenia(self):
        return self.menu.pobierz_wartosc_obiektu()

    def kolizja(self, wieza_2):
        odleglosc = math.sqrt((wieza_2.x - self.x) ** 2 + (wieza_2.y - self.y) ** 2)
        if odleglosc >= self.promien_kola_wiezy * 2:
            return False
        elif odleglosc < self.promien_kola_wiezy * 2:
            return True

    def wydzielenie_obszaru(self, okno):
        powierzchnia = pygame.Surface((self.zasieg * 4, self.zasieg * 4), pygame.SRCALPHA)
        pygame.draw.circle(powierzchnia, self.kolor_wiezy, (self.promien_kola_wiezy, self.promien_kola_wiezy),
                           self.promien_kola_wiezy, 0)
        okno.blit(powierzchnia, (self.x - self.promien_kola_wiezy, self.y - self.promien_kola_wiezy))

    def przeniesienie(self, x, y):
        self.menu.x = self.x = x
        self.menu.y = self.y = y
        self.menu.zmiana_pol()
