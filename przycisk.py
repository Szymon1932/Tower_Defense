class Przycisk:
    def __init__(self, menu, img, nazwa):
        self.korekta_x = 60
        self.korekta_y = 90
        self.nazwa = nazwa
        self.img = img
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.x = menu.x - self.korekta_x
        self.y = menu.y - self.korekta_y
        self.menu = menu

    def czy_wcisniete(self, X, Y):
        if X <= self.x + self.szerokosc and X >= self.x:
            if Y <= self.y + self.wysokosc and Y >= self.y:
                return True
        return False

    def rysuj(self, okno):
        okno.blit(self.img, (self.x, self.y))

    def zmiana_pol(self):
        self.x = self.menu.x - self.korekta_x
        self.y = self.menu.y - self.korekta_y