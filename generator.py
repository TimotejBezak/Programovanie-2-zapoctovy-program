import pygame
from komponenta import Komponenta
from position import Pos
import random
from konstanty import *
from dielik import Dielik
from funkcie_navyse import circle_through_points
import math

def sekame_obrazok(obrazok, sirka_pocet, vyska_pocet):#kolko dielikov je to na sirku a kolko na vysku
    obrazok = pygame.transform.scale( obrazok, (SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * POCET_DIELIKOV_NA_SIRKU_OBRAZKA, SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * POCET_DIELIKOV_NA_SIRKU_OBRAZKA))
    sirka = obrazok.get_width() // sirka_pocet #pozor na nedelitelnost, neviem mozno by som si mohol dat na to pozor aby to bolo proste delitelne
    vyska = obrazok.get_height() // vyska_pocet
    obrazky = [[pygame.Surface((sirka + 2*DIELIK_ANCHOR_POSITION_OBRAZOK, vyska + 2*DIELIK_ANCHOR_POSITION_OBRAZOK), pygame.SRCALPHA) for _ in range(sirka_pocet)] for _ in range(vyska_pocet)]
    for i in range(obrazok.get_width()):
        for j in range(obrazok.get_height()):
            s,r = i//sirka, j//vyska
            obrazky[r][s].set_at((i%sirka + DIELIK_ANCHOR_POSITION_OBRAZOK, j%vyska + DIELIK_ANCHOR_POSITION_OBRAZOK), obrazok.get_at((i, j)))
    return obrazky

def generujeme_dieliky(obrazky):
    ret = []
    for i in range(len(obrazky)):
        for j in range(len(obrazky[0])):
            ret.append(Komponenta([Dielik(obrazky[i][j], Pos(0,0), Pos(j, i))], Pos(random.randint(0,SIRKA_OBRAZOVKY-1),random.randint(0,VYSKA_ZACIATKU_SUFLIKU-1)), random.randint(0,3)))
    return ret

def generuj(obrazok, sirka_pocet, vyska_pocet):
    obrazky = sekame_obrazok(obrazok, sirka_pocet, vyska_pocet)
    vylepsi_hrany(obrazky)
    return generujeme_dieliky(obrazky)


def vylepsi_hrany(obrazky):
    smery = [Pos(-1,0), Pos(0,-1)]
    vyska_pocet = len(obrazky)
    sirka_pocet = len(obrazky[0])
    for y in range(len(obrazky)):
        for x in range(len(obrazky[0])):
            for smer in smery:
                pos_teraz = Pos(x, y)
                pos_sused = pos_teraz + smer
                if 0 <= pos_sused.x < sirka_pocet and 0 <= pos_sused.y < vyska_pocet:
                    vylepsi_hranu(obrazky[y][x], obrazky[pos_sused.y][pos_sused.x], smer)

def vylepsi_hranu(obrazok1, obrazok2, smer): # smer je ze ktorym smerom je obrazok2 od obrazku1
    pixels1 = pygame.PixelArray(obrazok1)
    pixels2 = pygame.PixelArray(obrazok2)

    sirka = obrazok1.get_width()-2*DIELIK_ANCHOR_POSITION_OBRAZOK
    hrana = Hrana_medzi(sirka)
    if smer == Pos(0, -1):
        for x in range(sirka):
            kde_ma_byt_obrazok = hrana.funkcia_hrany(x)
            for i in range(0, DIELIK_ANCHOR_POSITION_OBRAZOK):
                if kde_ma_byt_obrazok[i] == True:
                    pos = (x+DIELIK_ANCHOR_POSITION_OBRAZOK, sirka+DIELIK_ANCHOR_POSITION_OBRAZOK-i-1)
                    farba = obrazok2.get_at(pos)
                    pixels2[*pos] = (0,0,0,0) # nastavit na priesvitne
                    pixels1[*(x+DIELIK_ANCHOR_POSITION_OBRAZOK, DIELIK_ANCHOR_POSITION_OBRAZOK-i-1)] = farba

            for i in range(-DIELIK_ANCHOR_POSITION_OBRAZOK+1, 1):
                if kde_ma_byt_obrazok[i] == False:
                    i = abs(i)
                    pos = (x+DIELIK_ANCHOR_POSITION_OBRAZOK, DIELIK_ANCHOR_POSITION_OBRAZOK+i)
                    farba = obrazok1.get_at(pos)
                    pixels1[*pos] = (0,0,0,0) # nastavit na priesvitne
                    pixels2[*(x+DIELIK_ANCHOR_POSITION_OBRAZOK, sirka+DIELIK_ANCHOR_POSITION_OBRAZOK+i)] = farba
    else:
        for x in range(sirka):
            kde_ma_byt_obrazok = hrana.funkcia_hrany(x)
            for i in range(0, DIELIK_ANCHOR_POSITION_OBRAZOK):
                if kde_ma_byt_obrazok[i] == True:
                    pos = (sirka+DIELIK_ANCHOR_POSITION_OBRAZOK-i-1, x+DIELIK_ANCHOR_POSITION_OBRAZOK)
                    farba = obrazok2.get_at(pos)
                    pixels2[*pos] = (0,0,0,0) # nastavit na priesvitne
                    pixels1[*(DIELIK_ANCHOR_POSITION_OBRAZOK-i-1, x+DIELIK_ANCHOR_POSITION_OBRAZOK)] = farba

            for i in range(-DIELIK_ANCHOR_POSITION_OBRAZOK+1, 1):
                if kde_ma_byt_obrazok[i] == False:
                    i = abs(i)
                    pos = (DIELIK_ANCHOR_POSITION_OBRAZOK+i, x+DIELIK_ANCHOR_POSITION_OBRAZOK)
                    farba = obrazok1.get_at(pos)
                    pixels1[*pos] = (0,0,0,0) # nastavit na priesvitne
                    pixels2[*(sirka+DIELIK_ANCHOR_POSITION_OBRAZOK+i, x+DIELIK_ANCHOR_POSITION_OBRAZOK)] = farba

    del pixels1
    del pixels2

