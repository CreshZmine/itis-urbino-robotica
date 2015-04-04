import copy

def _clusterize_(found, grid, x, y):
    lista_t = []
    i = 0
    for x_c in range(x-1, x+2):
        for y_c in range(y-1, y+2):
            i = i+1
            try:
                if grid[x_c][y_c] == 2 and i % 2 == 0:
                    lista_t.append((x_c,y_c))
                    found.append((x_c,y_c))
                    grid[x_c][y_c] = 3
            except IndexError:
                pass
    for elem in lista_t:
        _clusterize_(found, grid, elem[0], elem[1])

def find_clusters(grid):
    '''
        3 - gia preso in considerazione
    '''
    grid2 = copy.deepcopy(grid)

    found = []
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            if grid2[x][y] == 2:
                grid2[x][y] = 3
                found.append([(x,y)])
                _clusterize_(found[-1], grid2, x, y)
    return found

def find_centers(found):
    res = []
    for cluster_orig in found:
        cluster = copy.deepcopy(cluster_orig)
        lim = 4
        while lim > 1:
            while not minimizzato(cluster, lim):
                cluster = riduci(cluster, lim)
            lim -= 1
        res.append(trovaMaggiore(cluster))
    return res

def riduci(cluster, min):
    cl_final = copy.deepcopy(cluster)
    for point in cluster:
        if conta_vicini(cluster, cluster.index(point)) < min:
            cl_final.remove(point)
    return cl_final

def minimizzato(cluster, min):
    for point in cluster:
        if conta_vicini(cluster, cluster.index(point)) == min:
            return False
    return True

def trovaMaggiore(cluster):
    return reduce(lambda x, y: maggiore_vicini(cluster, x, y), cluster)

def maggiore_vicini(cluster, a, b):
    if conta_vicini(cluster, cluster.index(a)) >= conta_vicini(cluster, cluster.index(b)):
        return a
    return b

def conta_vicini(cluster, punto_index):
    tot = 0
    i = 0
    cl = copy.deepcopy(cluster)
    (x, y) = cl.pop(punto_index)
    for y_c in range(y-1, y+2):
        for x_c in range(x-1, x+2):
            if (x_c, y_c) in cl and i%2==1:
                tot = tot+1
            i = i+1
    return tot
