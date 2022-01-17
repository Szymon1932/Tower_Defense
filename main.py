import pygame
import os
from enemies.cyber import Cyber
from enemies.marshall import Marshall
from enemies.barney import Barney
from enemies.ted import Ted
from towers.wiezaAtaku import WiezaAtaku
from towers.wiezaAtaku import WiezaAtaku_2
from menuGry import MenuGry
from pauzaPrzycisk import PauzaPrzycisk
import time
import random
from towers.totemZasieg import TotemZasieg
from towers.totemObrazenia import TotemObrazenia
import math

pygame.init()
pygame.font.init()

pygame.mixer.music.load(os.path.join("resources", "music.mp3"))
# Sound from Zapsplat.com
# Imgs from https://craftpix.net/
przycisk_play = pygame.transform.scale(pygame.image.load(os.path.join("resources", "play.png")), (80, 80))
przycisk_pauza = pygame.transform.scale(pygame.image.load(os.path.join("resources", "pause.png")), (80, 80))
restart_przycisk = pygame.transform.scale(pygame.image.load(os.path.join("resources", "reload.png")), (80, 80))
wyjscie_przycisk = pygame.transform.scale(pygame.image.load(os.path.join("resources", "remove.png")), (80, 80))
dzwiek_przycisk_on = pygame.transform.scale(pygame.image.load(os.path.join("resources", "button_sound.png")), (80, 80))
dzwiek_przycisk_off = pygame.transform.scale(pygame.image.load(os.path.join("resources", "button_sound_off.png")),
                                             (80, 80))
obraz_menu = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")), (720, 180))
konto_ikona = pygame.transform.scale(pygame.image.load(os.path.join("resources", "star.png")), (60, 60))
zycie_ikona = pygame.transform.scale(pygame.image.load(os.path.join("resources", "heart.png")), (64, 64))


