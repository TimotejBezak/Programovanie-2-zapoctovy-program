from position import Pos
import pygame

class Dielik:
    def __init__(self, image, offset, vysledny_pos):
        self.image = image # proste obrazok
        self.offset = offset # offset od pozicie komponenty v ktorej je
        self.vysledny_pos = vysledny_pos # kam patri vramci celeho obrazku