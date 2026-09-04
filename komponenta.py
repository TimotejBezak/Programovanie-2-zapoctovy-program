import pygame
from funkcie_navyse import is_mouse_over_image
from position import Pos

class Komponenta:
    def __init__(self, dieliky, pos):
        self.dieliky = dieliky
        self.pos = pos
        self.drag_start_mys_pos = None # pozicia myse pri zacati dragovania
        self.drag_start_pos = None # self.pos v case zacatia dragovania
        self.dragujem = False # True kym drzim stlacene tlacidlo nad dielikom
        self.prave_polozeny = False

    def drag_update(self, zoom): #volat kazdy frame, ktory je mys nad tymto dielikom
        self.prave_polozeny = False
        if pygame.mouse.get_pressed()[0]:
            mys_pos = Pos(*pygame.mouse.get_pos())
            if self.dragujem == False and self.je_mys_nad_mnou(zoom):
                self.dragujem = True
                self.drag_start_mys_pos = mys_pos
                self.drag_start_pos = self.pos
            if self.dragujem:
                self.pos = self.drag_start_pos + mys_pos - self.drag_start_mys_pos
        else:
            if self.dragujem:
                self.prave_polozeny = True
            self.dragujem = False

    def bol_prave_polozeny(self):
        return self.prave_polozeny

    def je_mys_nad_mnou(self, zoom):
        for d in self.dieliky: # kontrolujem vsetky svoje dieliky
            if is_mouse_over_image(d.image, self.pos + d.offset, zoom):
                return True
        return False

    def pozicie_dielikov_pre_kreslenie(self): # vrati vsetky pozicie svojich dielikov aj s obrazkami, aby sa nakreslili
        ret = []
        for d in self.dieliky:
            ret.append((d.image, (self.pos + d.offset).tuple()))
        return ret

    def set_vyslednych_pozic(self):
        ret = set()
        for d in self.dieliky:
            ret.add(d.vysledny_pos.tuple())
        return ret

    def najdi_svoj_dielik_podla_vysledneho_pos(self, vys_pos):
        for d in self.dieliky:
            if d.vysledny_pos == vys_pos:
                return d
        return -1

    def offset_ze_pasujem_do_komponenty(self, kom): # offset komponenty kom od self taky, ze do mna pasuje, -1 ak sa to neda
        vys_pos_self = self.set_vyslednych_pozic()
        vys_pos_kom = kom.set_vyslednych_pozic()
        navstivene = set()
        pasujuci = self.najdi_pasujucu_dvojicu(self.dieliky[0].vysledny_pos, navstivene, vys_pos_self, vys_pos_kom)
        if pasujuci == -1:
            return -1

        pasujuci_self, pasujuci_kom = self.najdi_svoj_dielik_podla_vysledneho_pos(pasujuci[0]), kom.najdi_svoj_dielik_podla_vysledneho_pos(pasujuci[1])
        return pasujuci_self.offset + (pasujuci_kom.vysledny_pos - pasujuci_self.vysledny_pos)*self.dlzka_strany_dielika() - pasujuci_kom.offset # checknem este

    def susedia_pozicie(self, pos): # vsetci mozny susedia danej pozicie
        smery = [Pos(0,1), Pos(0,-1), Pos(1,0), Pos(-1,0)]
        ret = []
        for smer in smery:
            ret.append(smer+pos)
        return ret

    def susedia_dieliku(self, kandidati, vys_pos_set): # vyfiltruje z kandidatov iba tie pozicie co existuju v komponente self, vys_pos_set je set vyslednych pozicie tejto komponenty
        ret = []
        for nadejnik in kandidati:
            if nadejnik.tuple() in vys_pos_set:
                ret.append(nadejnik)
        return ret

    def najdi_pasujucu_dvojicu(self, v, navstivene, vys_pos_self, vys_pos_kom): # -1 ak neexistuje, hladame dvojicu pozicii dielikov zo self a z kom, ktore susedia hranou
        if v.tuple() in navstivene:
            return -1
        navstivene.add(v.tuple())

        sus_poz = self.susedia_pozicie(v)
        sus_die = self.susedia_dieliku(sus_poz, vys_pos_self)
        # print(*sus_poz, "   medzera   ", *vys_pos_kom, "   medzera   ", *vys_pos_self)
        for sused in sus_poz:
            if sused.tuple() in vys_pos_kom: # je to dielik z tej druhej komponenty
                return (v, sused)
            if sused in sus_die:
                bu = self.najdi_pasujucu_dvojicu(sused, navstivene, vys_pos_self, vys_pos_kom)
                if bu != -1:
                    return bu

        return -1

    def dlzka_strany_dielika(self):
        return self.dieliky[0].image.get_width() # pozor na nestvorcove

    def spoj_sa_s(self, kom): # spojim sa s kom, kom treba vymazat potom, ratam s tym, ze uz je na spravnom mieste
        offset = kom.pos - self.pos
        for d in kom.dieliky:
            d.offset = d.offset + offset
            self.dieliky.append(d)