import pygame
import os
from enemies.cyber import Cyber
from enemies.marshall import Marshall
from enemies.barney import Barney
from enemies.ted import Ted
from towers.wiezaAtaku import WiezaAtaku, WiezaAtaku_2
from menu import PauzaPrzycisk, MenuGry
import time
import random
from towers.totem import TotemZasieg, TotemObrazenia
import math
pygame.font.init()

lista_obiektow = ["wieza_ataku", "wieza_ataku_2", "totem_obrazenia", "totem_zasieg"]

przycisk_play = pygame.transform.scale(pygame.image.load(os.path.join("resources", "play.png")), (80, 80))
przycisk_pauza = pygame.transform.scale(pygame.image.load(os.path.join("resources", "pause.png")), (80, 80))
rundy=[[1,0,0,0],[1,0,0,10]]
wymiar_ikony = 90
obraz_menu = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (720, 180))
wieza_ataku = pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_1.png")), (wymiar_ikony, wymiar_ikony))
wieza_ataku_2 = pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_2.png")), (wymiar_ikony, wymiar_ikony))
totem_obrazenia = pygame.transform.scale(pygame.image.load(os.path.join("resources", "attack_totem.png")), (wymiar_ikony, wymiar_ikony))
totem_zasieg= pygame.transform.scale(pygame.image.load(os.path.join("resources", "range_totem.png")), (wymiar_ikony, wymiar_ikony))


wieze_ataku=["wieza_ataku", "wieza_ataku_2"]
totemy=["totem_obrazenia", "totem_zasieg"]
sciezka = [(-10, 225), (19, 221), (313, 226), (315, 359), (695, 360), (696, 141), (984, 139), (986, 674), (811, 676),
           (808, 495), (374, 494), (333, 479), (12, 479), (-25, 479)]
