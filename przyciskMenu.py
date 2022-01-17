from menu import Przycisk


class PrzyciskMenu(Przycisk):
    def __init__(self, x, y, img, nazwa, koszt):
        self.nazwa = nazwa
        self.img = img
        self.szerokosc = self.img.get_width()
        self.wysokosc = self.img.get_height()
        self.x = x
        self.y = y
        self.koszt = koszt
