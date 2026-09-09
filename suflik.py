from konstanty import *
import math
import pygame
from position import Pos
from plocha import Plocha
import random

class Suflik(Plocha):
    def __init__(self, komponenty, pos):
        self.komponenty = komponenty # dieliky co tu su
        self.pos = pos # pozicia na obrazovke
        self.prelozit_na_plochu = []

        random.shuffle(self.komponenty) # zamiesam dieliky nech nie su v takom poradi, ze pasujuce su vedla seba
        self.pozicie_update()
        self.mys_stlacena_minule = False

    def update(self, realna_pozicia_transform): # volame kazdy frame
        self.drag_update(Pos(*pygame.mouse.get_pos())) # update dragovania dielikov, zdedene od Plocha

        for kom in self.komponenty:
            if kom.bol_prave_polozeny(): # detekcia presunu na skladaciu plochu
                if kom.pos.y < VYSKA_ZACIATKU_SUFLIKU:
                    self.prelozit_na_plochu.append(kom)
                    self.komponenty.remove(kom)
                    kom.pos = realna_pozicia_transform(kom.pos)
                else: # polozeny dielik zaradim na koniec
                    self.komponenty.remove(kom)
                    self.komponenty.append(kom)
                self.pozicie_update()

    def posuvanie_update(self, posun): # volame kazdy frame, posun je mnozstvo potocenia mysou, o tolko sa posunie celkova pozicia
        if posun != 0:
            self.pos.x += posun*RYCHLOST_POSUVANIA_SUFLIKU
            self.pozicie_update()

    def prelozit_na_plochu_komponenty(self): # vrati vsetky komponenty od posledneho volania tejto funkcie, ktore chceme prelozit na skladaciu plochu
        ret = self.prelozit_na_plochu
        self.prelozit_na_plochu = []
        return ret

    def pozicie_update(self): # vyrata vsetkym komponentam poziciu prisluchajucu ich poradiu v self.komponenty, v poradi zlava doprarva zhora dole
        pocet_v_riadku = math.ceil(len(self.komponenty) / POCET_RIADKOV_SUFLIKA)
        for idx, kom in enumerate(self.komponenty):
            riadok = idx // pocet_v_riadku
            stlpec = idx % pocet_v_riadku
            sirka_dielika = kom.dlzka_strany_dielika()
            rozostup = sirka_dielika + MEDZERY_DIELIKOV_V_SUFLIKU
            kom.pos = Pos(self.pos.x + stlpec * rozostup + MEDZERY_DIELIKOV_V_SUFLIKU, self.pos.y + riadok * rozostup + MEDZERY_DIELIKOV_V_SUFLIKU)

    def pridaj_komponentu(self, komponenta): # prida komponentu
        self.komponenty.append(komponenta)
        self.pozicie_update()

    def zobraz(self): #zobrazi vsetky dieliky na spravne pozicie
        ret = []
        for kom in reversed(self.komponenty):
            for d in kom.pozicie_dielikov_pre_kreslenie():
                ret.append((*d, 2))
        return ret