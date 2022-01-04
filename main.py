import pygame
import os
from enemies.cyber import Cyber
from towers.attackTower import AttackTower
class Main:
    def __init__(self):
        self.szerokosc = 1200
        self.wysokosc = 800
        self.okno = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        self.tlo = pygame.image.load(os.path.join("resources", "map.png"))
        self.tlo = pygame.transform.scale(self.tlo, (self.szerokosc, self.wysokosc))
        self.wrogowie = [Cyber()]
        self.wieze_ataku=[AttackTower(100, 150)]

    def dzialanie(self):
        dzialanie = True
        zegar = pygame.time.Clock()
        while dzialanie:
            zegar.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    dzialanie = False

            wrogowie_poza_mapa = []
            for e in self.wrogowie:
                if e.x<-20:
                    wrogowie_poza_mapa.append(e)
            for e in wrogowie_poza_mapa:
                self.wrogowie.remove(e)
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