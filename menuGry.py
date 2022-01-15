from menu import Menu
from przyciskMenu import PrzyciskMenu
import pygame
import os

gwiazda_ulepszenie = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (50, 50))
gwiazda_ulepszenie_mniejsza = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (27, 27))

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
        przycisk_x = self.x - 325 +(self.ilosc_przyciskow-1)*180
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