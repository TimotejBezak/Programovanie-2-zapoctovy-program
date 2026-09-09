from position import Pos
from konstanty import *
import pygame
import copy

class Zobrazovac:
    def __init__(self):
        self.scale = 1.0
        self.offset = Pos(0,0) #offset obrazovky od defaultnej pozicie
        self.stred_obrazovky = Pos(SIRKA_OBRAZOVKY//2, VYSKA_OBRAZOVKY//2)
        self.dragujem = False

    def transform(self, image, pos):
        offset_od_stredu_obrazovky = pos - self.stred_obrazovky
        offset_od_posunuteho_stredu_obrazovky = pos - (self.stred_obrazovky + self.offset)
        pozicia_na_obrazovke_od_stredu = offset_od_posunuteho_stredu_obrazovky * self.scale
        pozicia_na_obrazovke_od_laveho_horneho_rohu = self.stred_obrazovky + pozicia_na_obrazovke_od_stredu
        scaled_image = pygame.transform.scale( image, (int(image.get_width() * self.scale * 1/5), int(image.get_height() * self.scale * 1/5)) )
        return (scaled_image, pozicia_na_obrazovke_od_laveho_horneho_rohu)

    def inverzny_transform(self, pos): # potrebujem to na poziciu myse, aby som vedel kde naozaj ukazuje
        # pos = self.stred_obrazovky + (ret - (self.stred_obrazovky + self.offset)) * self.scale
        # (pos - self.stred_obrazovky)/self.scale = ret - (self.stred_obrazovky + self.offset)
        # (pos - self.stred_obrazovky)/self.scale + self.stred_obrazovky + self.offset = ret
        return (pos - self.stred_obrazovky)/self.scale + self.stred_obrazovky + self.offset

    def nechat(self, image, pos):
        return (pygame.transform.scale( image, (int(image.get_width() * 1/5), int(image.get_height() * 1/5)) ), pos)

    def zoomovat(self, posun):
        self.scale *= posun

    def drag_posun_update(self):
        mys_pos = Pos(*pygame.mouse.get_pos())
        if not self.dragujem and pygame.mouse.get_pressed()[1]:
            print("start")
            self.dragujem = True
            self.offset_start = self.offset + Pos(0,0) # kopia
            self.mys_pos_start = mys_pos
        if not pygame.mouse.get_pressed()[1]:
            self.dragujem = False
        if self.dragujem:
            self.offset = self.offset_start - (mys_pos - self.mys_pos_start) / self.scale