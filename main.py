import pygame
import os
from enemies.cyber import Cyber
from enemies.marshall import Marshall
from enemies.barney import Barney
from enemies.ted import Ted
from towers.attackTower import AttackTower
from menu import PauzaPrzycisk, MenuGry
import time
import random

pygame.font.init()

przycisk_play = pygame.transform.scale(pygame.image.load(os.path.join("resources", "play.png")), (80, 80))
przycisk_pauza = pygame.transform.scale(pygame.image.load(os.path.join("resources", "pause.png")), (80, 80))
rundy=[[11,0,0,0],[1,0,0,0]]
wymiar_ikony = 90
obraz_menu = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (720, 180))
kup_atak_1 = pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_1.png")), (wymiar_ikony, wymiar_ikony))
kup_atak_2 = pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_2.png")), (wymiar_ikony, wymiar_ikony))
kup_totem_1 = pygame.transform.scale(pygame.image.load(os.path.join("resources", "attack_totem.png")), (wymiar_ikony, wymiar_ikony))
kup_totem_2= pygame.transform.scale(pygame.image.load(os.path.join("resources", "range_totem.png")), (wymiar_ikony, wymiar_ikony))

class Main:
    def __init__(self):
        self.szerokosc = 1200
        self.wysokosc = 800
        self.okno = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        self.tlo = pygame.image.load(os.path.join("resources", "map.png"))
        self.tlo = pygame.transform.scale(self.tlo, (self.szerokosc, self.wysokosc))
        self.wrogowie = []
        self.wieze_ataku=[AttackTower(100,300)]
        self.wybrana_wieza = None
        self.stan_konta=100000
        self.pauza_przycisk = PauzaPrzycisk(przycisk_play, przycisk_pauza, self.szerokosc - przycisk_play.get_width() - 15, 15)
        self.pauza=False
        self.ilosc_wrogow=10
        self.runda = 0
        self.obecna_runda= rundy[self.runda][:]
        self.czas =time.time()
        self.zycia = 4
        self.menu = MenuGry(obraz_menu.get_width() / 2 + 25, 675, obraz_menu)
        self.menu.dodaj_nastepny_przycisk(kup_atak_1, "kup_atak_1", 1500)
        self.menu.dodaj_nastepny_przycisk(kup_atak_2, "kup_atak_2", 2000)
        self.menu.dodaj_nastepny_przycisk(kup_totem_1, "kup_totem_1", 1200)
        self.menu.dodaj_nastepny_przycisk(kup_totem_2, "kup_totem_2", 1000)

    def stworzenie_wrogow(self):

        if sum(self.obecna_runda) == 0:
            if len(self.wrogowie) == 0:
                self.runda += 1
                if self.runda >= len(rundy):
                    print("Koniec gry")
                    exit(0)
                self.obecna_runda = rundy[self.runda]


        else:
            obecni_wrogowie = [Cyber(), Barney(),Marshall(),Ted()]
            for e in range(len(self.obecna_runda)):
                if self.obecna_runda[e] != 0:
                    self.wrogowie.append(obecni_wrogowie[e])
                    self.obecna_runda[e] = self.obecna_runda[e] - 1
                    break

    def dzialanie(self):
        dzialanie = True
        zegar = pygame.time.Clock()
        while dzialanie:
            zegar.tick(60)
            if self.pauza==False:
                if time.time() - self.czas >= random.randrange(1, 2): #generowanie stworów co okreslony losowy czas
                    self.czas = time.time()
                    self.stworzenie_wrogow()

            pos = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    dzialanie = False
                if e.type == pygame.MOUSEBUTTONUP:
                    wybrany_element = None
                    if self.wybrana_wieza: #wybrano wieze
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
                    self.zycia -= 1
                    print("Aktualne zycia: "+ str(self.zycia))
            for e in wrogowie_poza_mapa:
                self.wrogowie.remove(e)

            for wieza in self.wieze_ataku:
                self.stan_konta += wieza.atakuj(self.wrogowie)



            if self.zycia <=0:
                print("Przegrana")
                exit(0)


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
        #rysowanie pauzy
        self.pauza_przycisk.rysuj(self.okno)
        #rysowanie menu
        self.menu.rysuj(self.okno)
        pygame.display.update()

main = Main()
main.dzialanie()