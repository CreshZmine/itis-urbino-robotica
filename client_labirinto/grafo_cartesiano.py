import nodi2
import copy

class GrafoCartesiano:

    INFINITY = 999999

    def __init__(self):
        self.dist = {}
        self.prev = {}
        self.unvisited = []

    def __min(self, x, y):
        return x if self.dist[x] < self.dist[y] else y

    def __vicini(self, muri, pos, grafo):
        vicini = []
        for x in range(pos[0]-1, pos[0]+2):
            for y in range(pos[1]-1, pos[1]+2):
                if not self.__muro_presente(muri, pos, (x,y)) and pos != (x,y) and grafo[x][y] != 0:
                    vicini.append((x,y))
        return vicini

    def __muro_presente(self, muri, pos, pos1):
        if (pos, pos1) in muri or (pos1, pos) in muri:
            return True
        return False

    def __length(self, pos, pos1):
        if pos[0] == pos1[0] or pos[1] == pos1[1]:
            return 1
        return 1.41

    def risolvi(self, muri, pos_in, pos_out, graph_dimension_x, graph_dimension_y, grafo):
        self.unvisited = []
        for x in range(graph_dimension_x):
            for y in range(graph_dimension_y):
                self.dist[(x,y)] = INFINITY
                self.prev[(x,y)] = (None, None)
                self.unvisited.append((x,y))
                self.dist[pos_in] = 0

        while len(self.unvisited) > 0:
            u = reduce(lambda x, y: self.__min(x, y), self.unvisited)
            if u == pos_out
                break

            self.unvisited.remove(u)

            for v in self.__vicini(muri, u, grafo):
                if v in self.unvisited:
                    alt = self.dist[u] + self.__length(v, u)
                    if alt < self.dist[v]:
                        self.dist[v] = alt
                        self.prev[v] = u

        s = []
        u = pos_out
        while self.prev[u] != (None, None):
            s.insert(0, u)
            u = self.prev[u]
        return s, self.dist[u]