sciezka_n = [(11, 220),(100,220),(200,220), (309, 228), (308, 354),(400,354),(500,354),(600,354), (690, 354),(690,254), (694, 146),(794, 146),(894, 146), (978, 147),(978, 247),(978, 347),(978, 447),(978, 547), (979, 678), (814, 679),(814, 579), (807, 505),(707, 505),(607, 505),(507, 505), (374, 502), (337, 480), (237, 480),(137, 480),(10, 479)]
konto_ikona = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (60, 60))
zycie_ikona = pygame.transform.scale(pygame.image.load(os.path.join("resources", "heart.png")), (64, 64))
runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (150, 70))
zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (110, 70))
konto_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (200, 70))
font_wielkosc = 40
font_ikony = 50
class Main:
    def __init__(self):
        self.szerokosc = 1200
        self.wysokosc = 800
        self.okno = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        self.tlo = pygame.image.load(os.path.join("resources", "map.png"))
        self.tlo = pygame.transform.scale(self.tlo, (self.szerokosc, self.wysokosc))
        self.wrogowie = []
        self.wieze_ataku=[]
        self.totemy=[]
        self.wybrana_wieza = None
        self.stan_konta=789554564
        self.pauza_przycisk = PauzaPrzycisk(przycisk_play, przycisk_pauza, self.szerokosc - przycisk_play.get_width() - 15, 15)
        self.pauza=False
        self.pauza_przycisk.pauza=self.pauza
        self.runda = 0
        self.obecna_runda= rundy[self.runda][:]
        self.czas =time.time()
        self.zycia = 10
        self.menu = MenuGry(obraz_menu.get_width() / 2 + 25, 675, obraz_menu)
        self.menu.dodaj_nastepny_przycisk(wieza_ataku, "wieza_ataku", 1500)
        self.menu.dodaj_nastepny_przycisk(wieza_ataku_2, "wieza_ataku_2", 2000)
        self.menu.dodaj_nastepny_przycisk(totem_obrazenia, "totem_obrazenia", 1200)
        self.menu.dodaj_nastepny_przycisk(totem_zasieg, "totem_zasieg", 1000)
        self.obiekt_z_menu=None
        self.menu_font = pygame.font.SysFont("comicsans", font_wielkosc)
        self.zycie_konto_font = pygame.font.SysFont("comicsans", font_ikony)
        self.sciezka_n=[]
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
            if self.obiekt_z_menu:
                self.bliskosc_do_sciezki(self.obiekt_z_menu)
                czy_kolizja = False
                self.obiekt_z_menu.przeniesienie(pos[0], pos[1])
                wieze = self.wieze_ataku[:]
                wieze += self.totemy[:]

                if self.bliskosc_do_sciezki(self.obiekt_z_menu):
                    czy_kolizja = False
                    self.obiekt_z_menu.kolor_wiezy = (14, 255, 12, 100)
                elif not self.bliskosc_do_sciezki(self.obiekt_z_menu):
                    czy_kolizja = True
                    self.obiekt_z_menu.kolor_wiezy = (255, 14, 12, 100)
                for w in wieze:
                    if w.kolizja(self.obiekt_z_menu):
                        czy_kolizja = True
                        w.kolor_wiezy = (255, 14, 12, 100)
                        self.obiekt_z_menu.kolor_wiezy = (255, 14, 12, 100)
                    else:
                        w.kolor_wiezy = (12, 255, 14, 100)
                        if not czy_kolizja:
                            self.obiekt_z_menu.kolor_wiezy = (12, 255, 14, 100)


            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    dzialanie = False
                if e.type == pygame.MOUSEBUTTONUP:
                    self.sciezka_n.append(pos)
                    print(self.sciezka_n)
                    if self.obiekt_z_menu:
                        self.bliskosc_do_sciezki(self.obiekt_z_menu)
                        czy_postawic_obiekt = True
                        wieze = self.wieze_ataku[:]
                        wieze += self.totemy[:]
                        for w in wieze:
                            if w.kolizja(self.obiekt_z_menu):
                                czy_postawic_obiekt = False

                        if czy_postawic_obiekt and self.bliskosc_do_sciezki(self.obiekt_z_menu):
                            if self.obiekt_z_menu.nazwa in wieze_ataku:
                                self.wieze_ataku.append(self.obiekt_z_menu)
                            elif self.obiekt_z_menu.nazwa in totemy:
                                self.totemy.append(self.obiekt_z_menu)
                            self.obiekt_z_menu = None

                    else:
                        if self.pauza_przycisk.czy_wcisniete(pos[0],pos[1]):
                            self.pauza = not(self.pauza)
                            self.pauza_przycisk.pauza = self.pauza
                        ikonka_menu = self.menu.wcisniecie_ikony(pos[0], pos[1])
                        if ikonka_menu:
                            cost = self.menu.pobierz_wartosc_obiektu(ikonka_menu)
                            if self.stan_konta >= cost:
                                self.stan_konta -= cost
                                self.dodaj_wieze(ikonka_menu)

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
                            #czy kliknięto w wieze ataku
                            for wieza in self.wieze_ataku:
                                if wieza.czy_wcisniete(pos[0], pos[1]):
                                    wieza.czy_wybrano = True
                                    self.wybrana_wieza = wieza
                                else:
                                    wieza.czy_wybrano = False
                            #czy kliknięto na totem
                            for totem in self.totemy:
                                if totem.czy_wcisniete(pos[0], pos[1]):
                                    totem.czy_wybrano = True
                                    self.wybrana_wieza = totem
                                else:
                                    totem.czy_wybrano = False


            wrogowie_poza_mapa = []
            if not self.pauza:
                for e in self.wrogowie:
                    e.ruch()
                    if e.x<-20:
                        wrogowie_poza_mapa.append(e)
                        self.zycia -= 1
                        print("Aktualne zycia: "+ str(self.zycia))
                for e in wrogowie_poza_mapa:
                    self.wrogowie.remove(e)

                for wieza in self.wieze_ataku:
                    self.stan_konta += wieza.atakuj(self.wrogowie)

                for tw in self.totemy:
                    tw.dodaj_efekt(self.wieze_ataku)


                if self.zycia <=0:
                    print("Przegrana")
                    exit(0)


            self.rysuj()
        pygame.quit()
    def rysuj(self):
        self.okno.blit(self.tlo, (0, 0))
        if self.obiekt_z_menu:
            for e in self.wieze_ataku:
                e.wydzielenie_obszaru(self.okno)
                e.rysuj(self.okno)
            for e in self.totemy:
                e.wydzielenie_obszaru(self.okno)
                e.rysuj(self.okno)
            self.obiekt_z_menu.wydzielenie_obszaru(self.okno)
        #rysowanie wrogów
        for e in self.wrogowie:
            e.rysuj(self.okno)
        #rysowanie wiez ataku
        for e in self.wieze_ataku:
            e.rysuj(self.okno)
        for e in self.totemy:
            e.rysuj(self.okno)

        if self.obiekt_z_menu:
            self.obiekt_z_menu.rysuj(self.okno)

        #rysowanie pauzy
        self.pauza_przycisk.rysuj(self.okno)
        #rysowanie menu
        self.menu.rysuj(self.okno)

        #runda
        tekst = self.menu_font.render("Runda " + str(self.runda), True, (255, 255, 255))
        runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (20+tekst.get_width(), 70))
        self.okno.blit(runda_tlo, (10, 10))
        self.okno.blit(tekst, (20, 15))
        odl_pom = 10 + runda_tlo.get_width() + 10

        #zycia
        tekst = self.zycie_konto_font.render(str(self.zycia), True, (255, 255, 255))
        zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (80+tekst.get_width(), 70))
        self.okno.blit(zycie_tlo, (odl_pom, 10))
        self.okno.blit(zycie_ikona, (odl_pom, 14))
        self.okno.blit(tekst, (odl_pom + zycie_ikona.get_width(), 8))

        #stan konta
        odl_pom += zycie_tlo.get_width() + 10
        tekst = self.zycie_konto_font.render(str(self.stan_konta), True, (255, 255, 255))
        konto_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (80+tekst.get_width(), 70))
        self.okno.blit(konto_tlo, (odl_pom, 10))
        self.okno.blit(konto_ikona, (odl_pom, 14))
        self.okno.blit(tekst, (odl_pom + konto_ikona.get_width(), 8))

        pygame.display.update()

    def dodaj_wieze(self, nazwa):
        x,y = pygame.mouse.get_pos()
        dostepne_obiekty = [WiezaAtaku(x, y), WiezaAtaku_2(x, y), TotemObrazenia(x, y), TotemZasieg(x, y)]
        temp = dostepne_obiekty[lista_obiektow.index(nazwa)]
        self.obiekt_z_menu = temp

    def bliskosc_do_sciezki(self, przenoszona_wieza):
        bliskie_elementy = []
        for p in sciezka_n:
            odleglosc = math.sqrt((przenoszona_wieza.x - p[0]) ** 2 + (przenoszona_wieza.y - p[1]) ** 2)
            bliskie_elementy.append([odleglosc, p]) #wybieranie 2 punktów które są blisko wiezy

        bliskie_elementy.sort(key=lambda o: o[0])
        n_punkt_1 = bliskie_elementy[0][1]
        n_punkt_2 = bliskie_elementy[1][1] #wybór najbliższych punktów

        up = abs((n_punkt_2[0]-n_punkt_1[0]) * (n_punkt_1[1] - przenoszona_wieza.y) - (n_punkt_1[0] - przenoszona_wieza.x) * (n_punkt_2[1] - n_punkt_1[1]))
        down = math.sqrt((n_punkt_2[0]-n_punkt_1[0])**2 +(n_punkt_2[1]-n_punkt_1[1])**2 )
        odleglosc = up/down
        print(odleglosc)
        if(odleglosc<20):
            przenoszona_wieza.kolor_wiezy = (255, 14, 12, 100)
            return False
        else:
            przenoszona_wieza.kolor_wiezy = (14, 255, 12, 100)
            return True

main = Main()
main.dzialanie()