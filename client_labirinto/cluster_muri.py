import cluster

def find_clusters_muri(muri, grid_lenght_x, grid_lenght_y):
    grid = [[int(0) for x in range(grid_lenght_x)] for y in range(grid_lenght_y)]

    for muro in muri:
        grid[muro[0][0]][muro[0][1]] = 2
        grid[muro[1][0]][muro[1][1]] = 2

    return cluster.find_clusters(grid)
