import pygame
from konstanty import *
from plocha import Plocha
from komponenta import Komponenta
from position import Pos
from generator import generuj

pygame.init()

screen = pygame.display.set_mode((SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY))
pygame.display.set_caption("Puzzle")

# image = pygame.image.load("test_transparentne.png").convert_alpha()

skladacia_plocha = Plocha(1.0, Pos(0,0))
# skladacia_plocha.pridaj_dielik(Komponenta(pygame.image.load("test_transparentne.png").convert_alpha(), Pos(100,167), Pos(0,0)))

obrazok_skibidi = pygame.image.load("skibidi mensie.png").convert_alpha()
komponenty = generuj(obrazok_skibidi, 5, 5)
for k in komponenty:
    skladacia_plocha.pridaj_komponentu(k)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    skladacia_plocha.update()

    screen.fill(FARBA_POZADIA)

    # scaled_image = pygame.transform.scale( image, (int(image.get_width() * scale), int(image.get_height() * scale)) )
    for parametre in skladacia_plocha.zobraz():
        screen.blit(*parametre)
    pygame.display.flip()

pygame.quit()