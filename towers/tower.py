

class Tower:
    def __init__(self,X,Y):
        self.x=X
        self.y=Y
        self.szerokosc=0
        self.wysokosc=0
        self.poziom = 0
        self.klatki = []
        self.obrazenia = 1
        self.czy_wybrano = False

    def rysuj(self, win):
        img= self.klatki[self.poziom]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))


    def click(self, X, Y):
        obiekt = self.klatki[self.poziom]
        if  X >= self.x - obiekt.get_width() // 2 and X <= self.x - obiekt.get_width() // 2 + self.szerokosc:  #kiedy klik w obszarze wiezy
            if  Y >= self.y - obiekt.get_height() // 2 and Y <= self.y - obiekt.get_height() // 2 + self.wysokosc:
                return True
        return False

