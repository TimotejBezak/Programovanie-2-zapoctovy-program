from funkcie_navyse import is_mouse_over_image

class Plocha:
    def __init__(self, zoom, pos):
        self.zoom = zoom
        self.pos = pos
        self.dieliky = []#vsetky dieliky v danej ploche, ich pozicie su relativne pozicie k ploche

    def pridaj_dielik(self, dielik):
        self.dieliky.append(dielik)

    def update(self): #volane kazdy frame
        for dielik in self.dieliky:
            dielik.drag_update(is_mouse_over_image(dielik.image, dielik.pos, self.zoom))

    def zobraz(self): #zobrazi vsetky dieliky na spravne pozicie
        ret = []
        for dielik in self.dieliky:
            ret.append((dielik.image, dielik.pos.tuple())) # tu bude teda nejaky offset potom
        return ret
