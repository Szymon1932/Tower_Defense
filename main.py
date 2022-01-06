import pygame
import os
from enemies.cyber import Cyber
from towers.attackTower import AttackTower

pygame.font.init()

class Main:
    def __init__(self):
        self.szerokosc = 1200
        self.wysokosc = 800
        self.okno = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        self.tlo = pygame.image.load(os.path.join("resources", "map.png"))
        self.tlo = pygame.transform.scale(self.tlo, (self.szerokosc, self.wysokosc))
        self.wrogowie = [Cyber()]
        self.wieze_ataku=[AttackTower(100, 150)]
        self.wybrana_wieza = None
        self.stan_konta=100000

    def dzialanie(self):
        dzialanie = True
        zegar = pygame.time.Clock()
        while dzialanie:
            zegar.tick(60)
            pos = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    dzialanie = False
                if e.type == pygame.MOUSEBUTTONUP:
                    wybrany_element = None
                    if self.wybrana_wieza:
                        wybrany_element = self.wybrana_wieza.menu.wcisniecie_przyciskow_w_menu(pos[0], pos[1])
                        if wybrany_element:
                            if wybrany_element == 'Ulepsz':
                                koszt = self.wybrana_wieza.wartosc_ulepszenia()
                                print(koszt)
                                if self.stan_konta >= koszt:
                                    print(self.stan_konta)
                                    self.stan_konta -= koszt
                                    self.wybrana_wieza.ulepsz()
                    if wybrany_element==None:
                        for wieza in self.wieze_ataku:
                            if wieza.czy_wcisniete(pos[0], pos[1]):
                                wieza.czy_wybrano = True
                                self.wybrana_wieza = wieza
                            else:
                                wieza.czy_wybrano = False

            wrogowie_poza_mapa = []
            for e in self.wrogowie:
                if e.x<-20:
                    wrogowie_poza_mapa.append(e)
            for e in wrogowie_poza_mapa:
                self.wrogowie.remove(e)

            for wieza in self.wieze_ataku:
                self.stan_konta += wieza.atakuj(self.wrogowie)
            self.rysuj()
        pygame.quit()
    def rysuj(self):
        self.okno.blit(self.tlo, (0, 0))
        #rysowanie wrogów
        for e in self.wrogowie:
            e.rysuj(self.okno)
        #rysowanie wiez ataku
        for e in self.wieze_ataku:
            e.rysuj(self.okno)


        pygame.display.update()

main = Main()
main.dzialanie()