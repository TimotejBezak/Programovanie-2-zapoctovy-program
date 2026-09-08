from funkcie_navyse import is_mouse_over_image
import pygame
from konstanty import *
from komponenta import Komponenta

class Plocha:
    def __init__(self, zoom, pos):
        self.zoom = zoom
        self.pos = pos
        self.komponenty = []#vsetky dieliky v danej ploche, ich pozicie su relativne pozicie k ploche
        self.prelozit_do_suflika = []
        self.mys_stlacena_minule = False

    def pridaj_komponentu(self, komponenta):
        self.komponenty.append(komponenta)

    def drag_update(self):
        for idx, kom in enumerate(self.komponenty):
            kom.drag_update(self.zoom)
            if kom.je_mys_nad_mnou(self.zoom) and pygame.mouse.get_pressed()[0] and not self.mys_stlacena_minule:
                kom.drag_start()
                self.komponenty = [self.komponenty[idx]] + self.komponenty[:idx] + self.komponenty[idx+1:]#posuniem ho dopredu nech je nad vsetkym uplne
                break
        self.mys_stlacena_minule = pygame.mouse.get_pressed()[0]

    def update(self): #volane kazdy frame
        self.drag_update()

        for kom in self.komponenty:
            if kom.rotacia_update(self.zoom):
                break
        for kom in self.komponenty:
            kom.pravy_klik_update()

        for kom in self.komponenty:
            if kom.bol_prave_polozeny():
                if kom.pos.y > VYSKA_ZACIATKU_SUFLIKU:
                    self.prelozit_do_suflika.append(kom)
                    self.komponenty.remove(kom)
                else:
                    self.vyries_pasovanie(kom)

    def prelozit_do_suflika_komponenty(self):
        ret = self.prelozit_do_suflika
        self.prelozit_do_suflika = []                
        return ret

    def vyries_pasovanie(self, kom): # skontroluje ci komponenta s niecim pasuje, ak ano tak to vyriesi
        for kom_nadejnik in self.komponenty:
            if kom_nadejnik == kom:
                continue
            offset = kom_nadejnik.offset_ze_pasujem_do_komponenty(kom)
            if offset != -1:
                kom_ideal_pos = kom_nadejnik.pos + offset
                if kom_ideal_pos.vzdialenost_do(kom.pos) < MAX_VZDIALENOST_NA_ZAPASOVANIE:
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
