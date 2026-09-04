import pygame
from komponenta import Komponenta
from position import Pos
import random
from konstanty import *
from dielik import Dielik

#PLAN POSTUPU K VITAZSTVU

def sekame_obrazok(obrazok, sirka_pocet, vyska_pocet):#kolko dielikov je to na sirku a kolko na vysku
    sirka = obrazok.get_width() // sirka_pocet #pozor na nedelitelnost, neviem mozno by som si mohol dat na to pozor aby to bolo proste delitelne
    vyska = obrazok.get_height() // vyska_pocet
    obrazky = [[pygame.Surface((sirka, vyska), pygame.SRCALPHA) for _ in range(sirka_pocet)] for _ in range(vyska_pocet)]
    for i in range(obrazok.get_width()):
        for j in range(obrazok.get_height()):
            s,r = i//sirka, j//vyska
            obrazky[r][s].set_at((i%sirka, j%vyska), obrazok.get_at((i, j)))
    return obrazky

def generujeme_dieliky(obrazky):
    ret = []
    for i in range(len(obrazky)):
        for j in range(len(obrazky[0])):
            ret.append(Komponenta([Dielik(obrazky[i][j], Pos(0,0), Pos(j, i))], Pos(random.randint(0,SIRKA_OBRAZOVKY-1),random.randint(0,VYSKA_OBRAZOVKY-1))))
    return ret

def generuj(obrazok, sirka_pocet, vyska_pocet):
    return generujeme_dieliky(sekame_obrazok(obrazok, sirka_pocet, vyska_pocet))


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


# plan na najblizsiu chvilu:
# vytvorit objekt *komponenta*, ktory bude mat v sebe nejake dieliky (uz spojene akoze)
# spajanie budem detekovat komponentami, spravny pasujuci offset vyratam nejakym dfs
# pripajanie tiez bude proste fungovat to bude len proste nasupanie vsetkych dielikov do jednej z nich, zo spravnym offsetom pozicie

#otrasna nuda to je toto