class Tower:
    def __init__(self,X,Y):
        self.x=X
        self.y=Y
        self.szerokosc=0
        self.wysokosc=0
        self.poziom = 0
        self.klatki = []
        self.obrazenia = 1
        self.place_color = (0,0,255,100)

    def rysuj(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        img= self.klatki[self.poziom]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2,))



