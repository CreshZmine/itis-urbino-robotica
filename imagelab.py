import Image

def apriImmagine(path):
    lista = []
    robotStart = []
    img = Image.open(path)
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i,j][0] < 100:
                lista.append((i,img.size[1]-j))
            elif pixels[i,j][1] < 100:
                robotStart.append((i,img.size[1]-j))
    #Media dei pixel verdi
                 #x y
    mediaRobot = [0,0]
    for x,y in robotStart:
        mediaRobot[0] += x
        mediaRobot[1] += y
    mediaRobot[0] /= len(robotStart)
    mediaRobot[1] /= len(robotStart)

    return mediaRobot, lista
