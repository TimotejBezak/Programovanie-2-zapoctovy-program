from konstanty import *
import math
import pygame
from position import Pos
from plocha import Plocha
import random

class Suflik(Plocha):
    def __init__(self, komponenty, pos):
        self.komponenty = komponenty # dieliky co tu su
        self.pos = pos
        self.zoom = 1.0
        self.prelozit_na_plochu = []

        random.shuffle(self.komponenty)
        self.pozicie_update()
        self.mys_stlacena_minule = False

    def update(self, realna_pozicia_transform):
        self.drag_update(Pos(*pygame.mouse.get_pos()))

        for kom in self.komponenty:
            if kom.bol_prave_polozeny():
                if kom.pos.y < VYSKA_ZACIATKU_SUFLIKU:
                    self.prelozit_na_plochu.append(kom)
                    self.komponenty.remove(kom)
                    kom.pos = realna_pozicia_transform(kom.pos)
                else: # zaradim to na koniec
                    self.komponenty.remove(kom)
                    self.komponenty.append(kom)
                self.pozicie_update()

    def posuvanie_update(self, posun):
        if posun != 0:
            self.pos.x += posun*RYCHLOST_POSUVANIA_SUFLIKU
            self.pozicie_update()

    def prelozit_na_plochu_komponenty(self):
        ret = self.prelozit_na_plochu
        self.prelozit_na_plochu = []
        return ret

    def pozicie_update(self):
        pocet_v_riadku = math.ceil(len(self.komponenty) / POCET_RIADKOV_SUFLIKA)
        for idx, kom in enumerate(self.komponenty):
            riadok = idx // pocet_v_riadku
            stlpec = idx % pocet_v_riadku
            sirka_dielika = kom.dlzka_strany_dielika()
            rozostup = sirka_dielika + MEDZERY_DIELIKOV_V_SUFLIKU
            kom.pos = Pos(self.pos.x + stlpec * rozostup + MEDZERY_DIELIKOV_V_SUFLIKU, self.pos.y + riadok * rozostup + MEDZERY_DIELIKOV_V_SUFLIKU)

    def pridaj_komponentu(self, komponenta):
        self.komponenty.append(komponenta)
        self.pozicie_update()

    def zobraz(self): #zobrazi vsetky dieliky na spravne pozicie
        ret = []
        for kom in reversed(self.komponenty): # self.dieliky su v poradi, ze prvy ma byt navrchu
            for d in kom.pozicie_dielikov_pre_kreslenie():
                ret.append((*d, 2))
        return ret