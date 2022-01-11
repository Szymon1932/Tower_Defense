import pygame
import os
from menu import Menu

tlo_menu = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (150, 80))
ulepszenie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "upgrade.png")), (50, 50))





class Tower:
    def __init__(self,X,Y):
        self.x=X
        self.y=Y
        self.szerokosc=0
        self.wysokosc=0
        self.poziom = 0
        self.klatki = []
        self.obrazenia = 1
        self.czy_wybrano = False
        self.menu = Menu(self, self.x, self.y, tlo_menu, 0)
        self.zasieg = 100
    def rysuj(self, win):
        img= self.klatki[self.poziom]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))
        if self.czy_wybrano:
            self.menu.rysuj(win)

    def czy_wcisniete(self, X, Y):
        obiekt = self.klatki[self.poziom]
        if  X >= self.x - obiekt.get_width() // 2 and X <= self.x - obiekt.get_width() // 2 + self.szerokosc:  #kiedy klik w obszarze wiezy
            if  Y >= self.y - obiekt.get_height() // 2 and Y <= self.y - obiekt.get_height() // 2 + self.wysokosc:
                return True
        return False

    def ulepsz(self):
        print(len(self.klatki))
        if self.poziom +1 < len(self.klatki):
            self.poziom+=1
            self.obrazenia +=1
            print(self.klatki)
        else:
            self.poziom=self.poziom
            self.obrazenia=self.obrazenia

    def pokaz_zasieg_wiezy(self, okno):

        if self.czy_wybrano == True:
            powierzchnia = pygame.Surface((self.zasieg * 4, self.zasieg * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(powierzchnia, (64,64,64,100), (self.zasieg, self.zasieg), self.zasieg, 0)
            okno.blit(powierzchnia, (self.x - self.zasieg, self.y - self.zasieg))
