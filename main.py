import pygame
from konstanty import *
from plocha import Plocha
from komponenta import Komponenta
from position import Pos
from generator import generuj
from suflik import Suflik
from zobrazovac import Zobrazovac

pygame.init()

screen = pygame.display.set_mode((SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY))
pygame.display.set_caption("Puzzle")

skladacia_plocha = Plocha(Pos(0,0))
OBRAZOK = pygame.image.load("obrazok.png").convert_alpha()
komponenty = generuj(OBRAZOK, POCET_DIELIKOV_NA_SIRKU_OBRAZKA, POCET_DIELIKOV_NA_SIRKU_OBRAZKA)

suflik = Suflik(komponenty, Pos(0, VYSKA_ZACIATKU_SUFLIKU))

zobrazovac = Zobrazovac()

clock = pygame.time.Clock()
running = True
while running:
    posun_myse = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            posun_myse = event.y
    dt = clock.tick(60) # maximalny framerate

    skladacia_plocha.update(zobrazovac.inverzny_transform(Pos(*pygame.mouse.get_pos())), zobrazovac.inverzny_transform(Pos(0, VYSKA_ZACIATKU_SUFLIKU)).y, pygame.mouse.get_pos()[1] < VYSKA_ZACIATKU_SUFLIKU)
    suflik.update(zobrazovac.inverzny_transform)
    if pygame.mouse.get_pos()[1] > VYSKA_ZACIATKU_SUFLIKU: # posuvanie sufliku
        suflik.posuvanie_update(posun_myse)
    else: # zoomovanie, posuvanie obrazovky
        posun = 1 + posun_myse * RYCHLOST_ZOOMOVANIA
        if posun < 0:
            posun = 1/abs(posun)
        zobrazovac.zoomovat(posun)
        zobrazovac.drag_posun_update()

    for kom in suflik.prelozit_na_plochu_komponenty(): # prekladanie dielikov medzi suflikom a skladacou plochou
        skladacia_plocha.pridaj_komponentu(kom)
        skladacia_plocha.navrch(kom)

    for kom in skladacia_plocha.prelozit_do_suflika_komponenty():
        suflik.pridaj_komponentu(kom)

    # zobrazovanie
    screen.fill(FARBA_POZADIA)

    zobrazovane_veci = []
    for parametre in skladacia_plocha.zobraz():
        zobrazovane_veci.append((*zobrazovac.transform(*parametre[:-1]), parametre[-1]))

    for parametre in suflik.zobraz():
        zobrazovane_veci.append((*zobrazovac.nechat(*parametre[:-1]), parametre[-1]))

    suflik_pozadie = pygame.Surface((SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY-VYSKA_ZACIATKU_SUFLIKU))
    suflik_pozadie.fill(FARBA_POZADIA_SUFLIKA)
    zobrazovane_veci.append((suflik_pozadie, Pos(0, VYSKA_ZACIATKU_SUFLIKU), 1))

    zobrazovane_veci = sorted(zobrazovane_veci, key=lambda x: x[2]) # utriedim podla priority zobrazenia, aby navrchu boli tie veci co maju byt navrchu a tak
    for z in zobrazovane_veci:
        screen.blit(z[0], z[1].tuple())
    
    pygame.display.flip()

pygame.quit()