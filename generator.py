import pygame
from komponenta import Komponenta
from position import Pos
import random
from konstanty import *
from dielik import Dielik
from funkcie_navyse import circle_through_points
import math

#PLAN POSTUPU K VITAZSTVU

def sekame_obrazok(obrazok, sirka_pocet, vyska_pocet):#kolko dielikov je to na sirku a kolko na vysku
    sirka = obrazok.get_width() // sirka_pocet #pozor na nedelitelnost, neviem mozno by som si mohol dat na to pozor aby to bolo proste delitelne
    vyska = obrazok.get_height() // vyska_pocet
    obrazky = [[pygame.Surface((sirka + 2*DIELIK_ANCHOR_POSITION, vyska + 2*DIELIK_ANCHOR_POSITION), pygame.SRCALPHA) for _ in range(sirka_pocet)] for _ in range(vyska_pocet)]
    for i in range(obrazok.get_width()):
        for j in range(obrazok.get_height()):
            s,r = i//sirka, j//vyska
            obrazky[r][s].set_at((i%sirka + DIELIK_ANCHOR_POSITION, j%vyska + DIELIK_ANCHOR_POSITION), obrazok.get_at((i, j)))
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
    sirka = obrazok1.get_width()-2*DIELIK_ANCHOR_POSITION
    hrana = Hrana_medzi(sirka)
    if smer == Pos(0, -1):
        for x in range(sirka):
            kde_ma_byt_obrazok = hrana.funkcia_hrany(x)
            for i in range(0, DIELIK_ANCHOR_POSITION):
                if kde_ma_byt_obrazok[i] == True:
                    pos = (x+DIELIK_ANCHOR_POSITION, sirka+DIELIK_ANCHOR_POSITION-i-1)
                    farba = obrazok2.get_at(pos)
                    obrazok2.set_at(pos, (0,0,0,0)) # nastavit na priesvitne
                    obrazok1.set_at((x+DIELIK_ANCHOR_POSITION, DIELIK_ANCHOR_POSITION-i-1), farba)

            for i in range(-DIELIK_ANCHOR_POSITION, 1):
                if kde_ma_byt_obrazok[i] == False:
                    i = abs(i)
                    pos = (x+DIELIK_ANCHOR_POSITION, DIELIK_ANCHOR_POSITION+i)
                    farba = obrazok1.get_at(pos)
                    obrazok1.set_at(pos, (0,0,0,0)) # nastavit na priesvitne
                    obrazok2.set_at((x+DIELIK_ANCHOR_POSITION, sirka+DIELIK_ANCHOR_POSITION+i), farba)
    else:
        for x in range(sirka):
            kde_ma_byt_obrazok = hrana.funkcia_hrany(x)
            for i in range(0, DIELIK_ANCHOR_POSITION):
                if kde_ma_byt_obrazok[i] == True:
                    pos = (sirka+DIELIK_ANCHOR_POSITION-i-1, x+DIELIK_ANCHOR_POSITION)
                    farba = obrazok2.get_at(pos)
                    obrazok2.set_at(pos, (0,0,0,0)) # nastavit na priesvitne
                    obrazok1.set_at((DIELIK_ANCHOR_POSITION-i-1, x+DIELIK_ANCHOR_POSITION), farba)

            for i in range(-DIELIK_ANCHOR_POSITION, 1):
                if kde_ma_byt_obrazok[i] == False:
                    i = abs(i)
                    pos = (DIELIK_ANCHOR_POSITION+i, x+DIELIK_ANCHOR_POSITION)
                    farba = obrazok1.get_at(pos)
                    obrazok1.set_at(pos, (0,0,0,0)) # nastavit na priesvitne
                    obrazok2.set_at((sirka+DIELIK_ANCHOR_POSITION+i, x+DIELIK_ANCHOR_POSITION), farba)

def funkcia_hrany_basic(x, dlzka): # zaciatok je v [0,0], koniec v [dlzka, 0], vracia int, lebo to ma byt pocet pixelov
    if x < dlzka/3:
        return int(x/(dlzka/3) * 5)
    if x > 2/3*dlzka:
        return int((dlzka-x)/(dlzka/3) * 5)
    return 15

class Hrana_medzi:
    MIN_DLZKA_MEDZI_KONCAMI = 20
    MAX_DLZKA_MEDZI_KONCAMI = 40
    MIN_VYSKA_KONCA = -9
    MAX_VYSKA_KONCA = 9
    MIN_RADIUS = 17
    MAX_RADIUS = 27
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
        for i in range(-DIELIK_ANCHOR_POSITION, DIELIK_ANCHOR_POSITION+1):
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
        for i in range(-DIELIK_ANCHOR_POSITION, DIELIK_ANCHOR_POSITION+1):
            ret[i] = not slovnik[-i]
        return ret

#rozsekat obrazok na stvorceky, vygenerovat z toho Dielik objekty
#kazdy dielik objekt bude mat suradnice kam pasuje - teda ze v kolkatom riadku, stlpci je vo vyslednom obrazku

#tieto dieliky chcem nahodne rozmiestnit do suflika
#suflik bude pre zaciatok proste grid dielikov z nejakymi rozostupmi
#   implementovat ako nieco podobne ploche, teda inheritovat plochu mozno, ale nie tak celkom
#   vylepsenia suflika: zoom, drag/posuvanie do boku, nastavitelny pocet riadkov

#a Plocha bude mat funkciu na detekciu spojov (resp nieco co inherituje Plochu to bude mat)
#    to chce fungovat tak, ze to bude riesit len posledny pohnuty dielik a vlastne to nechcem detekovat ked je dielik prave dragovany
#    no hej ze dielik si bude pametat, ze ci prave ten jeden frame bol dropnuty, a vtedy to plocha overi
#    ak to nastane, tak chcem tie objekty zmergeovat do jedneho, proste to nejako zmergeujem tie pngcka, nastavim vsetko tak ako ma byt - to znie ako dost pain ale velmi jednoduchy

#ako funguje dragovanie zo suflika do plochy
#   plocha aj suflik si vymenia navzajom dieliky dragnute mimo svojho uzemia (nejake edge casey ze ked dragujem mimo ale nie do toho druheho, ale to budem riesit lokalne, ze proste sa to do troch smerov nebude dat dragnut za nejaku hranicu)
#   ten druhy dostane ich absolutnu poziciu na obrazovke, skonvertuje si ju do svojej pozicie, da ten objekt tam, ten prvy suflik/plocha to vymaze

# bugs - pre nestvorcove nefunguje pasovanie
# ze to set_at() je pomale, treba pouzivat pygame.pixelArray

# oukej TODO list:
# spravit suflik
# spravit zoomovovanie, posuvanie skladacej plochy
# dokumentacia, mozno nejake skraslenie, povymazavanie nepotrebneho...
# odovzdanie

#otrasna nuda to je toto, no tie najnudnejsie casti ma len cakaju... hrozneee...