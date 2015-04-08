import cluster
import copy

def find_clusters_muri(muri, grid_lenght_x, grid_lenght_y):
    grid = [[int(0) for x in range(grid_lenght_x)] for y in range(grid_lenght_y)]

    for muro in muri:
        grid[muro[0][0]][muro[0][1]] = 2
        grid[muro[1][0]][muro[1][1]] = 2

    return cluster.find_clusters(grid)

def __distanza(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def __piu_vicino(a, b, pos):
    return a if __distanza(a[0], pos) < __distanza(b[0], pos) else b

def trova_muro_vicino(pos, muri, muri_passato):
    mur = copy.deepcopy(muri)
    for i in range(len(mur)):
        if muri_passato[i]:
            mur.remove(mur[i])
    if len(mur) == 0: #tutti i muri esplorati
        return None
    mur = reduce(lambda x, y: __piu_vicino(x, y, pos), muri)
    return mur[0] if __distanza(pos, mur[0]) < __distanza(pos, mur[1]) else mur[1]
