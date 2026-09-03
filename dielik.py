import pygame
from funkcie_navyse import is_mouse_over_image
from position import Pos

class Dielik:
    def __init__(self, image_source, pos):
        self.image = pygame.image.load(image_source).convert_alpha()
        self.pos = pos
        self.drag_start_mys_pos = None # pozicia myse pri zacati dragovania
        self.drag_start_pos = None # self.pos v case zacatia dragovania
        self.dragujem = False # True kym drzim stlacene tlacidlo nad dielikom

    def drag_update(self, je_na_nom_kurzor): #volat kazdy frame, kvoli dragovaniu dieliku
        mys_pos = Pos(*pygame.mouse.get_pos())
        if je_na_nom_kurzor and pygame.mouse.get_pressed()[0]:
            if self.dragujem == False:
                self.dragujem = True
                self.drag_start_mys_pos = mys_pos
                self.drag_start_pos = self.pos
            self.pos = self.drag_start_pos + mys_pos - self.drag_start_mys_pos
        else:
            self.dragujem = False