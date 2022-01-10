import pygame
import math
import os

class Enemy:

    def __init__(self):
        self.szerokosc = 64
        self.wysokosc = 64
        self.aktualne_zdrowie = 1
        self.maksymalne_zdrowie = 0
        self.sciezka = [(-10, 225), (19, 221), (313, 226), (315, 359), (695, 360), (696, 141), (984, 139), (986, 674), (811, 676), (808, 495), (374, 494), (333, 479),(12, 479), (-25, 479)]
        self.aktualna_sciezka = 0
        self.x = self.sciezka[0][0]
        self.y = self.sciezka[0][1]
        self.klatka = pygame.image.load(os.path.join("resources/enemies/cyber","00.png"))
        self.klatki = []
        self.aktualna_klatka = 0
        self.czy_obrocony = False
        self.predkosc = 1

    def pokaz_zdrowie(self, okno):

        dlugosc = 50
        zmiana = round(dlugosc / self.maksymalne_zdrowie)
        pasek_zdrowia = zmiana * self.aktualne_zdrowie
        pygame.draw.rect(okno, (255,0 , 0), (self.x - 35, self.y - 35, dlugosc, 10), 0)
        pygame.draw.rect(okno, (0, 255, 0), (self.x - 35, self.y - 35, pasek_zdrowia, 10), 0)# czerwony pasek przykryje zielony w celu symulacji utraty zdrowia

    def utrata_zdrowia(self):
        self.aktualne_zdrowie -= 1
        if self.aktualne_zdrowie <= 0:
            return True
        return False

    def rysuj(self, okno):
        self.klatka = self.klatki[self.aktualna_klatka]
        self.aktualna_klatka += 1
        if self.aktualna_klatka >= len(self.klatki):
            self.aktualna_klatka = 0

        okno.blit(self.klatka, (self.x - self.klatka.get_width() / 2, self.y - self.klatka.get_height() / 2))
        self.pokaz_zdrowie(okno)
        self.ruch()


    def ruch(self):
        x1, y1 = self.sciezka[self.aktualna_sciezka]
        x2, y2 = self.sciezka[self.aktualna_sciezka + 1]

        wektor = ((x2 - x1), (y2 - y1))
        dlugosc = math.sqrt(wektor[0] ** 2 + wektor[1] ** 2)
        wektor = (wektor[0] / dlugosc * self.predkosc , wektor[1] / dlugosc * self.predkosc )


        if wektor[0] < 0 and not (self.czy_obrocony): #jeśli postać ruszałaby się w lewo i nie była obrócona
            self.czy_obrocony = True
            for x, img in enumerate(self.klatki):
                self.klatki[x] = pygame.transform.flip(img, True, False) #(obrazek, os X, os Y) - obrot obrazka wokol osi X

        self.x += wektor[0]
        self.y += wektor[1]
        if wektor[0] >= 0:  # ruch w prawo
            if wektor[1] > 0:  # w dół
                if self.x >= x2 and self.y >= y2:  # gdy postać pójdzie odpowiednio daleko w dół
                    self.aktualna_sciezka += 1
            elif wektor[1]<=0:
                if self.x >= x2 and self.y <= y2: # gdy postać pójdzie odpowiednio daleko w górę
                    self.aktualna_sciezka += 1
        else:  # ruch w lewo
            if wektor[1] > 0:  # w dół
                if self.x <= x2 and self.y >= y2:  # gdy postać pójdzie odpowiednio daleko w dół
                    self.aktualna_sciezka += 1
            elif wektor[1] <= 0:
                if self.x <= x2 and self.y <= y2: # gdy postać pójdzie odpowiednio daleko w górę
                    self.aktualna_sciezka += 1



    def atakuj(self, obrazenia):
        self.aktualne_zdrowie -= obrazenia
        if self.aktualne_zdrowie <= 0:
            return True
        return False