class Hrana_medzi:
    MIN_DLZKA_MEDZI_KONCAMI = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * 20*2/250)
    MAX_DLZKA_MEDZI_KONCAMI = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * 40*2/250)
    MIN_VYSKA_KONCA = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * (-9*2/250))
    MAX_VYSKA_KONCA = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * 9*2/250)
    MIN_RADIUS = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * 17*2/250)
    MAX_RADIUS = int(SIRKA_STRANY_DIELIKU_PRE_OBRAZOK * 27*2/250)
    def __init__(self, dlzka):
        self.dlzka = dlzka
        self.koniec1 = random.randint(dlzka//2-self.MAX_DLZKA_MEDZI_KONCAMI//2, dlzka//2-self.MIN_DLZKA_MEDZI_KONCAMI//2)
        self.koniec2 = random.randint(dlzka//2+self.MIN_DLZKA_MEDZI_KONCAMI//2, dlzka//2+self.MAX_DLZKA_MEDZI_KONCAMI//2)
        self.vyska1 = random.randint(self.MIN_VYSKA_KONCA, self.MAX_VYSKA_KONCA)
        self.vyska2 = random.randint(self.MIN_VYSKA_KONCA, self.MAX_VYSKA_KONCA)
        self.radius = random.randint(self.MIN_RADIUS, self.MAX_RADIUS)
        self.ci_otocim_funkciu = random.randint(0,1)
        if self.ci_otocim_funkciu == 0:
            self.ci_otocim_funkciu = -1

    def funkcia_hrany(self, x): # zaciatok je v [0,0], koniec v [dlzka, 0], vracia slovnik boolov, ci na danom offsete je alebo nie je obrazok
        k,l,m = circle_through_points((self.koniec1, self.vyska1), (self.koniec2, self.vyska2), self.radius) # x^2 + xk + y^2 + ly = m  # y^2 + ly + x^2 + xk - m = 0  # y = (-l +- sqrt(l^2-4*(x^2 + xk - m)))/2
        ret = {}
        for i in range(-DIELIK_ANCHOR_POSITION_OBRAZOK, DIELIK_ANCHOR_POSITION_OBRAZOK+1):
            ret[i] = (i < 0)
        if x < self.koniec1:
            vyska_teraz = int(self.vyska1 * x/self.koniec1)
            self.pridaj_interval(ret, min(0, vyska_teraz), max(0, vyska_teraz), self.vyska1 >= 0)
        if x > self.koniec2:
            vyska_teraz = int(self.vyska2 * (self.dlzka - x)/(self.dlzka - self.koniec2))
            self.pridaj_interval(ret, min(0, vyska_teraz), max(0, vyska_teraz), self.vyska2 >= 0)
        if self.koniec1 <= x <= self.koniec2:
            vyska_teraz = int(self.vyska1 + (x-self.koniec1)/(self.koniec2-self.koniec1) * (self.vyska2-self.vyska1))
            self.pridaj_interval(ret, min(0, vyska_teraz), max(0, vyska_teraz), True)
        determinant = l**2-4*(x**2 + x*k - m)
        if determinant > 0:
            y1 = int((-l + math.sqrt(determinant))/2)
            y2 = int((-l - math.sqrt(determinant))/2)
            self.pridaj_interval(ret, min(y1, y2), max(y1, y2), True)
        if self.ci_otocim_funkciu:
            ret = self.naopak(ret)
        return ret

    def pridaj_interval(self, slovnik, z, k, hodnota):
        for i in range(z, k+1):
            slovnik[i] = hodnota

    def naopak(self, slovnik):
        ret = {}
        for i in range(-DIELIK_ANCHOR_POSITION_OBRAZOK, DIELIK_ANCHOR_POSITION_OBRAZOK+1):
            ret[i] = not slovnik[-i]
        return ret

# bugs - priesvitne vecicky trosku pod dielikmi

# oukej TODO list:
# dokumentacia, mozno nejake skraslenie, povymazavanie nepotrebneho...
# odovzdanie