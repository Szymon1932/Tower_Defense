from .enemy import Enemy
import os
import pygame


klatki = []

for x in range(20):
    pom = str(x)
    if x < 10:
        pom = "0" + pom
    klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/enemies/ted", pom + ".png")),
        (64, 64)))


class Ted(Enemy):

    def __init__(self):
        super().__init__()
        self.nazwa = "ted"
        self.klatki = klatki[:]
        self.maksymalne_zdrowie = 5
        self.aktualne_zdrowie = self.maksymalne_zdrowie
        self.predkosc = 10
        self.stan_konta=1

