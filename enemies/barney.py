from .enemy import Enemy
import os
import pygame


klatki = []

for x in range(20):
    pom = str(x)
    if x < 10:
        pom = "0" + pom
    klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/enemies/barney", pom + ".png")),
        (64, 64)))


class Barney(Enemy):

    def __init__(self):
        super().__init__()
        self.nazwa = "barney"
        self.klatki = klatki[:]
        self.maksymalne_zdrowie = 3
        self.aktualne_zdrowie = self.maksymalne_zdrowie
        self.predkosc = 4
        self.stan_konta=200

