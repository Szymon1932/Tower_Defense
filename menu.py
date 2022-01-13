import pygame
import os


gwiazda_ulepszenie = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (50, 50))
gwiazda_ulepszenie_mniejsza = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (27, 27))

korekta_x = 60
korekta_y = 90
class Przycisk:
    def __init__(self, menu, img, nazwa):
        self.nazwa = nazwa
        self.img = img
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.x = menu.x - korekta_x
        self.y = menu.y - korekta_y
        self.menu = menu

    def czy_wcisniete(self, X, Y):
        if X <= self.x + self.szerokosc and X >= self.x:
            if Y <= self.y + self.wysokosc and Y >= self.y:
                return True
        return False

    def rysuj(self, okno):
        okno.blit(self.img, (self.x, self.y))

    def update(self):
        """
        updates menu position
        :return: none
        """
        self.x = self.menu.x - korekta_x
        self.y = self.menu.y - korekta_y

class PauzaPrzycisk(Przycisk):
    def __init__(self,przycisk_play,przycisk_pauza,x,y):
        self.x = x
        self.y = y
        self.img = przycisk_play
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.przycisk_play = przycisk_play
        self.przycisk_pauza = przycisk_pauza
        self.pauza=False

    def rysuj(self, okno):
        if self.pauza:
            okno.blit(self.przycisk_play, (self.x, self.y))
        else:
            okno.blit(self.przycisk_pauza, (self.x, self.y))

class PrzyciskMenu(Przycisk):
    def __init__(self,x,y,img,nazwa,koszt):
        self.nazwa = nazwa
        self.img = img
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.x = x
        self.y = y
        self.koszt = koszt


class Menu:
    def __init__(self, wieza, x, y, img, wartosc):
        self.x=x
        self.y=y
        self.wartosc = wartosc
        self.przyciski = []
        self.ilosc_przyciskow = 0
        self.tlo = img
        self.font = pygame.font.SysFont("comicsans", 22)
        self.wieza = wieza
        self.szerokosc = img.get_width()
        self.wysokosc = img.get_height()

    def dodaj_nastepny_przycisk(self, img, name):
        self.ilosc_przyciskow +=1
        self.przyciski.append(Przycisk(self, img, name))

    def rysuj(self, okno):
        okno.blit(self.tlo, (self.x - self.tlo.get_width() / 2, self.y - 100))
        for przycisk in self.przyciski:
            przycisk.rysuj(okno)
            text = self.font.render(str(self.wartosc[self.wieza.poziom]), True, (255, 255, 255))
            okno.blit(gwiazda_ulepszenie, (przycisk.x + przycisk.szerokosc + 5, przycisk.y - 8))
            okno.blit(text, (przycisk.x + przycisk.szerokosc + 30 - text.get_width() / 2, przycisk.y + gwiazda_ulepszenie.get_height() - 9))


    def pobierz_wartosc_obiektu(self):
        pom = self.wartosc[self.wieza.poziom]
        print(pom)
        if isinstance(pom, str): #gdy jest MAX
            return 0
        return self.wartosc[self.wieza.poziom]

    def czy_wcisniete(self, X, Y):
        if X <=self.x + self.szerokosc and X >=self.x:
            if Y<=self.y + self.wysokosc and Y >=self.y:
                return True
        return False
    def wcisniecie_ikony(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.przyciski:
            if btn.czy_wcisniete(X,Y):
                return btn.nazwa
        return None

    def wcisniecie_przyciskow_w_menu(self, X, Y):
        for p in self.przyciski:
            if p.czy_wcisniete(X, Y):
                return p.nazwa
        return None

    def update(self):
        """update menu and btn location"""
        for btn in self.przyciski:
            btn.update()
class MenuGry(Menu):
    def __init__(self, x, y, img):
        self.x=x
        self.y=y
        self.szerokosc = img.get_width()
        self.wysokosc = img.get_height()
        self.przyciski = []
        self.ilosc_przyciskow = 0
        self.font = pygame.font.SysFont("comicsans", 27)
        self.tlo = img

    def dodaj_nastepny_przycisk(self, img, name,cost):
        self.ilosc_przyciskow +=1
        przycisk_x = self.x -325 +(self.ilosc_przyciskow-1)*180
        przycisk_y = self.y-75
        self.przyciski.append(PrzyciskMenu(przycisk_x, przycisk_y, img, name, cost))

    def rysuj(self, okno):
        okno.blit(self.tlo, (self.x - self.tlo.get_width() / 2, self.y - 100))
        for przycisk in self.przyciski:
            przycisk.rysuj(okno)
            text = self.font.render(str(przycisk.koszt), True, (255, 255, 255))
            wymiar_x = przycisk.x -8
            wymiar_y = przycisk.y + przycisk.wysokosc + 8
            okno.blit(gwiazda_ulepszenie_mniejsza, (wymiar_x, wymiar_y))
            wymiar_x = przycisk.x + przycisk.szerokosc/2- text.get_width() / 2 + 7
            wymiar_y = przycisk.y + przycisk.wysokosc +5
            okno.blit(text, (wymiar_x, wymiar_y))


    def pobierz_wartosc_obiektu(self,nazwa):

        for przycisk in self.przyciski:
            if przycisk.nazwa == nazwa:
                return przycisk.koszt
        return 0

