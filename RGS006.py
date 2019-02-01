from PIL import Image
import numpy as  np
from time import time, sleep
import cv2

# Matriz para threshold
limit = [ 80, 80, 80]
# Tamano de caja de probabilidad
box = 80

def tanto(l1):
    return l1[2]*4+l1[1]*2+l1[0]

def inBox(punto, color):
    if len(coords)==0:
        return True
    elif abs(punto[0]-coords[color][0])<box and abs(punto[1]-coords[color][1])<box:
        return True
    else:
        return False

# En coords se van a guardar las coordenadas de
# los baricentros de las manchas de cada color
# cuyos pixeles estan guardados en cada saco.
coords = []

paleta = [ [115, 55, 50],   # cyan
           [ 50, 50, 50],   # negro
           [ 50,140,150],   # amarillo
           [ 40, 40,140]]   # magenta

tabla  = [ [  True, False, False],   # cyan
           [ False, False, False],   # negro
           [ False,  True,  True],   # amarillo
           [ False, False,  True]]   # magenta
dire = [ 1, 0, -1, -1, 3, -1, 2, -1]

camera_port = 0
camera = cv2.VideoCapture(camera_port)
sleep(0.1)  # If you don't wait, the image will be dark
return_value, image = camera.read()

zona = [ [0, 0], [image.shape[0], image.shape[1]] ]
corte = np.array([ [ limit ]*image.shape[1] ]*image.shape[0])

cero = time()
#print('Inicio ', cero)

while True:

    inicio = time()
    return_value, bmpIn = camera.read()

    if return_value:

        start = time()

        # Matriz binaria
        bmpThr = (bmpIn > corte)

        saco = [ [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
        colorin = np.zeros([ 4, 3 ])

        for j in range(zona[0][0],zona[1][0],10):
            # Iteracion sobre las franjas horizontales de la imagen
            for i in range(zona[0][1],zona[1][1],10):
            #for i in range(0,image.shape[1],10):
                # Iteracion sobre los pixeles
                if bmpThr[j][i].tolist() <> [ True, True, True ]:
                    # Si el pixel no es blanco
                    S = dire[tanto(bmpThr[j][i])]
                    if S>-1:
                        if inBox([ i, j ], S):
                            saco[S][0] = saco[S][0] + i      # Se suma el x,y del pixel al n-esimo saco
                            saco[S][1] = saco[S][1] + j
                            saco[S][2] = saco[S][2] + 1      # y se incrementa su contador interno
                            colorin[S] += bmpIn[j][i]

        relev = time()

        for n,s in enumerate(saco):
            # Se promedian los sacos
            while len(coords)<n+1:
                coords.append([])
            if s[2]>0:
                coords[n] = [ s[0]*1.0/s[2], s[1]*1.0/s[2] ]
                colorin[n] /= s[2]

        paleta = np.uint8(colorin)

        estudio = time()

        # Dibuja cruces en los baricentros de las manchas
        for g in range(-45, 45):
            for n,c in enumerate(coords):
                try:
                    bmpIn[int(c[1])][int(c[0])+g] = np.array(paleta[n])
                    bmpIn[int(c[1])+g][int(c[0])] = np.array(paleta[n])
                except:
                    pass

        cv2.imshow('Out',bmpIn)

        save = time()
        print('Total ', save-inicio)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
print paleta
cv2.destroyAllWindows()