class Main:
    def __init__(self):
        self.nazwa_wieze_ataku = ["wieza_ataku", "wieza_ataku_2"]
        self.nazwa_totemy = ["totem_obrazenia", "totem_zasieg"]
        self.rundy = [
            [10, 0, 0, 0],
            [5, 5, 3, 0],
            [6, 5, 3, 0],
            [10, 10, 5, 5]
        ]
        self.font_wielkosc = 40
        self.font_ikony = 50
        self.stan_konta_pocz = 6000
        self.zdrowie_pocz = 5
        self.lista_obiektow = ["wieza_ataku", "wieza_ataku_2", "totem_obrazenia", "totem_zasieg"]
        self.szerokosc = 1200
        self.wysokosc = 800
        self.okno = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        self.tlo = pygame.image.load(os.path.join("resources", "map.png"))
        self.tlo = pygame.transform.scale(self.tlo, (self.szerokosc, self.wysokosc))
        self.wrogowie = []
        self.wieze_ataku = []
        self.totemy = []
        self.wybrana_wieza = None
        self.stan_konta = self.stan_konta_pocz
        self.pauza_przycisk = PauzaPrzycisk(przycisk_play, przycisk_pauza,
                                            self.szerokosc - przycisk_play.get_width() - 15, 15)
        self.restart_przycisk = PauzaPrzycisk(restart_przycisk, restart_przycisk,
                                              self.szerokosc - restart_przycisk.get_width() - 15,
                                              restart_przycisk.get_height() + 30)
        self.wyjscie_przycisk = PauzaPrzycisk(wyjscie_przycisk, wyjscie_przycisk,
                                              self.szerokosc - wyjscie_przycisk.get_width() - 15,
                                              wyjscie_przycisk.get_height() + restart_przycisk.get_height() + 45)
        self.dzwiek_przycisk = PauzaPrzycisk(dzwiek_przycisk_on, dzwiek_przycisk_off,
                                             self.szerokosc - dzwiek_przycisk_on.get_width() - 15,
                                             wyjscie_przycisk.get_height() + restart_przycisk.get_height() + dzwiek_przycisk_on.get_height() + 60)
        self.pauza = True
        self.pauza_przycisk.pauza = self.pauza
        self.runda = 0
        self.obecna_runda = self.rundy[self.runda][:]
        self.czas = time.time()
        self.zycia = self.zdrowie_pocz
        self.menu = MenuGry(obraz_menu.get_width() / 2 + 25, 675, obraz_menu)
        self.menu.dodaj_nastepny_przycisk(
            pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_1.png")), (90, 90)),
            "wieza_ataku", 1500)
        self.menu.dodaj_nastepny_przycisk(
            pygame.transform.scale(pygame.image.load(os.path.join("resources", "tower_attack_2.png")), (90, 90)),
            "wieza_ataku_2", 2000)
        self.menu.dodaj_nastepny_przycisk(
            pygame.transform.scale(pygame.image.load(os.path.join("resources", "attack_totem.png")), (90, 90)),
            "totem_obrazenia", 1200)
        self.menu.dodaj_nastepny_przycisk(
            pygame.transform.scale(pygame.image.load(os.path.join("resources", "range_totem.png")), (90, 90)),
            "totem_zasieg", 1000)
        self.obiekt_z_menu = None
        self.menu_font = pygame.font.SysFont("comicsans", self.font_wielkosc)
        self.zycie_konto_font = pygame.font.SysFont("comicsans", self.font_ikony)
        self.czy_restart = False
        self.dzialanie_wyjscie = False
        self.muzyka_wyl = False
        self.czy_wygrana = False
        self.czy_przegrana = False

    def stworzenie_wrogow(self):

        if sum(self.obecna_runda) == 0:
            if len(self.wrogowie) == 0:
                self.runda += 1
                if self.runda < len(self.rundy):
                    self.obecna_runda = self.rundy[self.runda]

        else:
            obecni_wrogowie = [Cyber(), Barney(), Marshall(), Ted()]
            for e in range(len(self.obecna_runda)):
                if self.obecna_runda[e] != 0:
                    self.wrogowie.append(obecni_wrogowie[e])
                    self.obecna_runda[e] = self.obecna_runda[e] - 1
                    break

    def dzialanie(self):
        pygame.mixer.music.play(1)
        dzialanie = True
        zegar = pygame.time.Clock()
        while dzialanie:

            zegar.tick(60)
            if self.pauza == False:
                if time.time() - self.czas >= random.randrange(1,
                                                               14) / 5:  # generowanie stworów co okreslony losowy czas
                    self.czas = time.time()
                    self.stworzenie_wrogow()

            pos = pygame.mouse.get_pos()
            if self.zycia > 0 and self.runda >= len(self.rundy):
                self.czy_wygrana = True
            elif self.zycia <= 0:
                self.czy_przegrana = True
            else:
                self.czy_wygrana = False
                self.czy_przegrana = False

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

                    if self.restart_przycisk.czy_wcisniete(pos[0], pos[1]):
                        self.reset()
                    if self.wyjscie_przycisk.czy_wcisniete(pos[0], pos[1]):
                        self.dzialanie_wyjscie = True
                    if self.obiekt_z_menu:
                        self.bliskosc_do_sciezki(self.obiekt_z_menu)
                        czy_postawic_obiekt = True
                        wieze = self.wieze_ataku[:]
                        wieze += self.totemy[:]
                        for w in wieze:
                            if w.kolizja(self.obiekt_z_menu):
                                czy_postawic_obiekt = False

                        if czy_postawic_obiekt and self.bliskosc_do_sciezki(self.obiekt_z_menu):
                            if self.obiekt_z_menu.nazwa in self.nazwa_wieze_ataku:
                                self.wieze_ataku.append(self.obiekt_z_menu)
                            elif self.obiekt_z_menu.nazwa in self.nazwa_totemy:
                                self.totemy.append(self.obiekt_z_menu)
                            self.obiekt_z_menu = None

                    else:
                        if self.dzwiek_przycisk.czy_wcisniete(pos[0], pos[1]):

                            self.muzyka_wyl = not (self.muzyka_wyl)
                            self.dzwiek_przycisk.pauza = self.muzyka_wyl
                            if self.muzyka_wyl:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()
                        if self.pauza_przycisk.czy_wcisniete(pos[0], pos[1]):
                            self.pauza = not (self.pauza)
                            self.pauza_przycisk.pauza = self.pauza
                        ikonka_menu = self.menu.wcisniecie_ikony(pos[0], pos[1])
                        if ikonka_menu:
                            cost = self.menu.pobierz_wartosc_obiektu(ikonka_menu)
                            if self.stan_konta >= cost:
                                self.stan_konta -= cost
                                self.dodaj_wieze(ikonka_menu)

                        wybrany_element = None
                        if self.wybrana_wieza:  # wybrano wieze
                            wybrany_element = self.wybrana_wieza.menu.wcisniecie_przyciskow_w_menu(pos[0], pos[1])
                            if wybrany_element:
                                if wybrany_element == 'Ulepsz':
                                    koszt = self.wybrana_wieza.wartosc_ulepszenia()
                                    if self.stan_konta >= koszt:
                                        self.stan_konta -= koszt
                                        self.wybrana_wieza.ulepsz()

                        if wybrany_element == None:
                            # czy kliknięto w wieze ataku
                            for wieza in self.wieze_ataku:
                                if wieza.czy_wcisniete(pos[0], pos[1]):
                                    wieza.czy_wybrano = True
                                    self.wybrana_wieza = wieza
                                else:
                                    wieza.czy_wybrano = False
                            # czy kliknięto na totem
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
                    if e.x < -15:
                        wrogowie_poza_mapa.append(e)
                        self.zycia -= 1
                for e in wrogowie_poza_mapa:
                    self.wrogowie.remove(e)

                for wieza in self.wieze_ataku:
                    self.stan_konta += wieza.atakuj(self.wrogowie)

                for tw in self.totemy:
                    tw.dodaj_efekt(self.wieze_ataku)

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
        # rysowanie wrogów
        for e in self.wrogowie:
            e.rysuj(self.okno)
        # rysowanie wiez ataku
        for e in self.wieze_ataku:
            e.rysuj(self.okno)
        for e in self.totemy:
            e.rysuj(self.okno)

        if self.obiekt_z_menu:
            self.obiekt_z_menu.rysuj(self.okno)

        # rysowanie pauzy
        self.pauza_przycisk.rysuj(self.okno)

        self.restart_przycisk.rysuj(self.okno)

        self.wyjscie_przycisk.rysuj(self.okno)

        self.dzwiek_przycisk.rysuj(self.okno)
        # rysowanie menu
        self.menu.rysuj(self.okno)

        # runda

        if self.czy_wygrana:
            tekst = self.menu_font.render("Wygrana", True, (255, 255, 255))
            runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (20 + tekst.get_width(), 70))
            # zycia
            tekst2 = self.zycie_konto_font.render(str(self.zycia), True, (255, 255, 255))
            zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (80 + tekst2.get_width(), 70))
        elif self.czy_przegrana:
            tekst = self.menu_font.render("Przegrana", True, (255, 255, 255))
            runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (20 + tekst.get_width(), 70))

            tekst2 = self.zycie_konto_font.render(str(self.zycia), True, (255, 255, 255))
            zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (80 + tekst2.get_width(), 70))
        elif self.dzialanie_wyjscie:
            tekst = self.menu_font.render("Koniec", True, (255, 255, 255))
            runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (20 + tekst.get_width(), 70))

            tekst2 = self.zycie_konto_font.render(str(self.zycia), True, (255, 255, 255))
            zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (80 + tekst2.get_width(), 70))
        else:
            tekst = self.menu_font.render("Runda " + str(self.runda), True, (255, 255, 255))
            runda_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (20 + tekst.get_width(), 70))

            # zycia
            tekst2 = self.zycie_konto_font.render(str(self.zycia), True, (255, 255, 255))
            zycie_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                               (80 + tekst2.get_width(), 70))

        odl_pom = 10 + runda_tlo.get_width() + 10
        self.okno.blit(runda_tlo, (10, 10))
        self.okno.blit(tekst, (14, 11))
        self.okno.blit(zycie_tlo, (odl_pom, 10))
        self.okno.blit(zycie_ikona, (odl_pom, 14))
        self.okno.blit(tekst2, (odl_pom + zycie_ikona.get_width(), 8))
        # stan konta
        odl_pom += zycie_tlo.get_width() + 10
        tekst3 = self.zycie_konto_font.render(str(self.stan_konta), True, (255, 255, 255))
        konto_tlo = pygame.transform.scale(pygame.image.load(os.path.join("resources", "menu.png")),
                                           (80 + tekst3.get_width(), 70))

        self.okno.blit(konto_tlo, (odl_pom, 10))
        self.okno.blit(konto_ikona, (odl_pom, 14))
        self.okno.blit(tekst3, (odl_pom + konto_ikona.get_width(), 8))
        pygame.display.update()
        if self.czy_wygrana or self.czy_przegrana:
            time.sleep(3)
            self.reset()

        elif self.dzialanie_wyjscie:
            self.pauza = True
            self.pauza_przycisk.pauza = True
            time.sleep(2)
            exit(0)
        pygame.display.update()

    def dodaj_wieze(self, nazwa):
        x, y = pygame.mouse.get_pos()
        dostepne_obiekty = [WiezaAtaku(x, y), WiezaAtaku_2(x, y), TotemObrazenia(x, y), TotemZasieg(x, y)]
        temp = dostepne_obiekty[self.lista_obiektow.index(nazwa)]
        self.obiekt_z_menu = temp

    def bliskosc_do_sciezki(self, przenoszona_wieza):
        sciezka_n = [(11, 220), (100, 220), (200, 220), (309, 228), (308, 354), (400, 354), (500, 354), (600, 354),
                     (690, 354), (690, 254), (694, 146), (794, 146), (894, 146), (978, 147), (978, 247), (978, 347),
                     (978, 447), (978, 547), (979, 678), (814, 679), (814, 579), (807, 505), (707, 505), (607, 505),
                     (507, 505), (374, 502), (337, 480), (237, 480), (137, 480), (10, 479)]

        bliskie_elementy = []
        for p in sciezka_n:
            odleglosc = math.sqrt((przenoszona_wieza.x - p[0]) ** 2 + (przenoszona_wieza.y - p[1]) ** 2)
            bliskie_elementy.append([odleglosc, p])  # wybieranie 2 punktów które są blisko wiezy

        bliskie_elementy.sort(key=lambda o: o[0])
        n_punkt_1 = bliskie_elementy[0][1]
        n_punkt_2 = bliskie_elementy[1][1]  # wybór najbliższych punktów

        up = abs((n_punkt_2[0] - n_punkt_1[0]) * (n_punkt_1[1] - przenoszona_wieza.y) - (
                n_punkt_1[0] - przenoszona_wieza.x) * (n_punkt_2[1] - n_punkt_1[1]))
        down = math.sqrt((n_punkt_2[0] - n_punkt_1[0]) ** 2 + (n_punkt_2[1] - n_punkt_1[1]) ** 2)
        odleglosc = up / down
        if (odleglosc < 21):
            przenoszona_wieza.kolor_wiezy = (255, 14, 12, 100)
            return False
        else:
            przenoszona_wieza.kolor_wiezy = (14, 255, 12, 100)
            return True

    def reset(self):
        self.pauza = True
        self.pauza_przycisk.pauza = True

        self.stan_konta = self.stan_konta_pocz
        self.zycia = self.zdrowie_pocz
        self.runda = 0
        self.rundy = [
            [10, 0, 0, 0],
            [5, 5, 3, 0],
            [6, 5, 3, 0],
            [10, 10, 5, 5]
        ]
        self.obecna_runda = self.rundy[self.runda][:]
        self.wrogowie = []
        self.totemy = []
        self.wieze_ataku = []


main = Main()
main.dzialanie()
