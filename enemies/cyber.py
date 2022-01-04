from .enemy import Enemy
import os
import pygame


klatki = []

for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    klatki.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources/enemies/cyber", add_str + ".png")),
        (64, 64)))


class Cyber(Enemy):

    def __init__(self):
        super().__init__()
        self.nazwa = "cyber"
        self.klatki = klatki[:]
        self.maksymalne_zdrowie = 1
        self.zdrowie = self.maksymalne_zdrowie
        self.predkosc = 10

