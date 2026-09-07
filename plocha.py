from funkcie_navyse import is_mouse_over_image
import pygame
from konstanty import *
from komponenta import Komponenta

class Plocha:
    def __init__(self, zoom, pos):
        self.zoom = zoom
        self.pos = pos
        self.komponenty = []#vsetky dieliky v danej ploche, ich pozicie su relativne pozicie k ploche

    def pridaj_komponentu(self, komponenta):
        self.komponenty.append(komponenta)

    def update(self): #volane kazdy frame
        for idx, kom in enumerate(self.komponenty):
            kom.drag_update(self.zoom)
            if kom.je_mys_nad_mnou(self.zoom) and pygame.mouse.get_pressed()[0]:
                self.komponenty = [self.komponenty[idx]] + self.komponenty[:idx] + self.komponenty[idx+1:]#posuniem ho dopredu nech je nad vsetkym uplne
                break

        for kom in self.komponenty:
            kom.rotacia_update(self.zoom)

        for kom in self.komponenty:
            if kom.bol_prave_polozeny():
                print("bol prave polozeny")
                self.vyries_pasovanie(kom)
                

    def vyries_pasovanie(self, kom): # skontroluje ci komponenta s niecim pasuje, ak ano tak to vyriesi
        for kom_nadejnik in self.komponenty:
            if kom_nadejnik == kom:
                continue
            offset = kom_nadejnik.offset_ze_pasujem_do_komponenty(kom)
            if offset != -1:
                kom_ideal_pos = kom_nadejnik.pos + offset#*kom.dlzka_strany_dielika()
                if kom_ideal_pos.vzdialenost_do(kom.pos) < MAX_VZDIALENOST_NA_ZAPASOVANIE:
                    print("pasuje")
                    kom.pos = kom_ideal_pos
                    self.spoj_komponenty(kom, kom_nadejnik)

    def spoj_komponenty(self, k1, k2):
        k1.spoj_sa_s(k2)
        self.komponenty.remove(k2)

    def zobraz(self): #zobrazi vsetky dieliky na spravne pozicie
        ret = []
        for kom in reversed(self.komponenty): # self.dieliky su v poradi, ze prvy ma byt navrchu
            for d in kom.pozicie_dielikov_pre_kreslenie():
                ret.append(d) # tu bude teda nejaky offset potom
        return ret
