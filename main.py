import pygame
from konstanty import *
from plocha import Plocha
from dielik import Dielik
from position import Pos

pygame.init()

# Okno
screen = pygame.display.set_mode((VYSKA_OBRAZOVKY, SIRKA_OBRAZOVKY))
pygame.display.set_caption("Puzzle")

# Obrazok
# image = pygame.image.load("test_transparentne.png").convert_alpha()

skladacia_plocha = Plocha(1.0, Pos(0,0))
skladacia_plocha.pridaj_dielik(Dielik("test_transparentne.png", Pos(100,167)))

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
    # screen.blit(scaled_image, (x, y))
    pygame.display.flip()

pygame.quit()