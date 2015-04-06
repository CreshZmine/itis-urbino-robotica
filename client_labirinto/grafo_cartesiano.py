import nodi2
import copy

class GrafoCartesiano:
    def __init__(self, muri, pos_in, pos_out):
        self.grafo = nodi2.Grafo()
        self.pos_in = pos_in
        self.pos_out = pos_out

    def risolvi(self):
        coor_muri_t = map(__trova_coor, self.muri)
        coor_muri = []
        for el in coor_muri_t:
            coor_muri.append(el[0])
            coor_muri.append(el[1])
        #TODO

    def __trova_coor(self, muro):
        coor = copy.deepcopy(muro[0])
        if muro[0][0] != muro[1][0]: #E' stata modificata la componente x
            coor[0] = muro[0][0] if muro[0][0] > muro[1][0] else muro[1][0]
            coor1 = copy.deepcopy(coor)
            coor1[1] += 1
        elif muro[0][1] != muro[1][1]: #E' stata modificata la componente y
            coor[1] = muro[0][1] if muro[0][1] > muro[1][0] else muro[1][1]
            coor1 = copy.deepcopy(coor)
            coor1[0] += 1
        return coor, coor1
