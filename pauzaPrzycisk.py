from przycisk import Przycisk

class PauzaPrzycisk(Przycisk):
    def __init__(self,przycisk_play,przycisk_pauza,x,y):
        self.x = x
        self.y = y
        self.img = przycisk_play
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.przycisk_play = przycisk_play
        self.przycisk_pauza = przycisk_pauza
        self.pauza=False

    def rysuj(self, okno):
        if self.pauza:
            okno.blit(self.przycisk_pauza, (self.x, self.y))
        else:
            okno.blit(self.przycisk_play, (self.x, self.y))
