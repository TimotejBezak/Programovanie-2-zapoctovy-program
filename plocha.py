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

    def drag_update(self, mys_realna_pozicia):
        for kom in self.komponenty:
            kom.drag_update(mys_realna_pozicia, self.zoom)
            if kom.je_mys_nad_mnou(mys_realna_pozicia) and pygame.mouse.get_pressed()[0] and not self.mys_stlacena_minule:
                kom.drag_start(mys_realna_pozicia)
                self.navrch(kom)
                break
        self.mys_stlacena_minule = pygame.mouse.get_pressed()[0]

    def update(self, mys_realna_pozicia, vyska_zaciatku_sufliku, mam_povolenie_dragovat_dieliky): #volane kazdy frame
        if mam_povolenie_dragovat_dieliky:
            self.drag_update(mys_realna_pozicia)

        for kom in self.komponenty:
            if kom.rotacia_update(mys_realna_pozicia):
                self.navrch(kom)
                self.vyries_pasovanie(kom)
                break
        for kom in self.komponenty:
            kom.pravy_klik_update()

        for kom in self.komponenty:
            if kom.bol_prave_polozeny():
                if kom.pos.y > vyska_zaciatku_sufliku:
                    if len(kom.dieliky) == 1:
                        self.prelozit_do_suflika.append(kom)
                        self.komponenty.remove(kom)
                    else:
                        pass
                else:
                    self.vyries_pasovanie(kom)

    def navrch(self, kom):
        idx = self.komponenty.index(kom)
        self.komponenty = [self.komponenty[idx]] + self.komponenty[:idx] + self.komponenty[idx+1:]#posuniem ho dopredu nech je nad vsetkym uplne

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
                priorita = 0 # ze v akom poradi sa to bude zobrazovat
                if kom.je_dragovany():
                    priorita = 3
                ret.append((*d, priorita))
        return ret
