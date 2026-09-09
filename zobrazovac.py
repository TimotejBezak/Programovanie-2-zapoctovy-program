from position import Pos
from konstanty import *
import pygame
import copy

class Zobrazovac:
    def __init__(self):
        self.scale = 1.0 # kolkonasobne viac bude vidiet obrazovka
        self.offset = Pos(0,0) #offset obrazovky od defaultnej pozicie
        self.stred_obrazovky = Pos(SIRKA_OBRAZOVKY//2, VYSKA_OBRAZOVKY//2)
        self.dragujem = False

    def transform(self, image, pos): # ze kde mam zobrazit obrazok, aby to prisluchalo situacii, ze obrazovka je posunuta o self.offset a zoomnuta o self.scale
        offset_od_stredu_obrazovky = pos - self.stred_obrazovky
        offset_od_posunuteho_stredu_obrazovky = pos - (self.stred_obrazovky + self.offset)
        pozicia_na_obrazovke_od_stredu = offset_od_posunuteho_stredu_obrazovky * self.scale
        pozicia_na_obrazovke_od_laveho_horneho_rohu = self.stred_obrazovky + pozicia_na_obrazovke_od_stredu
        scaled_image = pygame.transform.scale( image, (int(image.get_width() * self.scale * OBRAZOK_SCALE_OFFSET), int(image.get_height() * self.scale * OBRAZOK_SCALE_OFFSET)) )
        return (scaled_image, pozicia_na_obrazovke_od_laveho_horneho_rohu)

    def inverzny_transform(self, pos): # ze pre danu poziciu na obrazovke chcem zistit, akej realnej pozicii prislucha
        return (pos - self.stred_obrazovky)/self.scale + self.stred_obrazovky + self.offset

    def nechat(self, image, pos): # zobrazim obrazok na poziciu relativne k lavemu horneme rohu obrazovky
        return (pygame.transform.scale( image, (int(image.get_width() * OBRAZOK_SCALE_OFFSET), int(image.get_height() * OBRAZOK_SCALE_OFFSET)) ), pos)

    def zoomovat(self, posun):
        self.scale *= posun

    def drag_posun_update(self): # posuvanie tahanim mysou
        mys_pos = Pos(*pygame.mouse.get_pos())
        if not self.dragujem and pygame.mouse.get_pressed()[1]:
            self.dragujem = True
            self.offset_start = self.offset
            self.mys_pos_start = mys_pos
        if not pygame.mouse.get_pressed()[1]:
            self.dragujem = False
        if self.dragujem:
            self.offset = self.offset_start - (mys_pos - self.mys_pos_start) / self.scale